from app.models import Teacher, Student, SetOfPermission, Permission_SetOfPermission, Permission, Admin, \
    Staff, Year,Semester
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

def load_semester(year_id):
    with app.app_context():
        return db.session.query(Semgitester, Year).filter(Semester.id == Year.id, Year.id == year_id).all()