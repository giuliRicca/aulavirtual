from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    path('c/<int:id>/', views.subject, name="subject"),
    path('get_user_notifications/', views.user_notifications),

    path('c/<int:subject_id>/new',
         views.create_assignment, name="create_assignment"),
    path('c/<int:subject_id>/a/<int:assignment_id>/edit',
         views.edit_assignment, name="edit_assignment"),
    path('c/<int:subject_id>/a/<int:assignment_id>/delete',
         views.delete_assignment, name="delete_assignment"),

    path('delete-resposne/<int:response_id>/',
         views.delete_response, name="delete-response"),

    path('c/<int:subject_id>/a/<int:assignment_id>/',
         views.assignment, name="assignment"),
]
