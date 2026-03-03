from django.db import models

class Teacher(models.Model):
    teacherId = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.teacherId


class Student(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    studentReg = models.CharField(max_length=50)
    studentName = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.studentReg} - {self.studentName}"


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10)

    class Meta:
        unique_together = ('student', 'date')

class Subject(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject_code = models.CharField(max_length=20)
    subject_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.subject_code} - {self.subject_name}"


class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.IntegerField()

class Certificate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    file = models.FileField(upload_to='certificates/')
    description = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.studentName} - Certificate"