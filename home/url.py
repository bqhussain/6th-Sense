from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from . import views as user_view
from loginstuff.forms import LoginForm
from loginstuff.views import login_view, register_view

urlpatterns = [
    # path('', views.home, name='homepage'),
    path('', login_view, {'authentication_form': LoginForm}, name='login'),
    path('register/', register_view, {'authentication_form': LoginForm}, name="register"),
    path('profile/', user_view.profile_view, name="profile"),
    path('change_password/', user_view.change_password, name="change_password"),
    path('active_appointments/', user_view.patient_active_appoints, name="patient_active"),
    path('pending_appointments/', user_view.patient_pending_appoints, name="patient_pending"),
    path('completed_appointments/', user_view.patient_completed_appoints, name="patient_completed"),
    path('declined_appointments/', user_view.patient_declined_appoints, name="patient_declined"),
    path('rating/', user_view.rating, name="rating"),
    path('check_out/', user_view.transaction, name="check_out"),
    path('survey/', user_view.depression_survery, name="survey"),
    path('dashboard/', user_view.dashboard, name="dashboard"),
    path('bookappointment/', user_view.appointment, name='booking'),
    path('bookappointment/<int:id>/', user_view.confirmappoint, name='confirmBooking'),
    # path('login/', auth_views.LoginView.as_view(template_name='home/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='home/logout.html'), name="logout"),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='home/password_reset.html'),
         name="password_reset"),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='home/password_reset_done.html'),
         name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='home/password_reset_confirm.html'),
         name="password_reset_confirm"),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='home/password_reset_complete.html'),
         name="password_reset_complete"),
    # path('dashboard/',3 views.dashboard, name='dashboard')
]
