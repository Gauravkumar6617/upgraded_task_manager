from db.session import Base
from typing import Optional
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, Text, Boolean ,DateTime
class Task(Base):
    __tablename__ = 'tasks'
    __table__args__ = {'extend_existing': True, 'comment': "Task model representing a to-do item."}
    
    id: Optional[int] = Column(Integer, primary_key=True, index=True, comment="Unique identifier for the task.")
    title: str = Column(String(255), nullable=False, comment="Title of the task.")
    description: Optional[str] = Column(Text, nullable=True, comment="Detailed description of the task.")
    completed: bool = Column(Boolean, default=False, comment="Status indicating if the task is completed.") 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, Bread, Eggs, and Fruits",
                "completed": False
            }
        }



        def __repr__(self):
            return f"<Task(id={self.id}, title='{self.title}', completed={self.completed})>"