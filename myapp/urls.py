from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('attendance/', views.attendance, name='attendance'),
    path('students/', views.students, name='students'),
    path('marksheet/', views.marksheet, name='marksheet'),
    path("add-subject/", views.add_subject, name="add_subject"),
    path('certificate/', views.certificate, name='certificate'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher/certificates/', views.teacher_certificate_students, name='teacher_certificate_students'),
    path('teacher/certificates/<int:student_id>/', views.view_student_certificates, name='view_student_certificates'),
    path("view-attendance/", views.view_attendance, name="view_attendance"),
]