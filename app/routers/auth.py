# app/routers/auth.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.auth_models import AuthRequest, OTPRequest, OTPVerify
from app.models.master import MasterCourse, MasterProject
from app.models.student import Student
from app.models.user import RoleEnum
from app.repositories.user_repository import UserRepository
from app.factories.auth_factory import AuthFactory
from app.database import SessionLocal, engine, Base
from app.schemas.student_schema import StudentCreate, ProjectCreate, CourseCreate
# from app.services.auth.google_service import GoogleAuthService
# from app.services.auth.linkedin_service import LinkedInAuthService
from app.services.auth.otp_service import otp_storage
from managers.student_manager import StudentManager

# Create tables
Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/auth", tags=["Auth"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @router.post("/auth/google")
# def google_login(token: str, role: RoleEnum = RoleEnum.student):
#     repo = UserRepository()
#     auth_service = GoogleAuthService(repo)
#     user = auth_service.login_or_register(role=role, token=token)
#     return {"id": user.id, "email": user.email, "provider": user.provider}

# @router.post("/auth/linkedin")
# def linkedin_login(token: str, role: RoleEnum = RoleEnum.student):
#     repo = UserRepository()
#     auth_service = LinkedInAuthService(repo)
#     user = auth_service.login_or_register(role=role, token=token)
#     return {"id": user.id, "email": user.email, "provider": user.provider}



@router.post("/login-register")
def login_or_register(req: AuthRequest, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    identifier = req.phone or req.email
    service = AuthFactory.get_service(req.provider, repo, identifier)

    if req.provider == "otp" and not req.otp:
        raise HTTPException(status_code=400, detail="OTP required")

    try:
        user = service.login_or_register(
            role=req.role, email=req.email, phone=req.phone, otp=req.otp
        )

        return {
            "message": "Login/Register successful",
            "user": {
                "id": user.id,
                "role": user.role,
                "provider": user.provider,
                "email": user.email,
                "phone": user.phone
            }
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/send-otp")
def send_otp(req: OTPRequest):
    req.validate_contact()
    identifier = req.phone or req.email

    # Use OTPFactory (decides between SMS or Email service)
    from app.factories.otp_factory import OTPFactory
    otp_service = OTPFactory.get_service(identifier)

    otp = otp_service.send_otp(identifier)  # This will trigger Twilio SMS
    return {"message": f"OTP sent to {identifier}"}


@router.post("/verify-otp")
def verify_otp(req: OTPVerify):
    req.validate_contact()
    identifier = req.phone or req.email

    from app.factories.otp_factory import OTPFactory
    otp_service = OTPFactory.get_service(identifier)

    if not otp_service.verify_otp(identifier, req.otp):
        raise HTTPException(status_code=400, detail="Invalid OTP")

    return {"message": f"OTP verified for {identifier}"}


# Seed master tables
@router.on_event("startup")
def seed_master():
    db = SessionLocal()
    if not db.query(MasterCourse).first():
        db.add_all([
            MasterCourse(course_id="C001", course_name="Python Basics"),
            MasterCourse(course_id="C002", course_name="Web Development")
        ])
    if not db.query(MasterProject).first():
        db.add_all([
            MasterProject(project_id="P001", project_name="Portfolio Website"),
            MasterProject(project_id="P002", project_name="Chatbot AI")
        ])
    db.commit()
    db.close()
