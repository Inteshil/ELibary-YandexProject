from django.views.generic import CreateView, DetailView, UpdateView
import django.contrib.auth.views as AuthViews
from django.urls.base import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

from users import forms
from users.models import User


class RegisterView(CreateView):
    form_class = forms.RegisterUserForm
    template_name = 'base_form.html'
    extra_context = {
        'title_name': 'Регистрация',
        'button_text': 'Создать аккаунт',
        'form_title': 'Регистрация',
    }
    success_url = reverse_lazy('static_pages:home')

    def form_valid(self, form):
        result = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return result


class LoginView(AuthViews.LoginView):
    form_class = forms.LoginUserForm
    template_name = 'Users/login_form.html'
    extra_context = {
        'title_name': 'Вход',
        'button_text': 'Войти',
        'form_title': 'Вход в аккаунт',
    }


class LogoutView(LoginRequiredMixin, AuthViews.LogoutView):
    template_name = 'Users/logout.html'


class ChangePasswordView(LoginRequiredMixin, AuthViews.PasswordChangeView):
    template_name = 'base_form.html'
    success_url = reverse_lazy('users:password_change_done')
    form_class = forms.ChangeUserPasswordForm
    extra_context = {
        'title_name': 'Изменить пароль',
        'form_title': 'Изменить пароль',
        'button_text': 'Изменить'
    }


class ChangePasswordDoneView(
    LoginRequiredMixin, AuthViews.PasswordChangeDoneView
):
    template_name = 'Users/password_change_done.html'
    extra_context = {
        'title_name': 'Пароль изменен'
    }


class ResetPasswordView(AuthViews.PasswordResetView):
    template_name = 'base_form.html'
    email_template_name = 'Users/reset_password_email.html'
    from_email = settings.OWNER_EMAIL
    form_class = forms.ResetUserPasswordForm
    model = User
    success_url = reverse_lazy('users:reset_password_done')
    extra_context = {
        'title_name': 'Восстановление пароля',
        'form_title': 'Восстановление пароля',
        'button_text': 'Восстановить'
    }


class ResetPasswordDoneView(AuthViews.PasswordResetDoneView):
    template_name = 'Users/reset_password_done.html'
    extra_context = {
        'title_name': 'Восстановление пароля'
    }


class PasswordResetConfirmView(AuthViews.PasswordResetConfirmView):
    template_name = 'base_form.html'
    form_class = forms.ResetUserPasswordConfirmForm
    success_url = reverse_lazy('users:password_reset_done')
    extra_context = {
        'title_name': 'Сброс пароля',
        'form_title': 'Сброс пароля',
        'button_text': 'Изменить пароль'
    }


class PasswordResetCompleteView(AuthViews.PasswordResetCompleteView):
    template_name = 'Users/password_reset_done.html'
    extra_context = {
        'title_name': 'Успешный сброс пароля'
    }


class UserDetailView(DetailView):
    template_name = 'Users/user_details.html'
    queryset = User.objects.actived()
    pk_url_kwarg = 'user_id'
    context_object_name = 'user'
    extra_context = {
        'title_name': 'Профиль пользователя'
    }


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = forms.UpdateUserProfileForm
    template_name = 'Users/password_change_form.html'
    success_url = reverse_lazy('users:profile')
    extra_context = {
        'title_name': 'Мой профиль',
        'button_text': 'Сохранить',
        'form_title': 'Профиль',
    }

    def get_object(self):
        return self.request.user
