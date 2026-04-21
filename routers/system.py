from repository.system_repository import SystemRepository
from fastapi import APIRouter, Depends ,HTTPException
from db.session import get_db
router = APIRouter(
    prefix="/system",
    tags=["system"],
    dependencies=[Depends(SystemRepository)],
    responses={404: {"description": "Not found"}},

)

@router.get("/status")
def get_system_status(db = Depends(get_db)):
    is_healthy =SystemRepository.get_system_status(db)

    if not is_healthy:
        raise HTTPException(status_code=503, detail="System is unhealthy")
    return {"status": "ok", "message": "System is healthy  and database connection is successful."}

