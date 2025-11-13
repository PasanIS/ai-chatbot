from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings


engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)


def get_db_info():
    inspector = inspect(engine)
    try:
        table_names = inspector.get_table_names()
        schema_info = {}

        for table_name in table_names:
            columns_info = inspector.get_columns(table_name)

            schema_info[table_name] = []
            for column in columns_info:
                col_details = {
                    "name": column['name'],
                    "type": str(column['type']),
                    "nullable": column['nullable'],
                    "default": column.get('default'),
                    "primary_key": column.get('primary_key', False)
                }
                schema_info[table_name].append(col_details)

        return {
            "database_schema": schema_info,
            "total_tables": len(table_names),
            "table_names": table_names
        }
    except Exception as e:
        return {"error": f"Failed to get database schema: {str(e)}"}