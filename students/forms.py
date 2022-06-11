from django import forms
import datetime
from django.apps import apps

students_profile_model = apps.get_model('students', 'StudentProfile')
courses_model = apps.get_model('students', 'Course')


class StudentRegistrationForm(forms.Form):
    this_year = datetime.date.today().year
    years = range(this_year - 50, this_year + 1)
    faculties = (("Select Faculty", "Select Faculty"),
                 ("ARTS, MANAGEMENT AND SOCIAL SCIENCE", "ARTS, MANAGEMENT AND SOCIAL SCIENCE"),
                 ("ENGINEERING AND TECHNOLOGY", "ENGINEERING AND TECHNOLOGY"),
                 ("COMPUTING", "COMPUTING"),
                 ("NATURAL AND APPLIED SCIENCE", "NATURAL AND APPLIED SCIENCE"),
                 ("ENVIRONMENTAL SCIENCE", "ENVIRONMENTAL SCIENCE"))
    levels = (
        ("Select Level", "Select Level"),
        ("100 Level", "100 Level"),
        ("200 Level", "200 Level"),
        ("300 Level", "300 Level"),
        ("400 Level", "400 Level"),
        ("500 Level", "500 Level")
    )
    sessions = (("Select Session", "Select Session"),
                ("2018/2019", "2018/2019"),
                ("2019/2020", "2019/2020"),
                ("2020/2021", "2020/2021"),
                ("2021/2022", "2021/2022"),
                ("2022/2023", "2022/2023"))
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

    matric_number = forms.CharField(max_length=50, label='Matric Number', required=True)
    faculty = forms.CharField(widget=forms.Select(choices=faculties), max_length=50, label='Faculty', required=True)
    department = forms.CharField(max_length=50, label='Department', required=True)
    session = forms.CharField(widget=forms.Select(choices=sessions), max_length=50, label='Session', required=True)
    level = forms.CharField(widget=forms.Select(choices=levels), max_length=50, label='Level', required=True)

    gender = forms.CharField(widget=forms.Select(choices=genders), max_length=10, label='Gender', required=False)
    date_of_birth = forms.DateField(label='Date Of Birth', widget=forms.SelectDateWidget(years=years), required=True)
    nationality = forms.CharField(max_length=20, label='Nationality', required=False)
    state_of_origin = forms.CharField(max_length=20, label='State Of Origin', required=False)
    lga = forms.CharField(max_length=50, label='LGA', required=False)
    resident_address = forms.CharField(max_length=100, label='Resident Address', required=False)
    photo = forms.ImageField(label='Profile Photo', required=False)

    def clean_matric_number(self):
        matric_number = self.cleaned_data['matric_number']
        if students_profile_model.objects.filter(matric_number=matric_number).exists():
            raise forms.ValidationError('Matric Number Already Exists')
        return matric_number

    def clean_email(self):
        email = self.cleaned_data['email']
        if students_profile_model.objects.filter(email=email).exists():
            raise forms.ValidationError('Email Already Exists')
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if students_profile_model.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError('Phone_number Already Exists')
        return phone_number


class StudentProfileUpdateForm(forms.Form):
    this_year = datetime.date.today().year
    years = range(this_year - 50, this_year + 1)
    faculties = (("Select Faculty", "Select Faculty"),
                 ("ARTS, MANAGEMENT AND SOCIAL SCIENCE", "ARTS, MANAGEMENT AND SOCIAL SCIENCE"),
                 ("ENGINEERING AND TECHNOLOGY", "ENGINEERING AND TECHNOLOGY"),
                 ("COMPUTING", "COMPUTING"),
                 ("NATURAL AND APPLIED SCIENCE", "NATURAL AND APPLIED SCIENCE"),
                 ("ENVIRONMENTAL SCIENCE", "ENVIRONMENTAL SCIENCE"))
    levels = (
        ("Select Level", "Select Level"),
        ("100 Level", "100 Level"),
        ("200 Level", "200 Level"),
        ("300 Level", "300 Level"),
        ("400 Level", "400 Level"),
        ("500 Level", "500 Level")
    )
    sessions = (("Select Session", "Select Session"),
                ("2018/2019", "2018/2019"),
                ("2019/2020", "2019/2020"),
                ("2020/2021", "2020/2021"),
                ("2021/2022", "2021/2022"),
                ("2022/2023", "2022/2023"))
    genders = (
        ("Select Gender", "Select Gender"),
        ("MALE", "MALE"),
        ("FEMALE", "FEMALE")
    )

    first_name = forms.CharField(max_length=50, label='First Name', required=False)
    surname = forms.CharField(max_length=50, label='Surname', required=False)
    other_name = forms.CharField(max_length=50, label='Other Names', required=False)

    email = forms.EmailField(label='Email', disabled=True, required=False)
    phone_number = forms.IntegerField(disabled=True, widget=forms.NumberInput, label='Phone Number', required=False)

    matric_number = forms.CharField(disabled=True, max_length=50, label='Matric Number', required=False)
    faculty = forms.CharField(widget=forms.Select(choices=faculties), max_length=50, label='Faculty', required=False)
    department = forms.CharField(max_length=50, label='Department', required=False)
    session = forms.CharField(widget=forms.Select(choices=sessions), max_length=50, label='Session', required=False)
    level = forms.CharField(widget=forms.Select(choices=levels), max_length=50, label='Level', required=False)

    gender = forms.CharField(widget=forms.Select(choices=genders), max_length=10, label='Gender', required=False)
    date_of_birth = forms.DateField(label='Date Of Birth', widget=forms.SelectDateWidget(years=years), required=False)
    nationality = forms.CharField(max_length=20, label='Nationality', required=False)
    state_of_origin = forms.CharField(max_length=20, label='State Of Origin', required=False)
    lga = forms.CharField(max_length=50, label='LGA', required=False)
    resident_address = forms.CharField(widget=forms.Textarea, label='Resident Address', required=False)
    photo = forms.ImageField(label='Profile Photo', required=False)

    def clean_matric_number(self):
        matric_number = self.cleaned_data['matric_number']
        if students_profile_model.objects.filter(matric_number=matric_number).exists():
            raise forms.ValidationError('Matric Number Already Exists')  # Username or email already exist
        return matric_number

    def clean_email(self):
        email = self.cleaned_data['email']
        if students_profile_model.objects.filter(email=email).exists():
            raise forms.ValidationError('Email Already Exists')  # Username or email already exist
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if students_profile_model.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError('Phone_number Already Exists')  # Username or email already exist
        return phone_number


class CourseAddForm(forms.Form):

    faculties = (("Select Faculty", "Select Faculty"),
                 ("ARTS, MANAGEMENT AND SOCIAL SCIENCE", "ARTS, MANAGEMENT AND SOCIAL SCIENCE"),
                 ("ENGINEERING AND TECHNOLOGY", "ENGINEERING AND TECHNOLOGY"),
                 ("COMPUTING", "COMPUTING"),
                 ("NATURAL AND APPLIED SCIENCE", "NATURAL AND APPLIED SCIENCE"),
                 ("ENVIRONMENTAL SCIENCE", "ENVIRONMENTAL SCIENCE"),
                 ("GENERAL STUDIES", "GENERAL STUDIES"),
                 ("FACULTY", "FACULTY"))

    course_code = forms.CharField(max_length=50, label='Course Code', required=False)
    course_title = forms.CharField(max_length=50, label='Course Title', required=False)

    course_faculty = forms.CharField(widget=forms.Select(choices=faculties),
                                     max_length=50,
                                     label='Course Faculty',
                                     required=False)
    course_department = forms.CharField(max_length=50, label='Course Department', required=False)
    credit_unit = forms.IntegerField(max_value=8, min_value=1, required=True, label='Credit Unit')

    def clean_course_code(self):
        course_code = self.cleaned_data['course_code']
        if courses_model.objects.filter(course_code=course_code).exists():
            raise forms.ValidationError('Course Already Exists')  # Username or email already exist
        return course_code

    def clean_course_title(self):
        course_title = self.cleaned_data['course_title']
        if courses_model.objects.filter(course_title=course_title).exists():
            raise forms.ValidationError('Course Already Exists')  # Username or email already exist
        return course_title
