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
    address = Column(String(100), nullable=False)
    gender = Column(Boolean)
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
    payments = relationship("Payment", backref="student", lazy=True)


class Class(Base2):
    __tablename__ = 'class'

    grade_id = Column(Integer, ForeignKey('grade.id'), nullable=False)
    student_class = relationship('Student_Class', backref='class', lazy=True)
    subject_teacher_class = relationship('Subject_Teacher_Class', backref='class', lazy=True)
    homeroom_teacher_id = Column(Integer, ForeignKey('teacher.id'), unique=True, nullable=False)
    size = Column(Integer, nullable=False)

    def __str__(self):
        return self.name


class Rule(Base2):
    __tablename__ = 'rule'
    min = Column(Integer, nullable=False)
    max = Column(Integer, nullable=False)

    description = Column(String(50))


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
    fee_class = relationship('Fee_Semester', backref='semester', lazy=True)


class Year(Base1):
    __tablename__ = 'year'

    year = Column(Integer, nullable=False)
    semesters = relationship(Semester, backref='year', lazy=True)

    def __str__(self):
        return self.year


class Fee(Base2):
    __tablename__ = 'fee'
    fee = Column(Integer, nullable=False)
    fee_class = relationship('Fee_Semester', backref='fee', lazy=True)


class Fee_Semester(Base1):
    fee_id = Column(Integer, ForeignKey(Fee.id), nullable=False)
    semester_id = Column(Integer, ForeignKey(Semester.id), nullable=False)
    payments = relationship("Payment", backref="fee_semester", lazy=True)



class Subject(Base2):
    __tablename__ = 'subject'

    subject_teacher = relationship('Subject_Teacher', backref='subject', lazy=True)
    head_teacher = Column(Integer, ForeignKey(Teacher.id), nullable=False, unique=True)

class Payment(Base1):
    student_id = Column(Integer, ForeignKey(Student.id), nullable=False)
    fee_semester_id = Column(Integer, ForeignKey(Fee_Semester.id), nullable=False)
    amount = db.Column(db.Integer)
    bank_code = db.Column(db.String(10))
    order_info = db.Column(db.String(255))
    pay_date = db.Column(db.String(14))
    response_code = db.Column(db.String(2))
    tmn_code = db.Column(db.String(10))
    transaction_no = db.Column(db.String(20))
    transaction_status = db.Column(db.String(2))
    txn_ref = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

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
        per6 = Permission(name='Pay fee', link='pay_fee')
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
            [setper_per1, setper_per2, setper_per3, setper_per4, setper_per5, setper_per6,
             ])
        db.session.commit()

        t1 = Teacher(last_name='Duong', first_name='Huu Thanh', date_of_birth='2000/12/06', email='thanhdt@gmail.com',
                     phone='013525432', username='thanh', password=hashlib.md5('thanh'.encode()).hexdigest(), address='TPHCM', gender=1, degree='Master',
                     setofpermission=1)
        t2 = Teacher(last_name='Ho', first_name='Huong Thien', date_of_birth='1990/12/06', email='thienhhmail.com',
                     phone='012525432', username='thien', password=hashlib.md5('thien'.encode()).hexdigest(), address='TPHCM', gender=1, degree='Master',
                     setofpermission=1)
        t3 = Teacher(last_name='Nguyen Thi', first_name='Phuong Trang', date_of_birth='1990/12/07',
                     email='trangntpmail.com',
                     phone='012528432', username='trang', password=hashlib.md5('trang'.encode()).hexdigest(), address='Nha Trang', gender=0,
                     degree='Master',
                     setofpermission=1)
        db.session.add_all([t1, t2, t3])

        a1 = Admin(last_name='Duong', first_name='Van Khanh', date_of_birth='2003/12/06', email='khanhdv@gmail.com',
                   phone='0123456789', username='khanh', password=hashlib.md5('khanh'.encode()).hexdigest(), address='Ha Noi', gender=1,
                   setofpermission=4)
        db.session.add(a1)
        a2 = Admin(last_name='Duong', first_name='Van Khang', date_of_birth='2003/11/06', email='khangdv@gmail.com',
                   phone='0123456777', username='khang', password=hashlib.md5('khang'.encode()).hexdigest(), address='Da Nang', gender=1,
                   setofpermission=4)
        db.session.add(a2)

        s1 = Student(last_name='Dang', first_name='Trung Thang', date_of_birth='2003/12/07', email='thangdt@gmail.com',
                     phone='0123456788', username='thang', password=hashlib.md5('thang'.encode()).hexdigest(), address='Khanh Hoa', gender=1,
                     setofpermission=2)
        db.session.add(s1)
        s2 = Student(last_name='Dang', first_name='Trung Tien', date_of_birth='2003/12/08', email='tiendt@gmail.com',
                     phone='0123436788', username='tien', password=hashlib.md5('tien'.encode()).hexdigest(), address='Khanh Hoa', gender=1,
                     setofpermission=2)
        db.session.add(s2)

        st1 = Staff(last_name='Cao', first_name='Ngoc Son', date_of_birth='2000/12/05', email='soncn@gmail.com',
                    phone='0123456787', username='son', password=hashlib.md5('son'.encode()).hexdigest(), address='Long An', gender=1, setofpermission=3)
        db.session.add(st1)

        r1 = Rule(name="CLass", min=1, max=40)
        r2 = Rule(name="Age", min=15, max=20)
        r3 = Rule(name="Grade", min=1, max=20)
        r4 = Rule(name="15p", min=1, max=5)
        r5 = Rule(name="1Tiet", min=1, max=3)
        r6 = Rule(name="CuoiKi", min=1, max=1)
        db.session.add_all([r1, r2, r3, r4, r5])

        g1 = Grade(name='10')
        g2 = Grade(name='11')
        g3 = Grade(name='12')
        db.session.add_all([g1, g2, g3])

        y1 = Year(year=2023)
        y2 = Year(year=2024)
        db.session.add_all([y1, y2])

        semes1 = Semester(name='HK1', year_id=1)
        semes2 = Semester(name='HK2', year_id=1)
        db.session.add_all([semes1, semes2])

        typeofscore1 = TypeOfScore(name='15 phut', factor=1)
        typeofscore2 = TypeOfScore(name='1 tiet', factor=2)
        typeofscore3 = TypeOfScore(name='Cuoi ky', factor=3)
        db.session.add_all([typeofscore1, typeofscore2, typeofscore3])

        c1 = Class(name='A1', grade_id=1, homeroom_teacher_id=1, size=30)
        db.session.add(c1)

        s_c1 = Student_Class(student_id=1, class_id=1, semester_id=1)
        s_c2 = Student_Class(student_id=2, class_id=1, semester_id=1)
        db.session.add_all([s_c1, s_c2])

        subject1 = Subject(name='Toan', head_teacher=1)
        subject2 = Subject(name='Ly', head_teacher=2)
        subject3 = Subject(name='Hoa', head_teacher=3)
        db.session.add_all([subject1, subject2, subject3])

        subject_teacher1 = Subject_Teacher(subject_id=1, teacher_id=1)
        subject_teacher2 = Subject_Teacher(subject_id=2, teacher_id=2)
        subject_teacher3 = Subject_Teacher(subject_id=3, teacher_id=3)
        db.session.add_all([subject_teacher1, subject_teacher2, subject_teacher3])

        subject_teacher_class1 = Subject_Teacher_Class(subject_teacher_id=1, class_id=1)
        subject_teacher_class2 = Subject_Teacher_Class(subject_teacher_id=2, class_id=1)
        subject_teacher_class3 = Subject_Teacher_Class(subject_teacher_id=3, class_id=1)
        db.session.add_all([subject_teacher_class1, subject_teacher_class2, subject_teacher_class3])

        score1 = Score(student_class_id=1, subject_teacher_class_id=1, typeofscore_id=1, score=9.5)
        score2 = Score(student_class_id=1, subject_teacher_class_id=1, typeofscore_id=2, score=9.5)
        score3 = Score(student_class_id=1, subject_teacher_class_id=1, typeofscore_id=3, score=9.5)

        score4 = Score(student_class_id=2, subject_teacher_class_id=1, typeofscore_id=1, score=9.5)
        score5 = Score(student_class_id=2, subject_teacher_class_id=1, typeofscore_id=2, score=9.5)
        score6 = Score(student_class_id=2, subject_teacher_class_id=1, typeofscore_id=3, score=9.5)
        db.session.add_all([score1, score2, score3, score4, score5, score6])

        fee1 = Fee(name="BHYT", fee=100000)
        fee2 = Fee(name="Boi bo giao vien", fee='500000')
        f_s1 = Fee_Semester(fee_id=1, semester_id=1)
        f_s2 = Fee_Semester(fee_id=2, semester_id=1)
        db.session.add_all([fee1, fee2, f_s1, f_s2])
        db.session.commit()
