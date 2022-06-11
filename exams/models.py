from django.db import models
from django.urls import reverse
from unixtimestampfield.fields import UnixTimeStampField


class AttendanceSheet(models.Model):
    student = models.ForeignKey(
        'students.StudentProfile',
        on_delete=models.CASCADE,
        null=True,
        related_name='student_attendance_sheet'
    )

    course = models.ForeignKey(
        'students.Course',
        null=True, on_delete=models.CASCADE,
        related_name='exam_attendance_sheet'
    )

    sign_in_time = UnixTimeStampField(blank=True, null=True)
    sign_out_time = UnixTimeStampField(blank=True, null=True)
    has_written = models.BooleanField(default=False)

    class Meta:
        ordering = ('course',)

    def __str__(self):
        return self.student

    def get_delete_attendance_url(self):
        return reverse("delete_attendance", kwargs={"attendance_id": self.pk})


class InvigilatorAttendanceSheet(models.Model):
    invigilator = models.ForeignKey(
        'staff.StaffProfile',
        on_delete=models.CASCADE,
        null=True,
        related_name='invigilator_attendance_sheet'
    )

    course = models.ForeignKey(
        'students.Course',
        null=True,
        on_delete=models.CASCADE,
        related_name='invigilator_attendance_sheet'
    )

    sign_in_time = models.DateTimeField(auto_now_add=True)
    sign_out_time = models.DateTimeField(null=True, default=None)

    class Meta:
        ordering = ('course',)

    def __str__(self):
        return self.invigilator

    # def get_delete_attendance_url(self):
    #     return reverse("delete_attendance", kwargs={"attendance_id": self.pk})


class ExaminationRequest(models.Model):
    course = models.OneToOneField('students.Course',
                                  on_delete=models.CASCADE,
                                  null=True,
                                  related_name='examination_request')
    requested_by = models.ForeignKey('users.User',
                                     on_delete=models.CASCADE,
                                     null=True, related_name='examination_request')
    request_date = models.DateTimeField(auto_now_add=True)

    status = models.CharField(blank=False, null=False, max_length=20, default='PENDING')

    approved_by = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True,
                                    related_name='examination_request_approval')
    approved_start_time = models.DateTimeField(null=True)
    approved_stop_time = models.DateTimeField(null=True)

    invigilators = models.ManyToManyField('staff.StaffProfile',
                                          related_name='examination_invigilator')

    class Meta:
        ordering = ('request_date',)

    def __str__(self):
        return self.course.course_code

    def get_decline_exam_request_url(self):
        return reverse("decline_exam_request", kwargs={"exam_request_id": self.pk})

    def get_delete_exam_request_url(self):
        return reverse("delete_exam_request", kwargs={"exam_request_id": self.pk})


class ExaminationMalpractice(models.Model):
    student = models.ForeignKey('students.StudentProfile',
                                on_delete=models.CASCADE,
                                null=True,
                                related_name='exam_malpractice')

    course = models.ForeignKey('students.Course',
                               null=True, on_delete=models.CASCADE,
                               related_name='exam_malpractice')

    invigilator = models.ForeignKey('staff.StaffProfile',
                                    null=True,
                                    on_delete=models.CASCADE,
                                    related_name='exam_malpractice')

    time_of_act = models.DateTimeField(auto_now_add=True)

    details = models.CharField(blank=True, null=True, max_length=1000)

    exhibit = models.FileField(upload_to='file/', null=True)

    class Meta:
        ordering = ('student',)

    def __str__(self):
        return self.student.first_name
