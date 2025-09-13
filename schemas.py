from pydantic import BaseModel, EmailStr
from typing import List, Optional

# Student Schemas
class StudentCreate(BaseModel):
    name: str
    age: int
    email: EmailStr

class StudentResponse(StudentCreate):
    id: int

    class Config:
        orm_mode = True


# Course Schemas
class CourseCreate(BaseModel):
    title: str
    description: str

class CourseResponse(BaseModel):
    id: int
    title: str
    description: str

    class Config:
        orm_mode = True


# Enrollment Schemas
class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int

class EnrollmentResponse(BaseModel):
    message: str  # Confirmation message for enrollment

    class Config:
        orm_mode = True


# Response for Student's Enrolled Courses
class EnrolledCoursesResponse(BaseModel):
    enrolled_courses: List[int]  # List of enrolled course IDs

    class Config:
        orm_mode = True


# User Schemas
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


# Authentication Schemas
class UserLogin(BaseModel):
    username: str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None
