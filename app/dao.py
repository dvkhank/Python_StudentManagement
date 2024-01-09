from app.models import Teacher, Student, SetOfPermission, Permission_SetOfPermission, Permission, Admin, \
    Staff, Year, Semester, Class, Grade, Student_Class, Subject_Teacher_Class, Subject_Teacher, Subject, TypeOfScore, Score
from app import app, db
import hashlib


def get_user_by_id(user_id, set_of_permission_id):
    if set_of_permission_id == 1:
        return Teacher.query.get(user_id)
    if set_of_permission_id == 2:
        return Student.query.get(user_id)
    if set_of_permission_id == 3:
        return Staff.query.get(user_id)
    if set_of_permission_id == 4:
        return Admin.query.get(user_id)


def load_permission(set_of_permission_id):
    permission = db.session.query(Permission, SetOfPermission, Permission_SetOfPermission).filter(
        Permission.id == Permission_SetOfPermission.permission_id,
        SetOfPermission.id == Permission_SetOfPermission.set_of_permission_id,
        SetOfPermission.id == set_of_permission_id
    ).all()
    return permission


def load_class(teacher_id):
    return db.session.query(Class, Grade, Subject_Teacher_Class).filter(Grade.id == Class.grade_id,
                                                                        Subject_Teacher_Class.class_id == Class.id,
                                                                        Subject_Teacher_Class.subject_teacher_id == teacher_id).all()


def load_student_by_class_id(class_id, teacher_id):
    return db.session.query(Class, Student, Student_Class, Subject_Teacher_Class, Subject_Teacher).filter(
        Student_Class.student_id == Student.id,
        Student_Class.class_id == Class.id,
        Class.id == class_id,
        Subject_Teacher_Class.class_id == Class.id,
        Subject_Teacher_Class.subject_teacher_id == Subject_Teacher.id,
        Subject_Teacher.teacher_id == teacher_id
    ).all()


def load_teacher_subject(teacher_id):
    return db.session.query(Subject_Teacher, Teacher, Subject).filter(
        Subject_Teacher.teacher_id == Teacher.id,
        Subject_Teacher.subject_id == Subject.id,
        Teacher.id == teacher_id,
    ).first()

def load_type_of_score():
    return TypeOfScore.query.all()

def add_score(teacher_id, score, typeofscore_id):
    score = Score()




def load_setofpermission():
    return SetOfPermission.query.all()


def auth_user(username, password, set_of_permission):
    with app.app_context():
        if set_of_permission == '1':
            return Teacher.query.filter(Teacher.username.__eq__(username),
                                        Teacher.password.__eq__(password)).first()
        if set_of_permission == '2':
            return Student.query.filter(Student.username.__eq__(username),
                                        Student.password.__eq__(password)).first()
        if set_of_permission == '3':
            return Staff.query.filter(Staff.username.__eq__(username),
                                      Staff.password.__eq__(password)).first()
        if set_of_permission == '4':
            return Admin.query.filter(Admin.username.__eq__(username),
                                      Admin.password.__eq__(password)).first()


def auth_admin(username, password):
    with app.app_context():
        return Admin.query.filter(Admin.username.__eq__(username),
                                  Admin.password.__eq__(password)).first()


def add_student(last_name, first_name, date_of_birth, email, phone, username, password, address, gender):
    with app.app_context():
        student = Student(last_name=last_name, first_name=first_name, date_of_birth=date_of_birth, email=email,
                          phone=phone, username=username, password=password, address=address, gender=gender,
                          setofpermission=2)
        db.session.add(student)
        db.session.commit()


def load_student():
    with app.app_context():
        return Student.query.all()


def load_year():
    with app.app_context():
        return Year.query.all()


def load_semester():
    with app.app_context():
        return db.session.query(Semester, Year).filter(Semester.id == Year.id).all()
