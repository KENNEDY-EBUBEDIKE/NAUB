from django.db import models
from django.urls import reverse
# from django.contrib.contenttypes.fields import GenericRelation


class StaffProfile(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.BigIntegerField(unique=True, null=True)

    surname = models.CharField(max_length=255, null=True)
    first_name = models.CharField(max_length=255, null=True)
    other_name = models.CharField(max_length=255, null=True)

    staff_id_number = models.CharField(unique=True, max_length=255, null=True)

    gender = models.CharField(null=True, max_length=10)
    date_of_birth = models.DateField(null=True)

    nationality = models.CharField(null=True, max_length=20)
    state_of_origin = models.CharField(null=True, max_length=20)
    lga = models.CharField(null=True, max_length=50)

    photo = models.ImageField(upload_to='image/', null=True)

    rfid_code = models.CharField(unique=True, blank=True, null=True, default=None, max_length=20)

    department = models.CharField(max_length=255, null=True)
    designation = models.CharField(max_length=255, null=True)

    reg_date = models.DateTimeField(auto_now_add=True)
    last_scan = models.DateTimeField(auto_now_add=True)

    is_flaged = models.CharField(null=True, max_length=200, default=None)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    ''' Creating s string representation of the user '''
    def __str__(self):
        return self.surname

    class Meta:
        ordering = ('first_name',)

    def get_staff_deactivation_url(self):
        return reverse("deactivate_staff", kwargs={"staff_id": self.pk})

    def get_staff_profile_url(self):
        return reverse("staff_full_profile", kwargs={"staff_id": self.pk})

    def get_flag_staff_url(self):
        return reverse("flag_staff", kwargs={"staff_id": self.pk})


class StaffWorkAttendance(models.Model):
    staff = models.ForeignKey('StaffProfile',
                              on_delete=models.CASCADE,
                              related_name='staff_work_attendance',
                              null=False)
    sign_in_time = models.DateTimeField(auto_now_add=True)
    sign_out_time = models.DateTimeField(null=True)

    def __str__(self):
        return self.staff

    class Meta:
        ordering = ('sign_in_time',)

    def get_delete_work_attendance_url(self):
        return reverse("delete_work_attendance", kwargs={"attendance_id": self.pk})

    def get_staff_profile_update_url(self):
        return reverse("staff_profile_update", kwargs={"staff_id": self.pk})


class ScanRecords(models.Model):
    staff = models.ForeignKey('StaffProfile', on_delete=models.CASCADE, null=True, related_name='scan_records')
    scan_time = models.DateTimeField(auto_now_add=True)
    location = models.CharField(null=True, max_length=50, blank=True, default='T.Y Buratai Gate')

    class Meta:
        ordering = ('scan_time',)

    def __str__(self):
        return self.staff.staff_id_number
