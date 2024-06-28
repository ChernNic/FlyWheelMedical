# Generated by Django 5.0.2 on 2024-02-16 14:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnalysisDirection',
            fields=[
                ('AnalysisDirectionID', models.AutoField(primary_key=True, serialize=False)),
                ('DirectionDate', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('AppointmentID', models.AutoField(primary_key=True, serialize=False)),
                ('AppointmentDate', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('ClientID', models.AutoField(primary_key=True, serialize=False)),
                ('FirstName', models.CharField(max_length=21)),
                ('LastName', models.CharField(max_length=21)),
                ('Surname', models.CharField(max_length=21, null=True)),
                ('ContactNumber', models.CharField(max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('DoctorID', models.AutoField(primary_key=True, serialize=False)),
                ('FirstName', models.CharField(max_length=21)),
                ('LastName', models.CharField(max_length=21)),
                ('Surname', models.CharField(max_length=21, null=True)),
                ('Qualification', models.CharField(max_length=21)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('ScheduleID', models.AutoField(primary_key=True, serialize=False)),
                ('StartTime', models.CharField(max_length=10)),
                ('EndTime', models.CharField(max_length=10)),
                ('BreakStartTime', models.CharField(max_length=20)),
                ('BreakEndTime', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('ServiceID', models.AutoField(primary_key=True, serialize=False)),
                ('ServiceName', models.CharField(max_length=21)),
                ('Description', models.CharField(max_length=50)),
                ('Price', models.DecimalField(decimal_places=2, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('SpecializationID', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=21)),
                ('Description', models.CharField(max_length=21)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('UserID', models.AutoField(primary_key=True, serialize=False)),
                ('Username', models.CharField(max_length=21)),
                ('Password', models.CharField(max_length=39)),
            ],
        ),
        migrations.CreateModel(
            name='AnalysisResult',
            fields=[
                ('AnalysisResultID', models.AutoField(primary_key=True, serialize=False)),
                ('ResultDescription', models.CharField(max_length=50)),
                ('ResultDate', models.DateTimeField()),
                ('DirectionID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FlyWheelMedicalApp.analysisdirection')),
            ],
        ),
        migrations.CreateModel(
            name='AppointmentsInformation',
            fields=[
                ('AppointmentInformationID', models.AutoField(primary_key=True, serialize=False)),
                ('Status', models.BooleanField()),
                ('AppointmentID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FlyWheelMedicalApp.appointment')),
                ('ServiceID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FlyWheelMedicalApp.service')),
            ],
        ),
        migrations.AddField(
            model_name='appointment',
            name='ClientID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FlyWheelMedicalApp.client'),
        ),
        migrations.AddField(
            model_name='analysisdirection',
            name='ClientID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FlyWheelMedicalApp.client'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='DoctorID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FlyWheelMedicalApp.doctor'),
        ),
        migrations.CreateModel(
            name='MedicalHistory',
            fields=[
                ('MedicalHistoryID', models.AutoField(primary_key=True, serialize=False)),
                ('AppointmentInformationID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FlyWheelMedicalApp.appointmentsinformation')),
                ('ClientID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FlyWheelMedicalApp.client')),
            ],
        ),
        migrations.AddField(
            model_name='doctor',
            name='ScheduleID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FlyWheelMedicalApp.schedule'),
        ),
        migrations.AddField(
            model_name='analysisdirection',
            name='ServiceID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FlyWheelMedicalApp.service'),
        ),
        migrations.CreateModel(
            name='SpecializationDoctors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DoctorID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FlyWheelMedicalApp.doctor')),
                ('SpecializationID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FlyWheelMedicalApp.specialization')),
            ],
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('ManagerID', models.AutoField(primary_key=True, serialize=False)),
                ('FirstName', models.CharField(max_length=21)),
                ('LastName', models.CharField(max_length=21)),
                ('Surname', models.CharField(max_length=21, null=True)),
                ('UserID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FlyWheelMedicalApp.user')),
            ],
        ),
        migrations.AddField(
            model_name='doctor',
            name='UserID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FlyWheelMedicalApp.user'),
        ),
        migrations.AddField(
            model_name='client',
            name='UserID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FlyWheelMedicalApp.user'),
        ),
    ]
