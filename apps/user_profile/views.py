from django.contrib.auth import get_user_model
from django.views.generic import CreateView

from apps.user_profile.forms import UserRegistrationForm


class RegistrationView(CreateView):
    model = get_user_model()
    form_class = UserRegistrationForm
    template_name = 'user/registration.html'

    def form_valid(self, form):
        form.instance.is_staff = True
        return super().form_valid(form)
