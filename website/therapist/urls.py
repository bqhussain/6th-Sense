from django.urls import path
from . import views as user_view

urlpatterns = [

    path('', user_view.tdashboard, name="tdashboard"),
    path('active/', user_view.active_appoints, name="active"),
    path('pending/', user_view.pending_appoints, name="pending"),
    path('completed/', user_view.completed_appoints, name="p_completed"),
    path('declined/', user_view.declined_appoints, name="p_declined"),
    path('delete/<int:id>/', user_view.delete_appoints, name='delete_appoint'),
    path('confirm/<int:id>/', user_view.confirm_appoints, name='confirm_appoint'),
    path('profile/', user_view.profile_view, name="therapist_profile"),
    path('patients/', user_view.patients_view, name="patients"),
    path('patient_profile/<int:id>/', user_view.patient_profile, name='patient_profile'),
    path('patient_profile/<int:id>/survey_results/', user_view.survey_results, name='survey_results'),
    path('patient_profile/<int:id>/chat_transcript/', user_view.chat_transcript, name='chat_transcript'),
    # path('dashboard/', views.dashboard, name='dashboard')
]
