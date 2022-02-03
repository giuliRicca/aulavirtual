from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Response
from .models import Notification


@receiver(post_save, sender=Response)
def student_response_add_notify(sender, instance, **kwargs):
    print('Hello')
    try:
        recipient = instance.assignment.get_teacher()
        message = "{}: Nueva respuesta de {} en {}.".format(instance.assignment.subject,
                                                            instance.student, instance.assignment)
        response_id = instance.id
        Notification.objects.create(
            sender=instance.student.user, recipient=recipient,
            message=message,
            response_id=response_id)
    except KeyError as e:
        print(e)
        return False


@receiver(post_delete, sender=Response)
def delete_student_response_notification(sender, instance, **kwargs):
    try:
        notification = Notification.objects.filter(response_id=instance.id)
        notification.delete()
    except:
        pass
