from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Subject, Assignment, Response, Notification
from django.core.files.storage import FileSystemStorage
from .forms import ResponseForm, AssignmentForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
import json
from django.core import serializers
from django.http.response import JsonResponse
# Create your views here.


@login_required(login_url="login")
def home(request):
    context = {}
    user = request.user
    if user.is_student:
        subjects = user.student.student_subjects
        context['subjects'] = subjects
    elif user.is_teacher:
        subjects = user.subject_set.all()
        context['subjects'] = subjects

    return render(request, 'aula/home.html', context)


@login_required(login_url="login")
def subject(request, id):
    context = {}
    user = request.user
    if user.is_student:
        subject = user.student.get_subject(id)
        if subject is not None:
            context['subject'] = subject
            context['assignments'] = subject.assignment_set.all()
    elif user.is_teacher:
        try:
            subject = user.subject_set.get(id=id)
            context['subject'] = subject
            context['assignments'] = subject.assignment_set.all()
        except:
            return redirect('home')

    return render(request, 'aula/subject.html', context)


@login_required(login_url="login")
def create_assignment(request, subject_id):
    context = {}
    user = request.user
    if user.is_teacher:
        try:
            subject = user.subject_set.get(id=subject_id)
            context['subject'] = subject

            if request.method == 'POST':
                form = AssignmentForm(request.POST, files=request.FILES)
                if form.is_valid():
                    new_assignment = form.save(False)
                    new_assignment.subject = subject
                    new_assignment.save()
                    return redirect('subject', id=subject_id)
            form = AssignmentForm()
            context['form'] = form

        except:
            return redirect('home')

    return render(request, 'aula/assignment_form.html', context)


@login_required(login_url="login")
def edit_assignment(request, subject_id, assignment_id):
    context = {}
    user = request.user
    if user.is_teacher:
        try:
            subject = user.subject_set.get(id=subject_id)
            assignment = subject.assignment_set.get(id=assignment_id)
            context['subject'] = subject

            if request.method == 'POST':
                form = AssignmentForm(
                    request.POST, files=request.FILES, instance=assignment)
                if form.is_valid():
                    new_assignment = form.save(False)
                    new_assignment.subject = subject
                    new_assignment.save()
                    return redirect('subject', id=subject_id)
            form = AssignmentForm(instance=assignment)
            context['form'] = form

        except:
            return redirect('home')

    return render(request, 'aula/assignment_form.html', context)


@login_required(login_url="login")
def delete_assignment(request, subject_id, assignment_id):
    user = request.user
    if user.is_teacher:
        try:
            subject = user.subject_set.get(id=subject_id)
            assignment = subject.assignment_set.get(id=assignment_id)
            assignment.delete()
            return redirect('subject', id=subject_id)
        except:
            messages.error(request, 'Error al eliminar tarea')
        return redirect('home')


@login_required(login_url="login")
def assignment(request, subject_id, assignment_id):
    context = {}
    user = request.user
    template = 'assignment_student.html'
    try:
        subject = Subject.objects.get(id=subject_id)
        assignment = Assignment.objects.get(id=assignment_id)
        context["assignment"] = assignment
        context["subject"] = subject

        if user.is_student:
            response_status = assignment.get_response_status(user.student.id)
            context["response_status"] = response_status

            if request.method == "POST":
                form = ResponseForm(
                    request.POST, files=request.FILES)
                if form.is_valid():
                    response = form.save(False)
                    response.student = user.student
                    response.assignment = assignment
                    response.save()
                    print(subject_id)
                    return redirect('subject', id=subject_id)
            else:
                try:
                    response = assignment.response_set.get(
                        student=user.student)
                    context['response'] = response
                except:
                    form = ResponseForm()
                    context['form'] = form
        else:
            responses = assignment.response_set.all()
            context['responses'] = responses
            students = subject.classroom.student_set.all()
            context['students'] = students
            template = 'assignment_teacher.html'

    except:
        pass

    return render(request, 'aula/' + template, context)


@login_required(login_url="login")
def delete_response(request, response_id):
    try:
        response = Response.objects.get(id=response_id)
        response.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    except:
        return HttpResponse('Response not found')


@login_required(login_url="login")
def user_notifications(request):
    notifications = Notification.objects.filter(
        recipient=request.user, read=False)
    serialized_data = serializers.serialize(
        "json", notifications, fields=('pk', 'message', 'created_at'))

    return JsonResponse(serialized_data, safe=False)
