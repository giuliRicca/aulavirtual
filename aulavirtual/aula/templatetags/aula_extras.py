from django import template
from ..models import Assignment, Response

register = template.Library()


@register.filter(name='assigned')
def assigned(student, assignment_id):
    css_class = ''
    assignment = Assignment.objects.get(id=assignment_id)
    if student.is_assigned(assignment_id):
        css_class = 'success'
    elif assignment.is_overdue:
        css_class = 'danger'
    return css_class


@register.filter(name='response_file_name')
def response_file_name(student, assignment_id):
    try:
        assignment = Assignment.objects.get(id=assignment_id)
        response = assignment.response_set.get(
            student=student)
        file_name = response.file_name
        print(file_name)
    except:
        file_name = ''

    return file_name


@register.filter(name='response_file_url')
def response_file_url(student, assignment_id):
    try:
        assignment = Assignment.objects.get(id=assignment_id)
        response = assignment.response_set.get(
            student=student)
        file_url = response.file_url
    except:
        file_url = ''

    return file_url


@register.filter(name='text_response')
def text_response(student, assignment_id):
    try:
        assignment = Assignment.objects.get(id=assignment_id)
        response = assignment.response_set.get(
            student=student)
        text_response = response.text_response
    except:
        text_response = ''

    return text_response
