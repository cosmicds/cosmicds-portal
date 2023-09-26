from typing import List, Optional

from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, \
    select
from pathlib import Path


class StudentClassLink(SQLModel, table=True):
    student_id: Optional[int] = Field(
        default=None, foreign_key="student.id", primary_key=True
    )
    class_id: Optional[int] = Field(
        default=None, foreign_key="class.id", primary_key=True
    )


class EducatorClassLink(SQLModel, table=True):
    educator_id: Optional[int] = Field(
        default=None, foreign_key="educator.id", primary_key=True
    )
    class_id: Optional[int] = Field(
        default=None, foreign_key="class.id", primary_key=True
    )


class Class(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    educators: List["Educator"] = Relationship(back_populates="classes",
                                               link_model=EducatorClassLink)
    students: List["Student"] = Relationship(back_populates="classes",
                                             link_model=StudentClassLink)


class Educator(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    classes: List[Class] = Relationship(back_populates="educators",
                                        link_model=EducatorClassLink)
    verified: bool = Field(default=False)


class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    classes: List[Class] = Relationship(back_populates="students",
                                        link_model=StudentClassLink)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{Path(__file__).parent / sqlite_file_name}"

engine = create_engine(sqlite_url, echo=False)


# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)
#
#
# def create_course():
#     with Session(engine) as session:
#         test_class = Class(name="AP Test Class")
#         test_educator = Educator(username="test_educator",
#                                  classes=[test_class])
#         test_student = Student(username="test_student", classes=[test_class])
#
#         session.add(test_educator)
#         session.add(test_student)
#         session.commit()
#
#         session.refresh(test_educator)
#         session.refresh(test_student)
#
#         print("Educator:", test_educator)
#         print("Educator classes:", test_educator.classes)
#         print("Student:", test_student)
#         print("Student classes:", test_student.classes)
#
#
# def select_educators():
#     with Session(engine) as session:
#         statement = select(Educator).where(Educator.id == 1)
#         results = session.exec(statement)
#         for hero in results:
#             print(hero)
#
#
# def main():
#     create_db_and_tables()
#     create_course()
#     select_educators()


def get_user_type(username: str) -> str:
    user_type = None

    with Session(engine) as session:
        statement = select(Educator).where(
            Educator.username == username)
        results = session.exec(statement)

        if results.first() is not None:
            user_type = 'educator'

        statement = select(Student).where(
            Student.username == username)
        results = session.exec(statement)

        if results.first() is not None:
            user_type = 'student'

    return user_type


def check_user_type_defined(username: str) -> bool:
    return get_user_type(username) is not None

# if __name__ == "__main__":
#     main()
