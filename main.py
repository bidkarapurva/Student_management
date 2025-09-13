from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from logging_config import logger
from fastapi import Request
from fastapi import  APIRouter

from dependencies import get_db


from database import Base, engine
from schemas import (
    StudentCreate, StudentResponse,
    CourseCreate, CourseResponse,
    EnrollmentCreate, EnrollmentResponse,
    EnrolledCoursesResponse, UserCreate, UserResponse, Token
)
from crud import (
    create_student, get_student,
    create_course, get_course,
    enroll_student_in_course, get_student_enrolled_courses,
    create_user, get_user_by_username
)

from auth import authenticate_user, create_access_token, get_current_user

app = FastAPI(title="Student Management System")

# Create tables at startup (for development; use Alembic for production)
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# User Registration Endpoint
@app.post("/register/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    return await create_user(db, user)

# User Login Endpoint
@app.post("/login/", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Create Student Endpoint (🔒 Protected)
@app.post("/students/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def create_student_endpoint(
    student: StudentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    return await create_student(db, student)

# Get Student by ID Endpoint (🔒 Protected)
@app.get("/students/{student_id}", response_model=StudentResponse)
async def get_student_endpoint(
    student_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    student = await get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student

# Create Course Endpoint (🔒 Protected)
@app.post("/courses/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course_endpoint(
    course: CourseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    return await create_course(db, course)

# Get Course by ID Endpoint (Protected)
@app.get("/courses/{course_id}", response_model=CourseResponse)
async def get_course_endpoint(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    course = await get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course

# Enroll Student in Course Endpoint (Protected)
@app.post("/enrollments/", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
async def enroll_student_endpoint(
    enrollment: EnrollmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    try:
        return await enroll_student_in_course(db, enrollment)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Get Student's Enrolled Courses Endpoint (Protected)
@app.get("/students/{student_id}/courses/", response_model=EnrolledCoursesResponse)
async def get_student_courses_endpoint(
    student_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    courses = await get_student_enrolled_courses(db, student_id)
    if not courses["enrolled_courses"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No courses found for this student")
    return courses

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Student Management System!"}
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code} for {request.method} {request.url}")
    return response

router = APIRouter()

@router.get("/students/")
async def get_students(db: AsyncSession = Depends(get_db)):
    result = await db.execute("SELECT * FROM students;")
    return result.fetchall()
