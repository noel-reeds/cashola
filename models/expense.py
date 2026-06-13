from sqlalchemy import DateTime, Integer, Column, String, ForeignKey, Numeric
from models import Base
from sqlalchemy.sql import func
import uuid

class Expense(Base):
    """
    Defines expenditure class, initialization and a
    to_dict function for serialization.
    """
    __tablename__ = 'expenses'

    id = Column(String, primary_key=True, nullable=True)
    user_id = Column(Integer, ForeignKey('user_accounts.id'), nullable=True)
    receipt_no = Column(String(20), nullable=True)
    description = Column(String(500), nullable=True)
    name = Column(String(100), nullable=True)
    amount = Column(Numeric(precision=2), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


    def __init__(self, *args, **kwargs) -> None:
        """
        Instantiation of an expense object.

        Params
        *args, **kwargs to init the instance.
        """
        if kwargs:
            self.amount = kwargs.get('amount')
            self.category = kwargs.get('category')
            self.name = kwargs.get('name')
            self.description = kwargs.get('description')
            self.user_id = kwargs.get('user_id')
        self.id = str(uuid.uuid4())
    
    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the expense.
        """
        return dict(id=self.id,
                    category=self.category,
                    user_id=self.user_id,
                    description=self.description,
                    name=self.name,
                    amount_spent=self.amount,
                    created_at=self.created_at,
                    updated_at=self.updated_at
                )
    def __str__(self) -> str:
        """
        Return a custom str representation of the expenditure
        object in place.
        """
        return 'You spent KES.{} on {}.'.format(self.amount, self.name)
