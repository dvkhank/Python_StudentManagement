import math
from functools import wraps

from flask import render_template, request, redirect, jsonify, url_for, session
import dao
from app import app, login
from flask_login import login_user, logout_user, login_required, current_user


@app.route("/")
def index():
    if not current_user.is_authenticated:
        return redirect(url_for("user_login"))
    else:
        set_of_permission_id = session['set_of_permission_id']
        list_of_permission = dao.load_permission(set_of_permission_id=set_of_permission_id)
    return render_template("index.html", list_of_permission=list_of_permission)


@app.route("/user_login", methods=['post', 'get'])
def user_login():
    error_message = None
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        set_of_permission = request.form.get('set_of_permission')
        user = dao.auth_user(username=username, password=password, set_of_permission=set_of_permission)
        if user:
            login_user(user)
            session['set_of_permission_id'] = user.setofpermission
            if user.setofpermission in (1, 2, 3):
                return redirect(url_for("index"))
            else:
                return redirect('/admin')
        else:
            error_message = 'There is no user like that'
    set_of_permission = dao.load_setofpermission()
    return render_template("user_login.html", set_of_permission=set_of_permission, error_message=error_message)


@app.route('/create_scoresheet', methods=['get', 'post'])
def create_scoresheet():
    student_id_add = 0
    if request.args.get("student_id_add"):
        student_id_add = request.args.get("student_id_add")


    students_list = {}
    semester_list = dao.load_semester()
    classes_list = dao.load_classes()
    class_id = request.args.get("classes")
    semester_id = request.args.get("semester")
    teacher_in_class = dao.load_teacher_in_class(teacher_id=current_user.id, class_id=class_id)
    rule_15p = dao.load_rule(4)
    if class_id and semester_id and teacher_in_class:
        session["class_id"] = class_id
        session["semester"] = semester_id
        students_list = dao.load_student_by_class(class_id=int(class_id),
                                                  semester_id=int(semester_id))
    return render_template('create_scoresheet.html', semester=semester_list, classes=classes_list,
                           student_list=students_list, rule_15p=rule_15p, student_id_add=student_id_add)


@app.route('/create_scoresheet/add', methods=['get', 'post'])
def create_scoresheet_add():
    stu_id = request.args.get("student_id_add")
    class_id = session["class_id"]
    semester_id = session["semester"]

    rule_15p = dao.load_rule(4)
    rule_1tiet = dao.load_rule(5)
    rule_cuoiki = dao.load_rule(6)

    if stu_id:
        student = dao.get_user_by_id(stu_id, 2)

    if request.method.__eq__('POST'):
        score15p = request.form.getlist("score15p")
        score1tiet = request.form.getlist("score1tiet")
        scorecuoiki = request.form.get("scorecuoiki")
        student_id = request.form.get("student_id")
        for s in score15p:
            dao.add_Score(
                student_class_id=dao.load_class(student_id=int(student_id), class_id=class_id, semester_id=semester_id)[
                    0],
                subject_teacher_class_id=dao.load_teacher_in_class(teacher_id=current_user.id, class_id=int(class_id))[
                    0],
                typeofscore_id=1, score=float(s))
        for s in score1tiet:
            dao.add_Score(
                student_class_id=dao.load_class(student_id=int(student_id), class_id=class_id, semester_id=semester_id)[
                    0],
                subject_teacher_class_id=dao.load_teacher_in_class(teacher_id=current_user.id, class_id=int(class_id))[
                    0],
                typeofscore_id=2, score=float(s))
        dao.add_Score(
            student_class_id=dao.load_class(student_id=int(student_id), class_id=class_id, semester_id=semester_id)[
                0],
            subject_teacher_class_id=dao.load_teacher_in_class(teacher_id=current_user.id, class_id=int(class_id))[
                0],
            typeofscore_id=3, score=float(scorecuoiki))
    return render_template("add_create_scoresheet.html",student = student, rule_15p=rule_15p, rule_1tiet= rule_1tiet)


@app.route('/admin/login', methods=['post'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')
    session['set_of_permission_id'] = 4

    user = dao.auth_user(username=username, password=password, set_of_permission='4')
    if user:
        login_user(user)
        print(user)

    return redirect('/admin')


@app.route("/user_logout")
def user_logout():
    logout_user()
    if 'set_of_permission_id' in session:
        del session['set_of_permission_id']
    return redirect(url_for("user_login"))


# @app.route("/admin/login", methods=['post'])
# def admin_login():
#     username = request.form.get("username")
#     password = request.form.get("password")
#     user = dao.auth_user(username=username, password=password, set_of_permission_id = 4)
#     if admin:
#         login_user(user)
#         print(admin)
#     return redirect("/admin")


@app.route("/profile")
def profile_user():
    set_of_permission_id = session['set_of_permission_id']
    if current_user.is_authenticated:
        user = dao.get_user_by_id(current_user.id, set_of_permission_id)
    return render_template('profile.html', user=user)


@app.route("/pay_fee")
def pay_fee():
    semester = dao.load_semester()
    if request.method == 'POST':
        year = request.form.get()

    return render_template('pay_fee.html', semester=semester)


@login.user_loader
def load_user(user_id):
    set_of_permission_id = session['set_of_permission_id']
    user = dao.get_user_by_id(user_id, set_of_permission_id)
    return user


@app.route("/create_student", methods=['post', 'get'])
def create_student():
    students_list = dao.load_student()
    rule_age = dao.load_rule(2)
    if request.method.__eq__('POST'):
        last_name = request.form.get("last_name")
        first_name = request.form.get("first_name")
        date_of_birth = request.form.get("date_of_birth")
        hometown = request.form.get("hometown")
        email = request.form.get("email")
        phone = request.form.get('phone')
        username = request.form.get('username')
        password = request.form.get("password")
        gender = request.form.get("gender_student")
        dao.add_student(last_name=last_name, first_name=first_name, date_of_birth=date_of_birth, email=email,
                        phone=phone, username=username, password=password, address=hometown, gender=int(gender))
    return render_template('create_student.html', students=students_list, rule_age= rule_age)


@app.route("/create_class", methods=['post', 'get'])
def create_class():
    semester_list = dao.load_semester()
    classes_list = dao.load_classes()
    rule_class = dao.load_rule(1)
    class_id = request.args.get("classes")
    semester_id = request.args.get("semester")
    if class_id and semester_id:
        students_list = dao.load_student_by_class(class_id=int(class_id), semester_id=int(semester_id))
        session["class_id"] = class_id
        session["semester_id"] = semester_id
    else:
        students_list = dao.load_student_by_class(class_id=1, semester_id=1)
    return render_template('/create_class.html'
                           , students=students_list, semester=semester_list
                           , classes=classes_list, rules=rule_class, class_id=class_id, semester_id=semester_id)


@app.route("/create_class/add", methods=['post', 'get'])
def add_student_class():
    class_id = session["class_id"]
    semester_id = session["semester_id"]
    rule_class = dao.load_rule(1)
    class_name = dao.get_class_by_id(class_id)
    semester_name = dao.get_semester_by_id(semester_id)
    stu_add = request.args.get("stu_add")
    if stu_add:
        dao.add_Student_Class(stu_add, class_id, semester_id)
    if class_id and semester_id:
        students_list = dao.load_student_by_class(class_id=int(class_id), semester_id=int(semester_id))
        students_add_list = dao.load_student_not_class(semester_id)

    return render_template("/add_student_class.html", class_name=class_name, semester_name=semester_name,
                           rules=rule_class, students=students_list, students_add=students_add_list)


# @app.context_processor
# def common_response():
#     permission_id = None
#     if permission_id:
#         permission = dao.load_permission(permission_id)
#         return {"permission": permission}


if __name__ == '__main__':
    from app import admin

    app.run(debug=True)