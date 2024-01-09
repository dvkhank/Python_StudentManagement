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


@app.route('/create_scoresheet', methods=['get'])
def create_scoresheet():
    teacher_id = current_user.id
    classes = dao.load_class(teacher_id)
    class_id = request.args.get('class')
    students = dao.load_student_by_class_id(class_id, teacher_id)
    subject = dao.load_teacher_subject(teacher_id)
    type_of_score = dao.load_type_of_score()
    # if request.method.__eq__('POST'):
    #     teacher_id = current_user.id
    #     score_type = request.form.get('score_type')  # Lấy loại điểm từ form
    #     scores = request.form.to_dict()  # Lấy tất cả dữ liệu từ form
    #
    #     for key, value in scores.items():
    #         if key.startswith('score_'):
    #             student_id = key.split('_')[1]  # Lấy ID của học sinh từ tên trường
    #             # Tạo hoặc cập nhật điểm số cho học sinh với loại điểm tương ứng
    #             score = Score.query.filter_by(student_id=student_id, type=score_type).first()
    #             if score:
    #                 score.score_value = float(value)  # Cập nhật điểm số nếu đã tồn tại
    #             else:
    #                 new_score = Score(student_id=student_id, type=score_type, score_value=float(value))
    #                 db.session.add(new_score)  # Tạo điểm số mới nếu chưa tồn tại trong cơ sở dữ liệu

    return render_template('create_scoresheet.html', classes=classes, students=students, subject=subject,
                           type_of_score=type_of_score)


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
    return render_template('create_student.html', students=students_list)


@app.route("/create_class", methods=['post', 'get'])
def create_class():
    students_list = dao.load_student()
    year_list = dao.load_year()
    semester_list = dao.load_semester()
    return render_template('create_class.html', students=students_list, years=year_list, semesters=semester_list)


# @app.route("/create_class/<int:year_id>", methods=['post', 'get'])
# def create_class():
#     students_list = dao.load_student()
#     year_list = dao.load_year()
#     semester_list = dao.load_semester()
#     return render_template('create_class.html', students = students_list, years = year_list, semesters = semester_list )


# @app.context_processor
# def common_response():
#     permission_id = None
#     if permission_id:
#         permission = dao.load_permission(permission_id)
#         return {"permission": permission}


if __name__ == '__main__':
    from app import admin

    app.run(debug=True)
