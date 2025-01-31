from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.helper.genericHelper import convertKeysToCamelCase
from app.utils.logger import logger
from app.dependencies import get_db
from app.security import validate_token
from app.queries.warehouse import GET_WAREHOUSE_DETAILS

router = APIRouter()
security_scheme = HTTPBearer()

@router.get("/getWarehouseList")
def get_warehouse_details(
    db: Session = Depends(get_db),
    current_user: str = Depends(security_scheme),
    authorization: str = Header(None, description="Bearer token for authentication")
):
    """
    Fetch warehouse details.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Authorization header missing or invalid")
    
    token = authorization.split(" ")[1]
    payload = validate_token(token, db)
    
    try:
        logger.info(f"Request received for /getWarehouseList from - {payload.get('user_login_id')}")
        result = db.execute(text(GET_WAREHOUSE_DETAILS)).mappings().all()
        return {
            "wareHouseList": convertKeysToCamelCase(result),
        }
    except Exception as e:
        logger.error(f"Failed to getWarehouseList: {e}")
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")
