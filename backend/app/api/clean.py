from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.response import success
from app.core.security import require_roles
from app.database.session import get_db
from app.services.clean_service import CleanService

router = APIRouter(prefix="/api/clean", tags=["clean"])


@router.post("/run")
def run_clean(db: Session = Depends(get_db), _: object = Depends(require_roles("admin", "analyst"))):
    return success(CleanService(db).run())
