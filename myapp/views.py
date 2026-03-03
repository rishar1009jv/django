from django.shortcuts import render, redirect
from .models import Teacher


def signup(request):
    if request.method == "POST":
        teacherId = request.POST.get('teacherId')
        password = request.POST.get('password')

        if Teacher.objects.filter(teacherId=teacherId).exists():
            return render(request, 'signup.html', {
                'error': 'Teacher already exists'
            })

        Teacher.objects.create(
            teacherId=teacherId,
            password=password
        )

        return redirect('login')

    return render(request, 'signup.html')

def login(request):
    if request.method == "POST":
        user_type = request.POST.get("user_type")

        # TEACHER LOGIN
        if user_type == "teacher":
            teacherId = request.POST.get("teacherId")
            password = request.POST.get("password")

            try:
                teacher = Teacher.objects.get(
                    teacherId=teacherId,
                    password=password
                )

                request.session['teacher_logged_in'] = True
                request.session['teacher_id'] = teacher.id

                return redirect('dashboard')

            except Teacher.DoesNotExist:
                return render(request, "login.html", {
                    "error": "Invalid Teacher Credentials"
                })

        # STUDENT LOGIN
        elif user_type == "student":
            reg = request.POST.get("studentReg")
            name = request.POST.get("studentName")

            try:
                student = Student.objects.get(
                    studentReg=reg,
                    studentName=name
                )

                request.session['student_logged_in'] = True
                request.session['student_id'] = student.id

                return redirect('student_dashboard')

            except Student.DoesNotExist:
                return render(request, "login.html", {
                    "error": "Invalid Student Details"
                })

    return render(request, "login.html")

def dashboard(request):
    if not request.session.get('teacher_logged_in'):
        return redirect('login')

    return render(request, 'dashboard.html')

from .models import Student, Teacher, Attendance
from datetime import date

def attendance(request):
    if not request.session.get('teacher_logged_in'):
        return redirect('login')

    teacher_id = request.session['teacher_id']
    teacher = Teacher.objects.get(id=teacher_id)

    if request.method == "POST":
        selected_date = request.POST.get('date')

        students = Student.objects.filter(teacher=teacher)

        for student in students:
            status = request.POST.get(f'status_{student.id}')

            if status:
                Attendance.objects.update_or_create(
                    student=student,
                    date=selected_date,
                    defaults={'status': status}
                )

        return render(request, 'attendance.html', {
    'students': students,
    'today': selected_date,
    'success': "Attendance Saved Successfully!"
})

    students = Student.objects.filter(teacher=teacher)

    return render(request, 'attendance.html', {
        'students': students,
        'today': date.today()
    })

def students(request):
    if not request.session.get('teacher_logged_in'):
        return redirect('login')

    teacher_id = request.session['teacher_id']
    teacher = Teacher.objects.get(id=teacher_id)

    # DELETE STUDENT
    if request.method == "POST" and 'delete_id' in request.POST:
        student_id = request.POST.get('delete_id')
        Student.objects.filter(id=student_id, teacher=teacher).delete()
        return redirect('students')

    # ADD STUDENT
    if request.method == "POST":
        reg = request.POST.get('studentReg')
        name = request.POST.get('studentName')

        Student.objects.create(
            teacher=teacher,
            studentReg=reg,
            studentName=name
        )

        return redirect('students')

    students = Student.objects.filter(teacher=teacher)

    return render(request, 'students.html', {
        'students': students
    })

from django.shortcuts import render, redirect
from .models import Student, Subject, Mark

def marksheet(request):
    if not request.session.get('teacher_logged_in'):
        return redirect('login')

    teacher_id = request.session['teacher_id']
    teacher = Teacher.objects.get(id=teacher_id)

    students = Student.objects.filter(teacher=teacher)
    subjects = Subject.objects.filter(teacher=teacher)

    if request.method == "POST":
        for student in students:
            for subject in subjects:
                mark_value = request.POST.get(f"mark_{student.id}_{subject.id}")

                if mark_value:
                    Mark.objects.update_or_create(
                        student=student,
                        subject=subject,
                        defaults={'marks': mark_value}
                    )

        return redirect('marksheet')

    marks = Mark.objects.filter(
        student__teacher=teacher
    )

    mark_dict = {}
    for mark in marks:
        mark_dict[(mark.student.id, mark.subject.id)] = mark.marks

    return render(request, 'marksheet.html', {
        'students': students,
        'subjects': subjects,
        'mark_dict': mark_dict
    })

from django.shortcuts import render, redirect
from .models import Subject
from .models import Teacher, Subject
def add_subject(request):
    if not request.session.get('teacher_logged_in'):
        return redirect('login')

    teacher_id = request.session['teacher_id']
    teacher = Teacher.objects.get(id=teacher_id)

    if request.method == "POST":

        # 🔥 DELETE SUBJECT
        if "delete_id" in request.POST:
            subject_id = request.POST.get("delete_id")
            Subject.objects.filter(id=subject_id, teacher=teacher).delete()
            return redirect('add_subject')

        # 🔥 ADD SUBJECT
        code = request.POST.get('subject_code')
        name = request.POST.get('subject_name')

        if code and name:
            Subject.objects.create(
                teacher=teacher,
                subject_code=code,
                subject_name=name
            )

        return redirect('add_subject')

    subjects = Subject.objects.filter(teacher=teacher)

    return render(request, 'add_subject.html', {
        'subjects': subjects
    })

from django.shortcuts import render, redirect
from .models import Certificate, Student


def certificate(request):
    # Student session check
    if "student_id" not in request.session:
        return redirect("login")

    student = Student.objects.get(id=request.session["student_id"])

    # DELETE CERTIFICATE
    if request.method == "POST" and "delete_id" in request.POST:
        cert = Certificate.objects.get(
            id=request.POST.get("delete_id"),
            student=student
        )
        cert.delete()
        return redirect("certificate")

    # UPLOAD CERTIFICATE
    if request.method == "POST" and "file" in request.FILES:
        file = request.FILES["file"]
        description = request.POST.get("description")

        Certificate.objects.create(
            student=student,
            file=file,
            description=description
        )

        return redirect("certificate")

    certificates = Certificate.objects.filter(student=student)

    return render(request, "certificate.html", {
        "certificates": certificates
    })
def student_dashboard(request):
    if not request.session.get('student_logged_in'):
        return redirect('login')

    return render(request, 'student_dashboard.html')

def teacher_certificate_students(request):
    teacher_id = request.session.get('teacher_id')

    if not teacher_id:
        return redirect('login')

    teacher = Teacher.objects.get(id=teacher_id)

    students = Student.objects.filter(teacher=teacher)

    return render(request, 'teacher_certificate_students.html', {
        'students': students
    })

def view_student_certificates(request, student_id):
    teacher_id = request.session.get('teacher_id')

    if not teacher_id:
        return redirect('login')

    teacher = Teacher.objects.get(id=teacher_id)

    student = Student.objects.get(id=student_id, teacher=teacher)

    certificates = Certificate.objects.filter(student=student)

    return render(request, 'view_student_certificates.html', {
        'student': student,
        'certificates': certificates
    })

from django.shortcuts import render, redirect
from .models import Attendance, Student
from django.shortcuts import render, redirect
from .models import Student, Attendance


def view_attendance(request):
    teacher_id = request.session.get("teacher_id")

    if not teacher_id:
        return redirect("login")

    students = Student.objects.filter(teacher_id=teacher_id)

    attendance_records = Attendance.objects.filter(
        student__teacher_id=teacher_id
    ).select_related("student")

    # Collect unique dates
    dates = sorted(set(record.date for record in attendance_records))

    # Create attendance matrix
    attendance_data = []

    for student in students:
        row = {
            "student": student,
            "records": []
        }

        for date in dates:
            record = attendance_records.filter(
                student=student,
                date=date
            ).first()

            if record:
                row["records"].append(record.status)
            else:
                row["records"].append("-")

        attendance_data.append(row)

    context = {
        "attendance_data": attendance_data,
        "dates": dates
    }

    return render(request, "view_attendance.html", context)