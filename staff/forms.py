
from django import forms
from django.contrib.auth import get_user_model

import datetime
from django.apps import apps

staff_profile_model = apps.get_model('staff', 'StaffProfile')
user_model = get_user_model()


class StaffRegistrationForm(forms.Form):
    this_year = datetime.date.today().year
    years = range(this_year - 100, this_year + 1)

    departments = (("Select department", "Select department"),
                   ("ICT", "ICT"),
                   ("SECURITY", "SECURITY"),
                   ("STUDENT AFFAIRS", "STUDENT AFFAIRS"),
                   ("LIBRARY", "LIBRARY"),
                   ("EXAM OFFICE", "EXAM OFFICE"),
                   ("BURSARY", "BURSARY"))
    genders = (
        ("Select Gender", "Select Gender"),
        ("MALE", "MALE"),
        ("FEMALE", "FEMALE")
    )

    first_name = forms.CharField(max_length=50, label='First Name', required=True)
    surname = forms.CharField(max_length=50, label='Surname', required=True)
    other_name = forms.CharField(max_length=50, label='Other Names', required=False)

    email = forms.EmailField(label='Email', required=True)
    phone_number = forms.IntegerField(widget=forms.NumberInput, label='Phone Number', required=True)
    staff_id_number = forms.CharField(max_length=50, label='Staff Id Number', required=True)

    gender = forms.CharField(widget=forms.Select(choices=genders), max_length=10, label='Gender', required=False)
    date_of_birth = forms.DateField(label='Date Of Birth', widget=forms.SelectDateWidget(years=years), required=False)

    nationality = forms.CharField(max_length=50, label='Nationality', required=False)
    state_of_origin = forms.CharField(max_length=20, label='State Of Origin', required=False)
    lga = forms.CharField(max_length=50, label='LGA', required=False)

    photo = forms.ImageField(label='Profile Photo', required=False)

    department = forms.CharField(widget=forms.Select(choices=departments), max_length=255, required=True)
    designation = forms.CharField(max_length=255, required=True)

    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if user_model.objects.filter(email=email).exists():
    #         raise forms.ValidationError('Email Already Exists')  # Username or email already exist
    #     return email
    #
    # def clean_phone_number(self):
    #     phone_number = self.cleaned_data['phone_number']
    #     if staff_profile_model.objects.filter(phone_number=phone_number).exists():
    #         raise forms.ValidationError('Phone_number Already Exists')  # Username or email already exist
    #     return phone_number
