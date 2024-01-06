import enum
import hashlib

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Double
from sqlalchemy.orm import relationship
from app import db, app
from flask_login import UserMixin
from datetime import datetime


class Base1(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class Base2(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)

    def __str__(self):
        return self.name


class User(Base1, UserMixin):
    __tablename__ = 'user'
    __abstract__ = True
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    date_of_birth = Column(DateTime, default=datetime.now())
    email = Column(String(100), nullable=False)
    phone = Column(String(10), nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100),
                    default='https://cdn.tgdd.vn/Files/2016/05/04/824270/tim-hieu-cac-cong-nghe-man-hinh-dien-thoai-5.jpg')
    # phones = relationship(Phone, backref='user', lazy=True)
    active = Column(Boolean, default=True)
    setofpermission = Column(Integer, ForeignKey('setofpermission.id'), nullable=False)

    # phones = relationship('Phone', backref='user')
    def __str__(self):
        return self.first_name


class Student(User):
    __tablename__ = 'student'
    student_class = relationship('Student_Class', backref='student', lazy=True)


class Class(Base2):
    __tablename__ = 'class'

    size = Column(Integer, nullable=False)
    grade_id = Column(Integer, ForeignKey('grade.id'), nullable=False)
    student_class = relationship('Student_Class', backref='class', lazy=True)
    subject_teacher_class = relationship('Subject_Teacher_Class', backref='class', lazy=False)
    homeroom_teacher_id = Column(Integer, ForeignKey('teacher.id'), unique=True, nullable=False)


class Grade(Base2):
    __tablename__ = 'grade'

    classes = relationship(Class, backref='grade', lazy=True)


class Student_Class(Base1):
    __tablename__ = 'student_class'
    student_id = Column(Integer, ForeignKey(Student.id), nullable=False)
    class_id = Column(Integer, ForeignKey(Class.id), nullable=False)
    semester_id = Column(Integer, ForeignKey('semester.id'), nullable=False)
    score = relationship('Score', backref='student_class',
                         lazy=True)


class Teacher(User):
    __tablename__ = 'teacher'
    degree = Column(String(50), nullable=False)
    homeroom_class = relationship('Class', backref='homeroom_teacher', uselist=False)
    subject_teacher = relationship('Subject_Teacher', backref='teacher', lazy=True)
    head_subject = relationship('Subject', backref='teacher', lazy=True)


class Staff(User):
    __tablename__ = 'staff'

    def __str__(self): return self.first_name


class Admin(User):
    __tablename__ = 'admin'


class Semester(Base2):
    __tablename__ = 'semester'

    year_id = Column(Integer, ForeignKey('year.id'), nullable=False)
    students_classes = relationship(Student_Class, backref='semester', lazy=True)


class Year(Base1):
    __tablename__ = 'year'

    year = Column(Integer, nullable=False)
    semesters = relationship(Semester, backref='year', lazy=True)

    def __str__(self):
        return self.year


class Subject(Base2):
    __tablename__ = 'subject'

    subject_teacher = relationship('Subject_Teacher', backref='subject', lazy=True)
    head_teacher = Column(Integer, ForeignKey(Teacher.id), nullable=False, unique=True)


class Subject_Teacher(Base1):
    __tablename__ = 'subject_teacher'
    subject_id = Column(Integer, ForeignKey(Subject.id), nullable=False)
    teacher_id = Column(Integer, ForeignKey(Teacher.id), nullable=False)
    date_joined = Column(DateTime, default=datetime.now())
    subject_teacher_class = relationship('Subject_Teacher_Class', backref='subject_teacher', lazy=False)


class Subject_Teacher_Class(Base1):
    __tablename__ = 'subject_teacher_class'

    subject_teacher_id = Column(Integer, ForeignKey(Subject_Teacher.id), nullable=False)
    class_id = Column(Integer, ForeignKey(Class.id), nullable=False)
    score = relationship('Score', backref='subject_teacher_class', lazy=True)


class Score(Base1):
    __tablename__ = 'score'
    student_class_id = Column(Integer, ForeignKey(Student_Class.id), nullable=False)
    subject_teacher_class_id = Column(Integer, ForeignKey(Subject_Teacher_Class.id), nullable=False)
    score = Column(Double)
    typeofscore_id = Column(Integer, ForeignKey('typeofscore.id'), nullable=False)

    def __str__(self):
        return self.score


class TypeOfScore(Base2):
    __tablename__ = 'typeofscore'
    factor = Column(Double, nullable=False)
    scores = relationship(Score, backref='typeofscore', lazy=True)


class Permission(Base2):
    __tablename__ = 'permission'

    permission_setofpermission = relationship('Permission_SetOfPermission', backref='permission', lazy=True)
    link = Column(String(50), nullable=False)


class SetOfPermission(Base2):
    __tablename__ = 'setofpermission'
    student = relationship('Student', backref='SetOfPermission', lazy=True)
    teacher = relationship('Teacher', backref='SetOfPermission', lazy=True)
    permission_setofpermission = relationship('Permission_SetOfPermission', backref='setofpermission', lazy=True)

    def __str__(self):
        self.name


class Permission_SetOfPermission(Base1):
    __tablename__ = 'permission_setofpermission'
    permission_id = Column(Integer, ForeignKey(Permission.id), nullable=False)
    set_of_permission_id = Column(Integer, ForeignKey(SetOfPermission.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        per1 = Permission(name='Export a score sheet', link='export_scoresheet')
        per2 = Permission(name='Create a score sheet', link='create_scoresheet')
        per3 = Permission(name='Create a class', link='create_class')
        per4 = Permission(name='Create a student', link='create_student')
        per5 = Permission(name='Check results', link='check_results')
        per6 = Permission(name = 'Pay fee', link = 'pay_fee')
        db.session.add_all([per1, per2, per3, per4, per5, per6])
        # db.session.commit()
        setper1 = SetOfPermission(name='Teacher')
        setper2 = SetOfPermission(name='Student')
        setper3 = SetOfPermission(name='Staff')
        setper4 = SetOfPermission(name='Admin')

        db.session.add_all([setper1, setper2, setper3, setper4])
        db.session.commit()

        setper_per1 = Permission_SetOfPermission(permission_id=1, set_of_permission_id=1)
        setper_per2 = Permission_SetOfPermission(permission_id=2, set_of_permission_id=1)
        setper_per3 = Permission_SetOfPermission(permission_id=3, set_of_permission_id=3)
        setper_per4 = Permission_SetOfPermission(permission_id=4, set_of_permission_id=3)
        setper_per5 = Permission_SetOfPermission(permission_id=5, set_of_permission_id=2)
        setper_per6 = Permission_SetOfPermission(permission_id=6, set_of_permission_id=2)

        db.session.add_all(
            [setper_per1, setper_per2, setper_per3, setper_per4, setper_per5, setper_per6])
        db.session.commit()

        t1 = Teacher(last_name='Duong', first_name='Huu Thanh', date_of_birth='2000/12/06', email='thanhdt@gmail.com',
                     phone='013525432', username='thanh', password='thanh', degree='Master',
                     setofpermission=1)
        db.session.add(t1)

        a1 = Admin(last_name='Duong', first_name='Van Khanh', date_of_birth='2003/12/06', email='khanhdv@gmail.com',
                   phone='0123456789', username='khanh', password='khanh', setofpermission=4)
        db.session.add(a1)
        a2 = Admin(last_name='Duong', first_name='Van Khang', date_of_birth='2003/11/06', email='khangdv@gmail.com',
                   phone='0123456777', username='khang', password='khang', setofpermission=4)
        db.session.add(a2)

        s1 = Student(last_name='Dang', first_name='Trung Thang', date_of_birth='2003/12/07', email='thangdt@gmail.com',
                     phone='0123456788', username='thang', password='thang', setofpermission=2)
        db.session.add(s1)

        st1 = Staff(last_name='Cao', first_name='Ngoc Son', date_of_birth='2000/12/05', email='soncn@gmail.com',
                    phone='0123456787', username='son', password='son', setofpermission=3)
        db.session.add(st1)

        db.session.add(a2)
        db.session.commit()