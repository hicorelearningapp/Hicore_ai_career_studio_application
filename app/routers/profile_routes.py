from fastapi import APIRouter, Depends, UploadFile, File, Form, Request
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.crud.profile_crud import create_profile, get_profiles, get_profile, update_profile, delete_profile
from app.utils.file_helpers import save_file, model_to_dict

router = APIRouter(prefix="/profiles", tags=["Profiles"])

@router.post("/")
async def api_create_profile(
    request: Request,
    db: Session = Depends(get_db),
    # form fields
    first_name: Optional[str] = Form(None),
    last_name: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    mobile_number: Optional[str] = Form(None),
    professional_title: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    professional_bio: Optional[str] = Form(None),
    job_alerts: Optional[bool] = Form(False),
    linkedin_profile: Optional[str] = Form(None),
    portfolio_website: Optional[str] = Form(None),
    github_profile: Optional[str] = Form(None),
    job_titles: Optional[str] = Form(None),
    work_type: Optional[str] = Form(None),
    current_salary: Optional[str] = Form(None),
    expected_salary: Optional[str] = Form(None),
    availability_start: Optional[str] = Form(None),
    relocate: Optional[bool] = Form(False),
    remote: Optional[bool] = Form(False),
    hybrid: Optional[bool] = Form(False),
    company_name: Optional[str] = Form(None),
    job_title: Optional[str] = Form(None),
    job_location: Optional[str] = Form(None),
    start_date: Optional[str] = Form(None),
    end_date: Optional[str] = Form(None),
    currently_working: Optional[bool] = Form(False),
    responsibilities: Optional[str] = Form(None),
    skills: Optional[str] = Form(None),
    education_level: Optional[str] = Form(None),
    field_of_study: Optional[str] = Form(None),
    college_name: Optional[str] = Form(None),
    edu_start_year: Optional[str] = Form(None),
    edu_end_year: Optional[str] = Form(None),
    currently_studying: Optional[bool] = Form(False),
    resume_skills: Optional[str] = Form(None),
    certificate_name: Optional[str] = Form(None),
    issuing_org: Optional[str] = Form(None),
    issue_date: Optional[str] = Form(None),
    expiry_date: Optional[str] = Form(None),
    credential_url: Optional[str] = Form(None),
    project_name: Optional[str] = Form(None),
    technologies: Optional[str] = Form(None),
    project_description: Optional[str] = Form(None),
    project_link: Optional[str] = Form(None),
    profile_image: Optional[UploadFile] = File(None),
    resume_file: Optional[UploadFile] = File(None),
    project_image: Optional[UploadFile] = File(None)
):
    try:
        # JSON request
        if request.headers.get("content-type", "").startswith("application/json"):
            data = await request.json()
        else:  # FormData
            data = dict(
                first_name=first_name,
                last_name=last_name,
                email=email,
                mobile_number=mobile_number,
                professional_title=professional_title,
                location=location,
                professional_bio=professional_bio,
                job_alerts=job_alerts,
                linkedin_profile=linkedin_profile,
                portfolio_website=portfolio_website,
                github_profile=github_profile,
                job_titles=job_titles,
                work_type=work_type,
                current_salary=current_salary,
                expected_salary=expected_salary,
                availability_start=availability_start,
                relocate=relocate,
                remote=remote,
                hybrid=hybrid,
                company_name=company_name,
                job_title=job_title,
                job_location=job_location,
                start_date=start_date,
                end_date=end_date,
                currently_working=currently_working,
                responsibilities=responsibilities,
                skills=skills,
                education_level=education_level,
                field_of_study=field_of_study,
                college_name=college_name,
                edu_start_year=edu_start_year,
                edu_end_year=edu_end_year,
                currently_studying=currently_studying,
                resume_skills=resume_skills,
                certificate_name=certificate_name,
                issuing_org=issuing_org,
                issue_date=issue_date,
                expiry_date=expiry_date,
                credential_url=credential_url,
                project_name=project_name,
                technologies=technologies,
                project_description=project_description,
                project_link=project_link,
                profile_image=save_file(profile_image),
                resume_file=save_file(resume_file),
                project_image_url=save_file(project_image)
            )
        profile = create_profile(db, data)
        return model_to_dict(profile)
    except Exception as e:
        return {"error": str(e)}

@router.get("/")
def api_list_profiles(db: Session = Depends(get_db)):
    profiles = get_profiles(db)
    return [model_to_dict(p) for p in profiles]

@router.get("/{profile_id}")
def api_get_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = get_profile(db, profile_id)
    return model_to_dict(profile)

@router.put("/{profile_id}")
async def api_update_profile(profile_id: int, request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    profile = update_profile(db, profile_id, data)
    return model_to_dict(profile)

@router.delete("/{profile_id}")
def api_delete_profile(profile_id: int, db: Session = Depends(get_db)):
    return delete_profile(db, profile_id)
