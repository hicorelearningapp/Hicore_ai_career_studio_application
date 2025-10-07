from app.models.user import User, RoleEnum
from app.models.student import Student
from app.models.jobseeker import JobSeeker
from app.models.mentor import Mentor
from app.models.employee import Employee
from sqlalchemy.orm import Session

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_by_email_or_phone(self, email: str = None, phone: str = None):
        query = self.db.query(User)
        if email:
            return query.filter(User.email == email).first()
        if phone:
            return query.filter(User.phone == phone).first()
        return None

    def create_user(
        self,
        role: RoleEnum,
        provider: str,
        email: str = None,
        phone: str = None,
        name: str = None,
        college: str = None
    ) -> User:
        # Create the user
        user = User(role=role, provider=provider, email=email, phone=phone)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        # Create role profile
        if role == RoleEnum.student:
            student = Student(
                user_id=user.id,
                name=name or "Anonymous",
                college=college
            )
            self.db.add(student)
        elif role == RoleEnum.jobseeker:
            self.db.add(JobSeeker(user_id=user.id))
        elif role == RoleEnum.mentor:
            self.db.add(Mentor(user_id=user.id))
        elif role == RoleEnum.employee:
            self.db.add(Employee(user_id=user.id))

        self.db.commit()
        return user
