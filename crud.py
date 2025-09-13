from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound, IntegrityError
from models import Student, Course, Enrollment, User
from schemas import StudentCreate, CourseCreate, EnrollmentCreate, UserCreate
from utils import hash_password

# Create Student
async def create_student(db: AsyncSession, student: StudentCreate):
    new_student = Student(**student.dict())
    db.add(new_student)
    try:
        await db.commit()
        await db.refresh(new_student)
        return new_student
    except IntegrityError:
        await db.rollback()
        raise ValueError(f"Student with email '{student.email}' already exists.")

# Get Student by ID
async def get_student(db: AsyncSession, student_id: int):
    result = await db.execute(select(Student).filter(Student.id == student_id))
    student = result.scalars().first()
    if not student:
        raise NoResultFound(f"Student with ID {student_id} not found.")
    return student

# Create Course
async def create_course(db: AsyncSession, course: CourseCreate):
    new_course = Course(**course.dict())
    db.add(new_course)
    try:
        await db.commit()
        await db.refresh(new_course)
        return new_course
    except IntegrityError:
        await db.rollback()
        raise ValueError(f"Course with title '{course.title}' already exists.")

# Get Course by ID
async def get_course(db: AsyncSession, course_id: int):
    result = await db.execute(select(Course).filter(Course.id == course_id))
    course = result.scalars().first()
    if not course:
        raise NoResultFound(f"Course with ID {course_id} not found.")
    return course

# Enroll Student in Course
async def enroll_student_in_course(db: AsyncSession, enrollment: EnrollmentCreate):
    student = await get_student(db, enrollment.student_id)
    course = await get_course(db, enrollment.course_id)

    existing_enrollment = await db.execute(
        select(Enrollment).filter(
            Enrollment.student_id == student.id,
            Enrollment.course_id == course.id
        )
    )
    if existing_enrollment.scalars().first():
        raise ValueError("Student is already enrolled in this course.")

    new_enrollment = Enrollment(student_id=student.id, course_id=course.id)
    db.add(new_enrollment)
    await db.commit()
    await db.refresh(new_enrollment)
    return {"message": "Enrollment successful"}

# Get Student's Enrolled Courses
async def get_student_enrolled_courses(db: AsyncSession, student_id: int):
    await get_student(db, student_id)  # Verify student exists

    result = await db.execute(
        select(Course.id).join(Enrollment).filter(Enrollment.student_id == student_id)
    )
    courses = result.scalars().all()
    return {"enrolled_courses": courses}

# Create User
async def create_user(db: AsyncSession, user: UserCreate):
    try:
        hashed_pw = hash_password(user.password)
        new_user = User(username=user.username, email=user.email, hashed_password=hashed_pw)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except IntegrityError:
        await db.rollback()
        raise ValueError("Username or email already exists.")

# Get User by Username
async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).where(User.username == username))
    return result.scalars().first()
