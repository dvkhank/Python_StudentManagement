from app import app, db
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import logout_user, current_user
from flask import redirect, url_for
from app.models import Student, Teacher, Subject, Staff, SetOfPermission, Permission_SetOfPermission

admin = Admin(app=app, name="STUDENT MANAGEMENT", template_mode='bootstrap4')


class CustomUserView(ModelView):
    create_template = 'admin/models/create.html'
    column_editable_list = ['phone', 'email']
    column_list = ['last_name', 'first_name', 'date_of_birth', 'email', 'phone', 'username', 'password',
                   'active']
    column_searchable_list = ['first_name', 'first_name']
    column_filters = ['last_name', 'first_name', 'active', 'setofpermission']
    def is_accessible(self):
        if current_user.is_authenticated and current_user.setofpermission == 4:
            return True
        return False


class StudentView(BaseView):
    column_list = ['name', 'student', 'teacher']



class SetOfPermissionView(ModelView):
    column_list = ['name']

class SubjectView(ModelView):
    column_list = ['id', 'name', 'head_teacher']


class LogoutView(BaseView):
    @expose('/')
    def __index__(self):
        logout_user()
        return redirect(url_for("user_login"))

class MyStatsView(BaseView):
    @expose('/')
    def __index__(self):
        return self.render('admin/stats.html')


admin.add_view(CustomUserView(Student, db.session, name="Manage Students"))
admin.add_view(CustomUserView(Teacher, db.session, name="Manage Teachers"))
admin.add_view(CustomUserView(Staff, db.session))
admin.add_view(SubjectView(Subject, db.session))
admin.add_view(MyStatsView(name='Statistics'))
admin.add_view(LogoutView(name='Logout'))

