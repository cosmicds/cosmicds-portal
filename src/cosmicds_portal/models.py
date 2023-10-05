from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


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
    date: str
    stories: str
    code: str
    educators: List["Educator"] = Relationship(back_populates="classes",
                                               link_model=EducatorClassLink)
    students: List["Student"] = Relationship(back_populates="classes",
                                             link_model=StudentClassLink)


class EducatorBase(SQLModel):
    username: str
    verified: bool = Field(default=False)
    first_name: str
    last_name: str
    email: str
    school_name: str
    school_zip: str
    grade_levels: str
    classes_taught: str


class Educator(EducatorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    classes: List[Class] = Relationship(back_populates="educators",
                                        link_model=EducatorClassLink)


class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    classes: List[Class] = Relationship(back_populates="students",
                                        link_model=StudentClassLink)

# if __name__ == "__main__":
#     SQLModel.metadata.create_all(engine)
