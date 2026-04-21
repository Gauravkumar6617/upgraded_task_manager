from sqlalchemy.orm import Session
from models.task import Task
from schemas.tasks import TaskCreate

class TaskRepository:
    """Repository for managing Task database operations."""

    @staticmethod
    def create_task(db: Session, task: TaskCreate) -> Task:
        # Use **dict to unpack instead of manual mapping
        # This keeps the code clean if you add new fields later
        db_task = Task(**task.model_dump()) 
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def get_tasks(db: Session, skip: int = 0, limit: int = 100):
        """Retrieve tasks with Pagination (Essential for Concept #12)."""
        return db.query(Task).offset(skip).limit(limit).all()

    @staticmethod
    def get_task(db: Session, task_id: int):
        return db.query(Task).filter(Task.id == task_id).first()

    @staticmethod
    def update_task(db: Session, task_id: int, task_data: TaskCreate):
        """Update using a single query (More efficient)."""
        db_query = db.query(Task).filter(Task.id == task_id)
        db_task = db_query.first()
        
        if not db_task:
            return None
        
        # update() is faster than manual attribute assignment for many fields
        db_query.update(task_data.model_dump(), synchronize_session=False)
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def delete_task(db: Session, task_id: int) -> bool:
        """Efficient delete."""
        db_query = db.query(Task).filter(Task.id == task_id)
        db_task = db_query.first()
        
        if not db_task:
            return False
            
        db_query.delete(synchronize_session=False)
        db.commit()
        return True