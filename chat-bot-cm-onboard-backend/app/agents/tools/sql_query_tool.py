from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from sqlalchemy import text
import traceback

from app.agents.llm_manager import get_llm
from app.core.loggers import logger
from app.db.dbconnection import SessionLocal, get_db_info
from app.agents.prompts.sql_generator_prompt import SQL_GENERATOR_PROMPT
from app.agents.prompts.sql_nl_responder_prompt import SQL_NL_RESPONDER_PROMPT

@tool
def sql_query_tool(user_query: list) -> str:
    """
    Generate and Execute SQL query from user_query using SQLAlchemy
    """
    messages = user_query
    user_query_content = user_query[-1]['content']

    logger.info(f"sql_query_tool received messages: {messages}")

    # --- Step 1: Generate SQL Query ---
    try:
        llm_sql_gen = get_llm(temperature=0)
        db_schema =get_db_info()
        logger.info(f"DB schema: {db_schema}")
        formatted_prompt = SQL_GENERATOR_PROMPT.format(database_schema=db_schema)

        gen_messages = [
            SystemMessage(content=formatted_prompt),
            HumanMessage(content=f"user query: {user_query_content} + conversation history: {messages}")
        ]


        response = llm_sql_gen.invoke(gen_messages)
        sql_query = response.content.strip().replace("`", "") # Clean up backticks

        logger.info(f"LLM Generated Query:\n{sql_query}")

        if not any(sql_query.lower().startswith(k) for k in ["select", "insert", "update", "delete"]):
            logger.warning(f"LLM did not generate a valid SQL query: {sql_query}")
            return "The LLM did not generate a valid SQL query."

    except Exception as e:
        logger.error(f"Error generating query: {e}\n{traceback.format_exc()}")
        return f"Error generating query: {e}"

    # --- Step 2: Execute SQL Query ---
    session = SessionLocal()
    try:
        result = session.execute(text(sql_query))

        if sql_query.lower().startswith("select"):
            rows = result.fetchall()
            keys = result.keys()
            data = [dict(zip(keys, row)) for row in rows]
            logger.info(f"SQL result data (rows found: {len(data)}): {data}")

            # --- Step 3: Convert SQL Result to Natural Language ---
            system_message2 = SQL_NL_RESPONDER_PROMPT
            messages2 = [
                SystemMessage(content=system_message2),
                HumanMessage(content=f"user query: {user_query_content} + conversation history: {messages}\n\nSQL result: {data}")
            ]

            llm_nl_gen = get_llm(temperature=0)
            response2 = llm_nl_gen.invoke(messages2)
            logger.info(f"Final bot response:\n{response2.content}")
            return response2.content
        else:
            session.commit()
            logger.info("Successfully executed non-select query.")
            return "Query executed successfully."

    except Exception as e:
        session.rollback()
        logger.error(f"Error executing query: {e}\n{traceback.format_exc()}")
        return f"Error executing query: {e}"
    finally:
        session.close()