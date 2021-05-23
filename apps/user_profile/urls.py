from django.urls import path

from . import views

app_name = 'user_profile'


urlpatterns = [
    path('user/registration/', views.RegistrationView.as_view(), name='registration-form'),
]
