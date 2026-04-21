from sqlalchemy.orm import Session
from sqlalchemy import text


class SystemRepository:
    @staticmethod
    def get_system_status(db: Session):
        try:
            # Simple query to check if the database is responsive
            db.execute(text("SELECT 1"))
            return {"status": "ok", "message": "Database connection successful."}
        except Exception as e:
            return {"status": "error", "message": f"Database connection failed: {str(e)}"}