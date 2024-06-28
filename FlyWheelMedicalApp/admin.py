from django.contrib import admin
from .models import User, Client, Doctor, Specialization, SpecializationDoctors, Manager, Schedule, Appointment, \
    AppointmentsInformation, MedicalHistory, AnalysisDirection, AnalysisResult, Service


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Client._meta.get_fields() if not (field.many_to_many or field.one_to_many)]


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Doctor._meta.get_fields() if not (field.many_to_many or field.one_to_many)]


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Specialization._meta.get_fields() if
                    not (field.many_to_many or field.one_to_many)]


@admin.register(SpecializationDoctors)
class SpecializationDoctorsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SpecializationDoctors._meta.get_fields() if
                    not (field.many_to_many or field.one_to_many)]


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Manager._meta.get_fields() if not (field.many_to_many or field.one_to_many)]


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Schedule._meta.get_fields() if
                    not (field.many_to_many or field.one_to_many)]


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Appointment._meta.get_fields() if
                    not (field.many_to_many or field.one_to_many)]


@admin.register(AppointmentsInformation)
class AppointmentsInformationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AppointmentsInformation._meta.get_fields() if
                    not (field.many_to_many or field.one_to_many)]


@admin.register(MedicalHistory)
class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MedicalHistory._meta.get_fields() if
                    not (field.many_to_many or field.one_to_many)]


@admin.register(AnalysisDirection)
class AnalysisDirectionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AnalysisDirection._meta.get_fields() if
                    not (field.many_to_many or field.one_to_many)]


@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AnalysisResult._meta.get_fields() if
                    not (field.many_to_many or field.one_to_many)]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Service._meta.get_fields() if not (field.many_to_many or field.one_to_many)]
