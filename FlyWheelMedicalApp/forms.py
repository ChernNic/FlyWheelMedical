from django import forms
from FlyWheelMedicalApp.models import *


class ClientRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Client
        fields = ['FirstName', 'LastName', 'Surname', 'ContactNumber']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            password=self.cleaned_data["password"]
        )
        client = super().save(commit=False)
        client.user = user
        if commit:
            client.save()
        return client


class ClientEditForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['FirstName', 'LastName', 'Surname', 'ContactNumber']


class DoctorEditForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['FirstName', 'LastName', 'Surname', 'Qualification']