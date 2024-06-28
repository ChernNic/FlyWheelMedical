from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Client(models.Model):
    ClientID = models.AutoField(primary_key=True)
    FirstName = models.CharField(max_length=21)
    LastName = models.CharField(max_length=21)
    Surname = models.CharField(max_length=21, null=True)
    ContactNumber = models.CharField(max_length=11)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def get_full_name(self):
        if self.Surname:
            return f"{self.LastName} {self.FirstName}  {self.Surname}"
        else:
            return f"{self.LastName} {self.FirstName}"

    def __str__(self):
        return f"{self.get_full_name()}"


class Doctor(models.Model):
    DoctorID = models.AutoField(primary_key=True)
    FirstName = models.CharField(max_length=21)
    LastName = models.CharField(max_length=21)
    Surname = models.CharField(max_length=21, null=True)
    Qualification = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    ScheduleID = models.ForeignKey('Schedule', on_delete=models.CASCADE)

    def get_full_name(self):
        if self.Surname:
            return f"{self.FirstName} {self.LastName} {self.Surname}"
        else:
            return f"{self.FirstName} {self.LastName}"

    def __str__(self):
        return f"{self.get_full_name()}"


class Manager(models.Model):
    ManagerID = models.AutoField(primary_key=True)
    FirstName = models.CharField(max_length=21)
    LastName = models.CharField(max_length=21)
    Surname = models.CharField(max_length=21, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def get_full_name(self):
        if self.Surname:
            return f"{self.FirstName} {self.LastName} {self.Surname}"
        else:
            return f"{self.FirstName} {self.LastName}"

    def __str__(self):
        return f"{self.get_full_name()}"


class Specialization(models.Model):
    SpecializationID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=21)
    Description = models.CharField(max_length=21)


class SpecializationDoctors(models.Model):
    DoctorID = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    SpecializationID = models.ForeignKey(Specialization, on_delete=models.CASCADE)


class Schedule(models.Model):
    ScheduleID = models.AutoField(primary_key=True)
    StartTime = models.CharField(max_length=10)
    EndTime = models.CharField(max_length=10)
    BreakStartTime = models.CharField(max_length=20)
    BreakEndTime = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.StartTime} - {self.EndTime}"


class Appointment(models.Model):
    AppointmentID = models.AutoField(primary_key=True)
    ClientID = models.ForeignKey(Client, on_delete=models.CASCADE)
    DoctorID = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    AppointmentDate = models.DateTimeField()

    def __str__(self):
        return f"{self.AppointmentDate.strftime('%Y.%m.%d %H:%M')} {self.ClientID.get_full_name()}"


class AppointmentsInformation(models.Model):
    AppointmentInformationID = models.AutoField(primary_key=True)
    ServiceID = models.ForeignKey('Service', on_delete=models.CASCADE)
    AppointmentID = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    Status = models.BooleanField()

    def __str__(self):
        return f"{self.AppointmentID.AppointmentDate.strftime('%Y.%m.%d %H:%M')} {self.AppointmentID.ClientID.get_full_name()} ({self.ServiceID.ServiceName})"



class MedicalHistory(models.Model):
    MedicalHistoryID = models.AutoField(primary_key=True)
    ClientID = models.ForeignKey(Client, on_delete=models.CASCADE)
    AppointmentInformationID = models.ForeignKey(AppointmentsInformation, on_delete=models.CASCADE)

    def get_date(self):
        return f"{self.AppointmentInformationID.AppointmentID.AppointmentDate.strftime('%Y.%m.%d %H:%M')}"


class AnalysisDirection(models.Model):
    AnalysisDirectionID = models.AutoField(primary_key=True)
    ClientID = models.ForeignKey(Client, on_delete=models.CASCADE)
    DoctorID = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    ServiceID = models.ForeignKey('Service', on_delete=models.CASCADE)
    DirectionDate = models.DateTimeField()

    def __str__(self):
        return f"{self.DirectionDate.strftime('%Y.%m.%d %H:%M')} {self.ClientID.get_full_name()} ({self.ServiceID.ServiceName})"


class AnalysisResult(models.Model):
    AnalysisResultID = models.AutoField(primary_key=True)
    DirectionID = models.ForeignKey(AnalysisDirection, on_delete=models.CASCADE)
    ResultDescription = models.CharField(max_length=50)
    ResultDate = models.DateTimeField()

    def __str__(self):
        return self.ResultDate.strftime('%Y.%m.%d %H:%M')


class Service(models.Model):
    ServiceID = models.AutoField(primary_key=True)
    ServiceName = models.CharField(max_length=255)
    Description = models.TextField()
    Price = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return self.ServiceName


@receiver(post_save, sender=AppointmentsInformation)
def update_medical_history(sender, instance, created, **kwargs):
    # Проверяем, была ли создана новая запись на прием
    if created:
        # Если да, то проверяем статус
        if instance.Status:
            # Если статус True, то добавляем запись в медицинскую историю
            MedicalHistory.objects.create(
                ClientID=instance.AppointmentID.ClientID,
                AppointmentInformationID=instance
            )
    else:
        # Если запись на прием не была создана, то обновляем статус и проверяем его
        if instance.Status:
            # Если статус True, то добавляем запись в медицинскую историю
            MedicalHistory.objects.create(
                ClientID=instance.AppointmentID.ClientID,
                AppointmentInformationID=instance
            )
        else:
            # Если статус False, то удаляем запись из медицинской истории, если она там есть
            MedicalHistory.objects.filter(AppointmentInformationID=instance).delete()
