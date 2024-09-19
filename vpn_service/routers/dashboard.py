from fastapi import APIRouter, Depends
from app.models import Stats
from app.routers.auth import get_current_user

router = APIRouter()

@router.get("/dashboard")
def get_dashboard(current_user = Depends(get_current_user)):
    stats = [
        Stats(site_name="example.com", page_visits=12, data_sent=1000, data_received=2000)
    ]
    return {"user": current_user.username, "stats": stats}