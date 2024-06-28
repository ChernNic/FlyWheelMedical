from django.urls import path
from FlyWheelMedicalApp.profiles.views import *

urlpatterns = [
    path('client/', ClientDashboardView.as_view(), name='client_dashboard'),
    path('client/add_appointment', AddAppointmentView.as_view(), name='add_appointment'),

    path('doctor/', DoctorDashboardView.as_view(), name='doctor_dashboard'),
    path('doctor/edit_appointment', DoctorEditAppointmentView.as_view(), name='doctor_edit_appointment'),
    path('doctor/delete_appointment', DoctorDeleteAppointmentView.as_view(), name='doctor_delete_appointment'),
    path('doctor/edit_analysis_direction', DoctorEditAnalysisDirectionView.as_view(), name='doctor_edit_analysis_direction'),
    path('doctor/add_analysis_direction', DoctorAddAnalysisDirectionView.as_view(), name='doctor_add_analysis_direction'),
    path('doctor/delete_analysis_direction', DoctorDeleteAnalysisDirectionView.as_view(), name='doctor_delete_analysis_direction'),
    path('doctor/edit_analysis_result', DoctorEditAnalysisResultView.as_view(), name='doctor_edit_analysis_result'),
    path('doctor/delete_analysis_result', DoctorDeleleAnalysisResultView.as_view(), name='doctor_delete_analysis_result'),
    path('doctor/add_analysis_result', DoctorAddAnalysisResultView.as_view(), name='doctor_add_analysis_result'),
]
