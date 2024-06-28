from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages

from FlyWheelMedicalApp.forms import ClientRegistrationForm, DoctorEditForm
from FlyWheelMedicalApp.models import Client, Manager, Doctor, Appointment, Service, AppointmentsInformation, \
    AnalysisResult, AnalysisDirection, MedicalHistory, Schedule

from django.shortcuts import render, redirect
from django.views import View
from FlyWheelMedicalApp.models import Client
from FlyWheelMedicalApp.forms import ClientEditForm


# ЛИЧНЫЙ КАБИНЕТ КЛИЕНТА
class ClientDashboardView(View):
    def get(self, request):
        # Проверяем, авторизован ли пользователь
        if not request.user.is_authenticated:
            return redirect('login')  # Перенаправляем на страницу входа, если пользователь не авторизован

        # Получаем клиента, связанного с текущим пользователем
        try:
            client = Client.objects.get(user=request.user)
        except Client.DoesNotExist:
            # Если клиент не найден, можно вернуть ошибку или перенаправить на другую страницу
            return redirect('login')  # Перенаправляем на страницу входа, если пользователь не авторизован

        # Получаем все записи клиента
        appointments = Appointment.objects.filter(ClientID=client)
        # Получаем информацию о каждой записи, включая ФИО врача и название услуги
        appointments_info = []
        for appointment in appointments:
            doctor_full_name = appointment.DoctorID.get_full_name()
            service_name = appointment.appointmentsinformation_set.first().ServiceID.ServiceName
            appointments_info.append({
                'date': appointment.AppointmentDate.strftime("%Y.%m.%d %H:%M"),
                'doctor_full_name': doctor_full_name,
                'service_name': service_name,
                'status': appointment.appointmentsinformation_set.get(AppointmentID=appointment.AppointmentID).Status
            })

            # Получаем список врачей и услуг для использования в форме добавления записи
        doctors = Doctor.objects.all()
        services = Service.objects.all()

        # Получаем результаты анализов клиента
        analysis_directions = AnalysisDirection.objects.filter(ClientID=client)
        analysis_results = AnalysisResult.objects.filter(DirectionID__in=analysis_directions)

        # Выводим информацию о клиенте и записях
        context = {
            'client': client,
            'edit_form': ClientEditForm(instance=client),  # Передаем форму редактирования данных клиента
            'doctors': doctors,
            'services': services,
            'appointments_info': appointments_info,
            'analysis_results': analysis_results,  # Передаем результаты анализов
            'analysis_directions': analysis_directions,
        }
        return render(request, 'profiles/client_dashboard.html', context)

    def post(self, request):
        # Получаем клиента, связанного с текущим пользователем
        client = Client.objects.get(user=request.user)

        # Обрабатываем POST-запрос для редактирования данных клиента
        form = ClientEditForm(request.POST, instance=client)
        if form.is_valid():
            form.save()  # Сохраняем изменения
            return redirect('client_dashboard')  # Перенаправляем на страницу панели клиента после успешного сохранения

        # Если форма недопустима, возвращаем страницу снова с формой и ошибками
        context = {
            'client': client,
            'edit_form': form
        }
        return render(request, 'profiles/client_dashboard.html', context)


class AddAppointmentView(View):
    def post(self, request):
        # Получаем данные из POST-запроса
        appointment_date = request.POST.get('appointment_date')
        doctor_id = request.POST.get('doctor_id')
        service_id = request.POST.get('service_id')

        # Создаем новую запись на прием
        appointment = Appointment.objects.create(
            ClientID=Client.objects.get(user=request.user),
            DoctorID=Doctor.objects.get(DoctorID=doctor_id),
            AppointmentDate=appointment_date
        )

        # Создаем информацию о записи на прием
        AppointmentsInformation.objects.create(
            AppointmentID=appointment,
            ServiceID=Service.objects.get(ServiceID=service_id),
            Status=False
        )

        return redirect('client_dashboard')


# ЛИЧНЫЙ КАБИНЕТ ВРАЧА
class DoctorDashboardView(View):
    def get(self, request):
        # Проверяем, авторизован ли пользователь
        if not request.user.is_authenticated:
            return redirect('login')  # Перенаправляем на страницу входа, если пользователь не авторизован

        # Получаем клиента, связанного с текущим пользователем
        try:
            doctor = Doctor.objects.get(user=request.user)
        except Doctor.DoesNotExist:
            # Если клиент не найден, можно вернуть ошибку или перенаправить на другую страницу
            return redirect('login')  # Перенаправляем на страницу входа, если пользователь не авторизован

        # Получаем все записи клиента
        appointments = Appointment.objects.filter(DoctorID=doctor)
        # Получаем информацию о каждой записи, включая ФИО врача и название услуги
        appointments_info = []
        for appointment in appointments:
            medical_history = MedicalHistory.objects.select_related('ClientID',
                                                                    'AppointmentInformationID__AppointmentID__DoctorID',
                                                                    'AppointmentInformationID__ServiceID').filter(
                ClientID=appointment.ClientID)
            client_full_name = appointment.ClientID.get_full_name()
            service_id = appointment.appointmentsinformation_set.get(AppointmentID=appointment.AppointmentID).ServiceID
            appointments_info.append({
                'appointment_id': appointment.AppointmentID,
                'date': appointment.AppointmentDate.strftime("%Y-%m-%dT%H:%M"),
                'dateF': appointment.AppointmentDate.strftime("%Y.%m.%d %H:%M"),
                'client_full_name': client_full_name,
                'clientID': appointment.ClientID,
                'service_id': service_id,
                'service_name': appointment.appointmentsinformation_set.get(
                    AppointmentID=appointment.AppointmentID).ServiceID.ServiceName,
                'status': appointment.appointmentsinformation_set.get(AppointmentID=appointment.AppointmentID).Status,
                'medical_history': medical_history,
            })

        # Получаем все записи врача о направлениях на анализы
        analysis_directions = AnalysisDirection.objects.filter(DoctorID=doctor)
        # Получаем информацию о каждом направлении на анализы, включая дату направления и название услуги
        analysis_directions_info = []
        for direction in analysis_directions:
            service_name = direction.ServiceID.ServiceName
            analysis_directions_info.append({
                'direction_id': direction.AnalysisDirectionID,
                'client_name': direction.ClientID.get_full_name(),
                'service_name': service_name,
                'direction_date': direction.DirectionDate.strftime("%Y-%m-%d %H:%M"),
            })

        # Получаем все результаты анализов, связанные с направлениями на анализы врача
        analysis_results = AnalysisResult.objects.filter(DirectionID__DoctorID=doctor)
        # Получаем информацию о каждом результате анализа, включая описание результата и дату результата
        analysis_results_info = []
        for result in analysis_results:
            analysis_results_info.append({
                'result_id': result.AnalysisResultID,
                'client_name': result.DirectionID.ClientID.get_full_name(),
                'service_name': result.DirectionID.ServiceID.ServiceName,
                'direction_id': result.DirectionID,
                'result_description': result.ResultDescription,
                'result_date': result.ResultDate.strftime("%Y-%m-%d %H:%M"),
            })

        schedule = doctor.ScheduleID
        clients = Client.objects.all()
        services = Service.objects.all()
        context = {
            'doctor': doctor,
            'clients': clients,
            'services': services,
            'edit_form': DoctorEditForm(instance=doctor),  # Передаем форму редактирования данных клиента
            'appointments_info': appointments_info,
            'schedule': schedule,
            'directions': analysis_directions,
            'analysis_directions_info': analysis_directions_info,
            'analysis_results_info': analysis_results_info,
        }
        return render(request, 'profiles/doctor_dashboard.html', context)

    def post(self, request):
        # Получаем клиента, связанного с текущим пользователем
        doctor = Doctor.objects.get(user=request.user)

        # Обрабатываем POST-запрос для редактирования данных клиента
        form = DoctorEditForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()  # Сохраняем изменения
            return redirect('doctor_dashboard')  # Перенаправляем на страницу панели клиента после успешного сохранения

        # Если форма недопустима, возвращаем страницу снова с формой и ошибками
        context = {
            'doctor': doctor,
            'edit_form': form,
        }
        return render(request, 'profiles/doctor_dashboard.html', context)


class DoctorEditAppointmentView(View):
    def post(self, request):
        appointment_id = request.POST.get('appointment_id')
        date = request.POST.get('date')
        service_id = request.POST.get('service_id')
        client_id = request.POST.get('client_id')
        doctor_id = request.POST.get('doctor_id')
        status = request.POST.get('status') == 'on'

        # Найдите запись по appointment_id и обновите ее атрибуты
        appointment = Appointment.objects.get(AppointmentID=appointment_id)
        appointment.AppointmentDate = date
        appointment.DoctorID = Doctor.objects.get(DoctorID=doctor_id)
        appointment.ClientID = Client.objects.get(ClientID=client_id)
        appointment.save()

        appointmentInformation = AppointmentsInformation.objects.get(AppointmentID=appointment_id)
        appointmentInformation.ServiceID = Service.objects.get(ServiceID=service_id)
        appointmentInformation.Status = status
        appointmentInformation.save()

        return redirect('doctor_dashboard')  # Перенаправляем на страницу доктора после успешного сохранения


class DoctorDeleteAppointmentView(View):
    def post(self, request):
        appointment_id = request.POST.get('appointment_id')

        # Найдите запись по appointment_id и удалите ее
        appointment = Appointment.objects.get(AppointmentID=appointment_id)
        appointment.delete()

        return redirect('doctor_dashboard')  # Перенаправляем на страницу доктора после успешного удаления


class DoctorEditAnalysisDirectionView(View):
    def post(self, request):
        direction_id = request.POST.get('direction_id')
        direction_date = request.POST.get('direction_date')
        service_id = request.POST.get('service_id')
        client_id = request.POST.get('client_id')

        direction = AnalysisDirection.objects.get(AnalysisDirectionID=direction_id)
        direction.DirectionDate = direction_date
        direction.ServiceID = Service.objects.get(ServiceID=service_id)
        direction.ClientID = Client.objects.get(ClientID=client_id)
        direction.save()

        return redirect('doctor_dashboard')  # Перенаправляем на страницу доктора после успешного сохранения


class DoctorAddAnalysisDirectionView(View):
    def post(self, request):
        direction_date = request.POST.get('direction_date')
        service_id = request.POST.get('service_id')
        client_id = request.POST.get('client_id')
        doctor_id = request.POST.get('doctor_id')

        # Создаем новый объект AnalysisDirection и сохраняем его
        direction = AnalysisDirection.objects.create(
            DirectionDate=direction_date,
            ServiceID=Service.objects.get(ServiceID=service_id),
            ClientID=Client.objects.get(ClientID=client_id),
            DoctorID=Doctor.objects.get(DoctorID=doctor_id)
        )

        return redirect('doctor_dashboard')


class DoctorDeleteAnalysisDirectionView(View):
    def post(self, request):
        direction_id = request.POST.get('direction_id')

        # Найдите запись по appointment_id и удалите ее
        analysisDirection = AnalysisDirection.objects.get(AnalysisDirectionID=direction_id)
        analysisDirection.delete()
        return redirect('doctor_dashboard')  # Перенаправляем на страницу доктора после успешного удаления


class DoctorEditAnalysisResultView(View):
    def post(self, request):
        # Retrieve form data from POST request
        analysis_direction_id = request.POST.get('analysis_direction_id')
        analysis_result_id = request.POST.get('analysis_result_id')
        result_description = request.POST.get('result_description')
        result_date = request.POST.get('result_date')

        # Retrieve the analysis result object
        analysis_result = AnalysisResult.objects.get(AnalysisResultID=analysis_result_id)

        # Update the analysis result object with new data
        analysis_result.DirectionID = AnalysisDirection.objects.get(AnalysisDirectionID=analysis_direction_id)
        analysis_result.ResultDescription = result_description
        analysis_result.ResultDate = result_date
        analysis_result.save()

        # Redirect to doctor dashboard after successful update
        return redirect('doctor_dashboard')


class DoctorDeleleAnalysisResultView(View):
    def post(self, request):
        result_id = request.POST.get('result_id')

        # Найдите запись по appointment_id и удалите ее
        analysisResult = AnalysisResult.objects.get(AnalysisResultID=result_id)
        analysisResult.delete()
        return redirect('doctor_dashboard')  # Перенаправляем на страницу доктора после успешного удаления


class DoctorAddAnalysisResultView(View):
    def post(self, request):
        # Retrieve data from the form
        result_description = request.POST.get('result_description')
        analysis_direction_id = request.POST.get('analysis_direction_id')
        result_date = request.POST.get('result_date')

        # Get the AnalysisDirection object corresponding to the ID
        analysis_direction = AnalysisDirection.objects.get(pk=analysis_direction_id)

        # Create a new AnalysisResult object
        analysis_result = AnalysisResult(
            ResultDescription=result_description,
            DirectionID=analysis_direction,
            ResultDate=result_date
        )

        # Save the new analysis result
        analysis_result.save()

        # Redirect to the doctor dashboard
        return redirect('doctor_dashboard')