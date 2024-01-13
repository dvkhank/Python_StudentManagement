import hashlib
import math
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import wraps
from random import randint

from flask import render_template, request, redirect, jsonify, url_for, session, flash
import dao, utils, vnpay
from app import app, login
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime


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


def calculate_average_scores(score15p, score1tiet, scorecuoiki):
    score15p = [float(score) for score in score15p]
    score1tiet = [float(score) for score in score1tiet]
    scorecuoiki = float(scorecuoiki)

    # Tính điểm trung bình cho từng cột
    average_15p = sum(score15p) / len(score15p) if len(score15p) > 0 else 0
    average_1tiet = sum(score1tiet) / len(score1tiet) if len(score1tiet) > 0 else 0
    average_cuoiki = scorecuoiki

    return average_15p, average_1tiet, average_cuoiki


@app.route('/create_scoresheet/add', methods=['get', 'post'])
def create_scoresheet_add():
    stu_id = request.args.get("student_id_add")
    class_id = session["class_id"]
    semester_id = session["semester"]

    rule_15p = dao.load_rule(4)
    rule_1tiet = dao.load_rule(5)
    rule_cuoiki = dao.load_rule(6)
    average_15p, average_1tiet, average_cuoiki = 0, 0, 0

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
        average_15p, average_1tiet, average_cuoiki = calculate_average_scores(score15p, score1tiet, scorecuoiki)
    return render_template("add_create_scoresheet.html",
                           student=student, rule_15p=rule_15p, rule_1tiet=rule_1tiet,
                           average_15p=average_15p, average_1tiet=average_1tiet, average_cuoiki=average_cuoiki)


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


@app.route("/api/fee", methods=['post'])
def add_fee():
    """
    "fee": {
    "1" {
    "id" : "1",
    "name" : "ABC",
    "fee" : "500000"
        }, "2" {
    "id" : "2",
    "name" : "DEF",
    "fee" : "900000"
        }
    }

    :return:
    """
    fee = session.get('fee')

    data = request.json
    if fee is None:
        fee = {}
    id = str(data.get("id"))
    fee[id] = {
        "id": id,
        "name": data.get("name"),
        "fee": data.get("fee")
    }
    session["fee"] = fee
    print(fee)
    return jsonify(utils.count_fee(fee))


@app.route("/pay_fee", methods=['post', 'get'])
def pay_fee():
    semester = dao.load_semester()
    if request.method == 'GET':
        chosen_semester = request.args.get('semester')
        fees = dao.load_fee(chosen_semester)

    return render_template('pay_fee.html', semester=semester, fees=fees)


VNPAY_TERMINAL_ID = 'A18060DP'
VNPAY_HASH_SECRET_KEY = 'PASLWDWBAGFDSQZJOSREVQQGGEZDZNGX'
VNPAY_TEST_URL = 'https://sandbox.vnpayment.vn/paymentv2/vpcpay.html'
import logging


@app.route('/payment', methods=['POST'])
def payment():
    if request.method == 'POST':
        total = int(request.form.get('totalAmount'))
        info = "Thanh toan hoc phi"
        order_type = "Hoc phi"

        # Thay thế bằng thông tin cụ thể của bạn
        tmn_code = VNPAY_TERMINAL_ID
        hash_secret_key = VNPAY_HASH_SECRET_KEY
        test_url = VNPAY_TEST_URL

        # Khởi tạo class VNPAY với thông tin cần thiết
        vnp = vnpay.VNPAY(tmn_code, hash_secret_key, test_url)

        # Set thông tin đơn hàng
        vnp.set_order_info(total, info, order_type, 'http://127.0.0.1:5000/pay_fee')

        # Lấy URL thanh toán
        vnpay_payment_url = vnp.get_payment_url()

        print(total)
        print(vnpay_payment_url)

        # Chuyển hướng đến VNPAY
        return redirect(vnpay_payment_url)
    else:
        return render_template("payment.html", title="Thanh toán")


@app.route('/vnpay_return', methods=['GET'])
def vnpay_return():
    # Xử lý kết quả trả về từ VNPay
    # Đọc và kiểm tra chữ ký hash
    vnpay_data = request.args.to_dict()
    secure_hash = vnpay_data.pop('vnp_SecureHash', None)
    secure_hash_type = vnpay_data.pop('vnp_SecureHashType', None)

    # Sắp xếp dữ liệu theo key để tạo chuỗi hash
    sorted_data = sorted(vnpay_data.items())
    hash_data = "&".join(f"{key}={value}" for key, value in sorted_data)

    # Kiểm tra chữ ký hash
    computed_hash = hashlib.sha256(f"{VNPAY_HASH_SECRET_KEY}&{hash_data}".encode('utf-8')).hexdigest()

    if secure_hash == computed_hash:
        # Chữ ký hợp lệ, xử lý thông tin thanh toán ở đây
        return "Thanh toán thành công!"
    else:
        # Chữ ký không hợp lệ, xử lý lỗi ở đây
        return "Lỗi xác thực chữ ký hash!"


# # Xử lý IPN URL
# @app.route('/payment_ipn', methods=['GET'])
# def payment_ipn():
#     selected_fee_ids = request.args.getlist('selected_fees[]')
#     if selected_fee_ids:
#
#         vnp.responseData = selected_fee_ids
#         # ...Xử lý dữ liệu và kiểm tra chữ ký
#         if vnp.validate_response(VNPAY_HASH_SECRET_KEY):
#             # Xử lý kết quả thanh toán và cập nhật vào Database
#             # ...
#             return jsonify({'RspCode': '00', 'Message': 'Confirm Success'})
#         else:
#             return jsonify({'RspCode': '97', 'Message': 'Invalid Signature'})
#     else:
#         return jsonify({'RspCode': '99', 'Message': 'Invalid request'})
#
#
# # Xử lý ReturnURL
# @app.route('/payment_return', methods=['GET'])
# def payment_return():
#     selected_fee_ids = request.form.getlist('selected_fees[]')
#
#     if selected_fee_ids:
#         vnp.responseData = selected_fee_ids
#         # ...Xử lý dữ liệu và kiểm tra chữ ký
#         if vnp.validate_response(VNPAY_HASH_SECRET_KEY):
#             # Hiển thị thông tin kết quả thanh toán cho khách hàng
#             # Truyền thêm thông tin về các học phí đã chọn vào template
#             return render_template("payment_return.html", title="Kết quả thanh toán", result="Thành công",
#                                    order_id=1, amount=1, selected_fee_ids=selected_fee_ids)
#         else:
#             return render_template("payment_return.html", title="Kết quả thanh toán", result="Lỗi", msg="Sai checksum")
#     else:
#         return render_template("payment_return.html", title="Kết quả thanh toán")


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
    return render_template('create_student.html', students=students_list, rule_age=rule_age)


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


def generate_otp():
    length = 6
    otp = ''
    for _ in range(length):
        otp += str(randint(0, 9))

    return otp


def verify_otp(otp, user_otp):
    if str(otp).__eq__(str(user_otp)):
        return True
    return False


def send_otp_email(email, otp):
    myemail = '2151050187khanh@ou.edu.vn'
    mypassword = '079203035064'

    connection = smtplib.SMTP("smtp.gmail.com", 587)
    connection.starttls()
    connection.login(user=myemail, password=mypassword)

    message = MIMEMultipart()
    message['From'] = myemail
    message['To'] = email
    message['Subject'] = "Your OTP"  # Chủ đề của email
    body = f"Your OTP is: {otp}"
    message.attach(MIMEText(body, 'plain'))

    connection.send_message(message)
    connection.quit()


@app.route('/forget_pass', methods=['POST', 'GET'])
def forget_pass():
    set_of_permission = dao.load_setofpermission()
    if request.method == 'POST':
        setofpermission = request.form.get('set_of_permission')
        session['setofpermission'] = setofpermission
        username = request.form.get('username')
        if username:
            user = dao.get_user_by_username(username, int(setofpermission))
            print(user)

            if user:
                user_mail = user.email
                ma_otp = generate_otp()
                send_otp_email(user_mail, ma_otp)
                session['username'] = username
                session['ma_otp'] = ma_otp

                return redirect(url_for('confirm_otp'))

    return render_template('forget_pass.html', set_of_permission=set_of_permission)


@app.route('/confirm-otp', methods=['POST', 'GET'])
def confirm_otp():
    ma_otp = session['ma_otp']
    if request.method == 'POST':
        user_otp = request.form.get('otp')
        is_valid = verify_otp(ma_otp, user_otp)
        if is_valid:
            return redirect(url_for('change_password'))

        error_message = 'Invalid OTP. Please try again.'
        return render_template('confirm_otp.html', error_message=error_message)

    # Nếu là method GET, hiển thị form xác nhận OTP
    return render_template('confirm_otp.html')


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    username = session.get('username')
    setofpermission = int(session['setofpermission'])
    error_message = None
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if new_password.strip() == confirm_password.strip():
            dao.change_user_password(username=username, new_password=new_password, setofpermission=setofpermission)
            flash('Password changed successfully', 'success')
            return redirect(url_for('user_login'))
        else:
            error_message = 'Passwords do not match. Please try again.'
    return render_template('change_password.html', username=username,error_message=error_message)


# @app.context_processor
# def common_response():
#     permission_id = None
#     if permission_id:
#         permission = dao.load_permission(permission_id)
#         return {"permission": permission}


if __name__ == '__main__':
    from app import admin

    app.run(debug=True)
