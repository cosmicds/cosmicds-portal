from .models import Educator, Student, Class
from pathlib import Path

from sqlmodel import Session, create_engine, \
    select
from pathlib import Path

from sqlmodel import Session, create_engine, \
    select

from .models import Educator, Student, Class

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{Path(__file__).parent / sqlite_file_name}"

engine = create_engine(sqlite_url, echo=False)


def get_user(username: str):
    with Session(engine) as session:
        statement = select(Educator).where(
            Educator.username == username)
        results = session.exec(statement).first()

        if results is not None:
            return {**results.dict(), 'type': 'educator'}

        statement = select(Student).where(
            Student.username == username)
        results = session.exec(statement).first()

        if results is not None:
            return {**results.dict(), 'type': 'student'}


def get_educator_classes(username: str):
    with Session(engine) as session:
        educator = session.exec(
            select(Educator).where(Educator.username == username)).first()

        return [x.dict() for x in educator.classes]


def get_student_classes(username: str):
    with Session(engine) as session:
        student = session.exec(
            select(Student).where(Student.username == username)).first()

        return [x.dict() for x in student.classes]


def add_student_to_class(username: str, class_code: str):
    with Session(engine) as session:
        student = session.exec(select(Student).where(
            Student.username == username)).first()
        class_ = session.exec(select(Class).where(
            Class.code == class_code)).first()

        if class_ is not None:
            student.classes.append(class_)

            session.add(student)
            session.commit()
            session.refresh(student)


def check_user_type_defined(username: str) -> bool:
    return get_user(username) is not None


def create_educator(form_data: dict):
    del form_data['confirm_email']
    del form_data['valid']
    form_data['grade_levels'] = ','.join(form_data['grade_levels'])

    try:
        with Session(engine) as session:
            educator = Educator()

            for k, v in form_data.items():
                setattr(educator, k, v)

            session.add(educator)
            session.commit()
            session.refresh(educator)

            return {"ok": True, "error": None}
    except Exception as e:
        return {"ok": False, "error": e}


def create_student(form_data: dict):
    try:
        with Session(engine) as session:
            student = Student()

            for k, v in form_data.items():
                setattr(student, k, v)

            session.add(student)
            session.commit()
            session.refresh(student)

            return {"ok": True, "error": None}
    except Exception as e:
        return {"ok": False, "error": e}


def create_class(username: str, data: dict):
    try:
        with Session(engine) as session:
            educator = session.exec(select(Educator).where(
                Educator.username == username)).first()

            class_ = Class()

            for k, v in data.items():
                setattr(class_, k, v)

            educator.classes.append(class_)

            session.add(class_)
            session.add(educator)
            session.commit()
            session.refresh(class_)
            session.refresh(educator)

            return {"ok": True, "error": None}
    except Exception as e:
        return {"ok": False, "error": e}


def delete_class(code: str):
    with Session(engine) as session:
        class_ = session.exec(select(Class).where(
            Class.code == code)).first()

        if class_ is not None:
            session.delete(class_)
            session.commit()
