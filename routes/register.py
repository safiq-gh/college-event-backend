from fastapi import APIRouter
from database import supabase
from models import RegistrationRequest
from datetime import date

router = APIRouter()

def generate_registration_id():
    today = date.today().strftime("%Y%m%d")
    response = supabase.table("registrations") \
        .select("registration_id") \
        .like("registration_id", f"REG-{today}-%") \
        .execute()
    count = len(response.data) + 1
    return f"REG-{today}-{str(count).zfill(4)}"


@router.get("/register/check")
def check_email(email: str):
    response = supabase.table("registrations") \
        .select("email") \
        .eq("email", email) \
        .execute()

    return {"success": True, "data": {"registered": len(response.data) > 0}}


@router.post("/register", status_code=201)
def register(payload: RegistrationRequest):
    if len(payload.name) < 2:
        return {"success": False, "error": {"code": "VALIDATION_ERROR", "message": "Name is too short."}}
    if not payload.phone.isdigit() or len(payload.phone) != 10:
        return {"success": False, "error": {"code": "VALIDATION_ERROR", "message": "Phone must be a 10-digit number."}}
    if not (1 <= payload.year <= 5):
        return {"success": False, "error": {"code": "VALIDATION_ERROR", "message": "Year must be between 1 and 5."}}
    if not payload.event_ids:
        return {"success": False, "error": {"code": "VALIDATION_ERROR", "message": "Select at least one event."}}

    registration_id = generate_registration_id()

    try:
        response = supabase.table("registrations").insert({
            "registration_id": registration_id,
            "name": payload.name,
            "email": payload.email,
            "phone": payload.phone,
            "college": payload.college,
            "department": payload.department,
            "year": payload.year,
            "event_ids": payload.event_ids,
            "transaction_id": payload.transaction_id,
            "status": "pending_verification"
        }).execute()

        data = response.data[0]
        return {
            "success": True,
            "data": {
                "registration_id": data["registration_id"],
                "name": data["name"],
                "email": data["email"],
                "status": data["status"],
                "message": "Registration submitted. You'll receive a confirmation once payment is verified."
            }
        }

    except Exception as e:
        error_str = str(e)
        if "23505" in error_str:
            if "email" in error_str:
                return {"success": False, "error": {"code": "DUPLICATE_EMAIL", "message": "This email is already registered."}}
            if "phone" in error_str:
                return {"success": False, "error": {"code": "DUPLICATE_PHONE", "message": "This phone number is already registered."}}
            if "transaction_id" in error_str:
                return {"success": False, "error": {"code": "DUPLICATE_TRANSACTION", "message": "This transaction ID has already been used."}}
        return {"success": False, "error": {"code": "SERVER_ERROR", "message": "Something went wrong."}}


@router.get("/register/{registration_id}")
def get_registration_status(registration_id: str):
    response = supabase.table("registrations") \
        .select("registration_id, name, status, event_ids") \
        .eq("registration_id", registration_id) \
        .execute()

    if not response.data:
        return {"success": False, "error": {"code": "NOT_FOUND", "message": "No registration found with this ID."}}

    return {"success": True, "data": response.data[0]}