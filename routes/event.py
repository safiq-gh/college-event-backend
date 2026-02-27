from fastapi import APIRouter
from database import supabase

router = APIRouter()

@router.get("/event")
def get_event():
    try:
        response = supabase.table("event_config").select("*").single().execute()
        return {"success": True, "data": response.data}
    except Exception as e:
        return {"success": False, "error": {"code": "NOT_FOUND", "message": "Event not found."}}