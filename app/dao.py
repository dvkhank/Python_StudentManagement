from app.models import Teacher, Student, SetOfPermission, Permission_SetOfPermission, Permission, Admin, \
    Staff, Year, Semester, Class, Grade, Student_Class, Subject_Teacher_Class, Subject_Teacher, Subject, TypeOfScore, \
    Score, Rule
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


def load_student_not_class(semester_id):
    with app.app_context():
        return db.session.query(Student).filter(~Student.id.in_(
            db.session.query(Student.id).
            join(Student_Class, Student_Class.student_id == Student.id).
            filter(Student_Class.semester_id == semester_id)
        )).all()


def load_student_by_class(class_id, semester_id):
    with app.app_context():
        return db.session.query(Student).join(
            Student_Class, Student.id == Student_Class.student_id
        ).filter(
            Student_Class.class_id == class_id,
            Student_Class.semester_id == semester_id
        ).all()


def load_year():
    with app.app_context():
        return Year.query.all()


def load_semester():
    with app.app_context():
        return db.session.query(Semester, Year).filter(Semester.id == Year.id).all()


def load_name_semester(class_id, semester_id):
    with app.app_context():
        Class.query.filter_by(id=class_id).first()


def load_semester():
    with app.app_context():
        return db.session.query(Semester, Year).filter(Semester.year_id == Year.id).all()


def load_classes():
    with app.app_context():
        return db.session.query(Class, Grade).filter(Class.grade_id == Grade.id).all()


def load_rule(rule_id):
    with app.app_context():
        return db.session.query(Rule).filter(Rule.id.__eq__(rule_id)).first()


def get_semester_by_id(semester_id):
    with app.app_context():
        return Semester.query.get(semester_id)


def get_class_by_id(class_id):
    with app.app_context():
        return db.session.query(Grade.name, Class.name).join(Grade, Class.grade_id == Grade.id).filter(
            Class.id == class_id).first()


def add_Student_Class(student_id, class_id, semester_id):
    with app.app_context():
        s_c = Student_Class(student_id=student_id, class_id=class_id, semester_id=semester_id)
        db.session.add(s_c)
        db.session.commit()

def load_class (student_id, class_id, semester_id):
    with app.app_context():
        return db.session.query(Student_Class.id).filter(Student_Class.class_id == class_id,
                                                         Student_Class.student_id == student_id,
                                                         Student_Class.semester_id == semester_id).first()

def load_teacher_in_class(teacher_id, class_id):
    return db.session.query(Subject_Teacher_Class.id). \
        filter(Subject_Teacher.id == Subject_Teacher_Class.id,
               Subject_Teacher.teacher_id == teacher_id, Subject.id == Subject_Teacher.subject_id,
               Subject_Teacher_Class.class_id == class_id).first()

def add_Score(student_class_id, subject_teacher_class_id, typeofscore_id, score):
    score1 = Score(student_class_id=student_class_id, subject_teacher_class_id=subject_teacher_class_id, typeofscore_id=typeofscore_id, score=score)
    db.session.add(score1)
    db.session.commit()


def load_semesters():
    with app.app_context():
        return Semester.query.all()

def count_student():
        return Student.query.count()

def count_teacher():
        return Teacher.query.count()


if __name__ == '__main__':
    with app.app_context():
        print(load_class(1,1,1)[0])