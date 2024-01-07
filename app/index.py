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
        dao.add_student(last_name=last_name, first_name=first_name, date_of_birth= date_of_birth, email=email, phone= phone, username = username, password= password, address= hometown, gender= int(gender))
    return render_template('create_student.html',students = students_list )

@app.route("/create_class/<int:year_id>", methods=['post', 'get'])
def create_class():
    students_list = dao.load_student()
    year_list = dao.load_year()
    year_id = request.get.form('year')
    if year_list:
        semester_list = dao.load_semester(year_id)
    return render_template('create_class.html', students = students_list, years = year_list, semesters = semester_list )



# @app.context_processor
# def common_response():
#     permission_id = None
#     if permission_id:
#         permission = dao.load_permission(permission_id)
#         return {"permission": permission}


if __name__ == '__main__':
    from app import admin

    app.run(debug=True)
