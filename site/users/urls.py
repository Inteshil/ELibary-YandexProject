from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path(
        'change_password/', views.ChangePasswordView.as_view(),
        name='change_password'
        ),
    path(
        'password_change_done/', views.ChangePasswordDoneView.as_view(),
        name='password_change_done'
        ),

    path(
        'reset_password/', views.ResetPasswordView.as_view(),
        name='reset_password'
        ),
    path(
        'reset_password_done/', views.ResetPasswordDoneView.as_view(),
        name='reset_password_done'
        ),
    path(
        'reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(),
        name='reset_password_confirm'
        ),
    path(
        'reset/done/', views.PasswordResetCompleteView.as_view(),
        name='password_reset_done'
        ),


    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path(
        'user/<int:user_id>/', views.UserDetailView.as_view(),
        name='user_details'
        ),
]
