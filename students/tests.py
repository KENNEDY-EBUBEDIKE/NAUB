from django.test import TestCase, SimpleTestCase
from django.urls import reverse


class StudentPageTest(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("student-database/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("student_database"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("student_database"))
        self.assertTemplateUsed(response, "students_database.html")

    def test_template_content(self):
        response = self.client.get(reverse("student_database"))
        self.assertContains(response, "<h1>STUDENTS DATABASE</h1>")
        self.assertNotContains(response, "Traceback")
