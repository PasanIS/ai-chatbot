from sqlalchemy import Column, String, DateTime, func, ForeignKey
from app.db.dbconnection import Base


class Prescriptions(Base):
    __tablename__ = "prescriptions"

    prescription_id = Column(String(50), primary_key=True, nullable=False, index=True)
    doctor_id = Column(String(50), ForeignKey("doctors.doctor_id"), nullable=False, index=True)
    customer_id = Column(String(50), ForeignKey("customers.customer_id"), nullable=False, index=True)
    date_issued = Column(DateTime, default=func.now(), nullable=False)
    diagnosis = Column(String(50), nullable=False)
