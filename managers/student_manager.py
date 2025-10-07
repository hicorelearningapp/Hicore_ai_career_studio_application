from .base_manager import BaseManager
from app.models.student import Student
from app.models.student import Course, Project
from app.models.master import MasterCourse, MasterProject

class StudentManager(BaseManager):
    def add_course(self, student_id: int, course_id: str):
        student = self.get_by_id(Student, student_id)
        if not student:
            return None

        master_course = self.db.query(MasterCourse).filter(MasterCourse.course_id == course_id).first()
        if not master_course:
            raise ValueError(f"Course ID '{course_id}' is invalid!")

        existing = self.db.query(Course).filter(
            Course.course_id == course_id, Course.student_id == student_id
        ).first()
        if existing:
            raise ValueError(f"Student already has course '{course_id}'")

        course = Course(course_id=master_course.course_id, course_name=master_course.course_name, student=student)
        self.add(course)
        return {"course_id": course.course_id, "course_name": course.course_name}

    def add_project(self, student_id: int, project_id: str):
        student = self.get_by_id(Student, student_id)
        if not student:
            return None

        master_project = self.db.query(MasterProject).filter(MasterProject.project_id == project_id).first()
        if not master_project:
            raise ValueError(f"Project ID '{project_id}' is invalid!")

        existing = self.db.query(Project).filter(
            Project.project_id == project_id, Project.student_id == student_id
        ).first()
        if existing:
            raise ValueError(f"Student already has project '{project_id}'")

        project = Project(project_id=master_project.project_id, project_name=master_project.project_name, student=student)
        self.add(project)
        return {"project_id": project.project_id, "project_name": project.project_name}

    def list_courses(self, student_id: int):
        student = self.get_by_id(Student, student_id)
        if not student:
            return []
        return [{"course_id": c.course_id, "course_name": c.course_name} for c in student.courses]

    def list_projects(self, student_id: int):
        student = self.get_by_id(Student, student_id)
        if not student:
            return []
        return [{"project_id": p.project_id, "project_name": p.project_name} for p in student.projects]

