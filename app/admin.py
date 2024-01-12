from app import app, db
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import logout_user, current_user
from flask_admin.form import rules
from wtforms import FileField, validators
from wtforms.validators import DataRequired
from flask import render_template, request, redirect, jsonify, url_for, session
from app.models import Student, Teacher, Subject, Staff, Grade, Score
import dao


class MyAdmin(AdminIndexView):
    @expose('/')
    def index(self):
        students = dao.count_student()
        teachers = dao.count_teacher()
        year_list = dao.load_year()
        semester_list = dao.load_semester()
        return self.render('admin/index.html', students=students, teachers=teachers)

admin = Admin(app=app, name="STUDENT MANAGEMENT", template_mode='bootstrap4', index_view=MyAdmin())



class CustomUserView(ModelView):
    column_editable_list = ['phone', 'email']
    column_list = ['last_name', 'first_name', 'date_of_birth', 'email', 'phone',
                   'active', 'gender']
    column_searchable_list = ['first_name', 'first_name']
    column_filters = ['last_name', 'first_name', 'active', 'setofpermission']
    form_args = dict(
        last_name=dict(validators=[DataRequired(), validators.Length(max=100)],
                       render_kw={
                           'placeholder': 'Last name...'
                       }),
        first_name=dict(validators=[DataRequired(), validators.Length(max=100)],
                        render_kw={
                            'placeholder': 'First name...'
                        }),
        email=dict(validators=[DataRequired(), validators.Length(max=100)],
                   render_kw={
                       'placeholder': 'Email...'
                   }),
        phone=dict(validators=[DataRequired(), validators.Length(max=11)],
                   render_kw={
                       'placeholder': 'Phone...'
                   }),
        username=dict(validators=[DataRequired(), validators.Length(max=100)],
                      render_kw={
                          'placeholder': 'User name...'
                      }),
        password=dict(validators=[DataRequired(), validators.Length(max=100)],
                      render_kw={
                          'placeholder': 'Password...'
                      }),
        address=dict(validators=[DataRequired(), validators.Length(max=100)],
                     render_kw={
                         'placeholder': 'Address...'
                     }),
        degree=dict(validators=[DataRequired(), validators.Length(max=100)],
                    render_kw={
                        'placeholder': 'Degree...'
                    }),
    )

    def is_accessible(self):
        if current_user.is_authenticated and current_user.setofpermission == 4:
            return True
        return False


class StudentView(BaseView):
    column_list = ['name', 'student', 'teacher']


class GradeView(ModelView):
    column_list = ['id', 'name']
    form_args = dict(
        name=dict(validators=[DataRequired(), validators.Length(max=10)],
                  render_kw={
                      'placeholder': 'Name...'
                  })
    )


class SetOfPermissionView(ModelView):
    column_list = ['name']


class ScoreView(ModelView):
    column_list = ['student_class_id', 'subject_teacher_class_id', 'typeofscore_id', 'score']
    form_args = dict(
        score=dict(validators=[DataRequired(), validators.Length(max=10)],
                   render_kw={
                       'placeholder': 'Score...'
                   })
    )


class SubjectView(ModelView):
    column_list = ['id', 'name', 'head_teacher']
    form_args = dict(
        name=dict(validators=[DataRequired(), validators.Length(max=50)],
                  render_kw={
                      'placeholder': 'Name...'
                  })
    )


class LogoutView(BaseView):
    @expose('/')
    def __index__(self):
        logout_user()
        return redirect(url_for("user_login"))


class MyStatsView(BaseView):
    @expose('/')
    def __index__(self):
        semester_list = dao.load_semester()
        classes_list = dao.load_classes()
        class_id = request.args.get("classes")
        semester_id = request.args.get("semester")
        order = request.args.get("order")
        class_name = None
        semester_name = None
        student_lists = dao.calc_AVG_studnent_in_class(class_id=int(1), semester_id=int(1),
                                                           order_select=int(1))
        if class_id and semester_id and order:
            student_lists = dao.calc_AVG_studnent_in_class(class_id=int(class_id), semester_id=int(semester_id),
                                                           order_select=int(order))
            class_name = dao.get_class_by_id(class_id)
            semester_name = dao.get_semester_by_id(semester_id)

        return self.render('admin/stats.html',students= student_lists,classes=classes_list , semester=semester_list,
                           class_name=class_name, semester_name=semester_name)



admin.add_view(CustomUserView(Student, db.session, name="Manage Students"))
admin.add_view(CustomUserView(Teacher, db.session, name="Manage Teachers"))
admin.add_view(CustomUserView(Staff, db.session, name="Manage Staff"))
admin.add_view(ScoreView(Score, db.session))
admin.add_view(SubjectView(Subject, db.session))
admin.add_view(GradeView(Grade, db.session))
admin.add_view(MyStatsView(name='Statistics'))
admin.add_view(LogoutView(name='Logout'))
