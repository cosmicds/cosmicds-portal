from fastapi import FastAPI, Depends, HTTPException, Query
from pathlib import Path
from typing import List

from sqlmodel import Session, create_engine, select

from .models import Educator, Student, Class, EducatorBase, StudentBase

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{Path(__file__).parent / sqlite_file_name}"

engine = create_engine(sqlite_url, echo=False)

app = FastAPI()


def get_session():
    with Session(engine) as session:
        yield session


@app.get("/hello")
def read_root():
    return {"Hello": "World"}


@app.get("/api/users/{username}")
def get_user(*, session: Session = Depends(get_session), username: str):
    statement = select(Educator).where(
        Educator.username == username)
    results = session.exec(statement).first()

    if results is not None:
        return results

    statement = select(Student).where(
        Student.username == username)
    results = session.exec(statement).first()

    if results is not None:
        return results


@app.get("/api/users/{username}/classes", response_model=List[Class])
def get_user_classes(*, session: Session = Depends(get_session),
                     username: str):
    user = get_user(username=username, session=session)

    return user.classes


@app.post("/api/classes/join")
def add_student_to_class(*, session: Session = Depends(get_session),
                         username: str, class_code: str):
    student = session.exec(select(Student).where(
        Student.username == username)).first()
    class_ = session.exec(select(Class).where(
        Class.code == class_code)).first()

    if class_ is not None:
        student.classes.append(class_)

        session.add(student)
        session.commit()
        session.refresh(student)

        return student


# def check_user_type_defined(username: str) -> bool:
#     return get_user(username) is not None


@app.post("/api/users/create/educator", response_model=EducatorBase)
def create_educator(*, session: Session = Depends(get_session),
                    educator: Educator):
    session.add(educator)
    session.commit()
    session.refresh(educator)

    return educator


@app.post("/api/users/create/student", response_model=StudentBase)
def create_student(*, session: Session = Depends(get_session),
                   student: Student):
    session.add(student)
    session.commit()
    session.refresh(student)

    return student


@app.post("/api/classes/create")
def create_class(*, session: Session = Depends(get_session), username: str,
                 class_: Class):
    educator = session.exec(select(Educator).where(
        Educator.username == username)).first()

    educator.classes.append(class_)

    session.add(class_)
    session.add(educator)
    session.commit()
    session.refresh(class_)
    session.refresh(educator)

    return class_


@app.delete("/api/classes/{code}")
def delete_class(*, session: Session = Depends(get_session), code: str):
    class_ = session.exec(select(Class).where(
        Class.code == code)).first()

    if class_ is not None:
        session.delete(class_)
        session.commit()
