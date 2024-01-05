from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
import os
from colorfield.fields import ColorField
from django.utils import timezone, dateformat
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

# Create your models here.


def date_validation(date):
    try:
        now = timezone.now()
        if date < now:
            raise ValidationError("{} Is invalid".format(date))
    except:
        pass


class Classroom(models.Model):
    name = models.CharField(max_length=4, unique=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    dni = models.IntegerField(null=True, blank=True, unique=True)
    classroom = models.ForeignKey(
        Classroom, on_delete=models.CASCADE, null=True, blank=True)

    @receiver(post_save, sender=get_user_model())
    def create_user_profile(sender, instance, created, **kwargs):
        if created and instance.is_student:
            Student.objects.create(user=instance)

    @receiver(post_save, sender=get_user_model())
    def save_user_profile(sender, instance, **kwargs):
        if instance.is_student:
            instance.student.save()

    class Meta:
        verbose_name = u'Estudiante'
        verbose_name_plural = u'Estudiantes'
        ordering = ['user__last_name']

    @property
    def student_subjects(self):
        return self.classroom.subject_set.all()

    def get_subject(self, subject_id):
        try:
            subject = self.classroom.subject_set.get(id=subject_id)
        except:
            subject = None

        return subject

    def is_assigned(self, assignment_id):
        try:
            assignment = Assignment.objects.get(id=assignment_id)
            assignment_responses = assignment.response_set.all()
            if assignment_responses.get(student=self):
                return True
        except:
            return False

    def __str__(self):
        return self.user.email


class Subject(models.Model):
    MAT = "MAT"
    LIT = "LIT"
    EDF = "EDF"
    ING = "ING"
    CIU = "CIU"
    ART = "ART"
    FIL = "FIL"
    QUI = "QUI"

    KIND_CHOICES = [
        (MAT, "Matematica"),
        (LIT, "Literatura"),
        (EDF, "Educaion fisica"),
        (ING, "Ingles"),
        (CIU, "Ciudadania y Participacion"),
        (ART, "Arte"),
        (FIL, "Filosofia"),
        (QUI, "Quimica"),

    ]

    COLOR_CHOICES = [
        ("#FF923C", "orange"),
        ("#0099FF", "blue"),
        ("#3AFF51", "green"),
        ("#FF1D1D", "red"),
        ("#F6FF35", "yellow"),
        ("#ED46FF", "pink"),
    ]

    classroom = models.ForeignKey(
        Classroom, on_delete=models.CASCADE, blank=True, null=True)
    teacher = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
    kind = models.CharField(
        max_length=3, choices=KIND_CHOICES, null=True, blank=True)
    color = ColorField(choices=COLOR_CHOICES, null=True, blank=True)

    @ property
    def title(self):
        return self.get_kind_display() + " " + self.classroom.name

    def __str__(self):
        return self.kind + " " + self.classroom.name


class Assignment(models.Model):
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500, null=True, blank=True)
    assigment_file = models.FileField(
        upload_to="documents/assignments/", blank=True, null=True)
    due_date = models.DateTimeField(null=True, blank=True)

    def get_due_date(self):
        if self.due_date and not self.is_overdue:
            return "vence " + self.due_date.strftime("%d %b, %Y")
        elif self.is_overdue:
            return "venció " + self.due_date.strftime("%d %b, %Y")
        return "sin fecha de vencimiento"

    def clean(self):
        date_validation(self.due_date)
        return super().clean()

    @property
    def is_overdue(self):
        if self.due_date:
            now = timezone.now()
            if self.due_date < now:
                return True
            else:
                return False
        return

    @property
    def file_name(self):
        return os.path.basename(self.assigment_file.name)

    @property
    def file_url(self):
        if self.assigment_file:
            return self.assigment_file.url
        else:
            return None

    @property
    def file_extension(self):
        if self.assigment_file:
            filename, file_extension = os.path.splitext(
                self.assigment_file.path)
            extension = file_extension[1:]
            if extension.__contains__('doc'):
                extension = 'word'
            elif extension != 'pdf':
                extension = 'alt'
        else:
            return None

        return "file-" + extension

    def get_response_status(self, student_id):
        status = ['Asignado', 'text-success']
        try:
            student = Student.objects.get(id=student_id)
            status = ''
            return status
        except:
            return status

    def __str__(self):
        return self.title

    def get_teacher(self):
        if self.subject.teacher:
            return self.subject.teacher
        return


def get_response_upload_path(instance, filename):
    return os.path.join("documents/assignments", "%d" % instance.assignment.id, filename)


class Response(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    text_response = models.TextField(
        max_length=500, blank=True, null=True, verbose_name="Respuesta")
    response_file = models.FileField(
        upload_to=get_response_upload_path, blank=True, null=True)

    @property
    def file_name(self):
        try:
            if self.response_file:
                filename = os.path.basename(self.response_file.name)
            else:
                filename = "No hay archivo adjunto"
        except:
            return KeyError("No found")

        return filename

    @property
    def file_url(self):
        try:
            url = self.response_file.url
            return url
        except:
            return ''

    def __str__(self):
        return self.assignment.title + " " + self.student.__str__()


class Notification(models.Model):
    sender = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, null=True, related_name='sender_notification')
    recipient = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='recipient_notification', null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    response_id = models.IntegerField(null=True, blank=True)
    read = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, )

    @property
    def since_created(self):
        now = timezone.now()
        delta = dateformat.format(self.created_at, 'Y-m-d H:i')
        return delta

    def __str__(self):
        return self.message
