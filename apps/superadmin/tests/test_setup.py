from rest_framework.test import APITestCase
from django.urls import reverse

from apps.superadmin.models import Employee, Role

class TestSetUp(APITestCase):

    def setUp(self):
        self.create_user_url = reverse('register')
        self.login_url = reverse('login')
        self.change_role_url = reverse('change_role')
        self.create_company_url = reverse('register_company')
        if len(Role.objects.all()) < 4:
            Role.objects.create(name="super_admin")
            Role.objects.create(name="human_resources")
            Role.objects.create(name="subordinate_staff")
            Role.objects.create(name="finance")

        self.company_details = {
            "first_name": "Maxwell",
            "last_name": "Munene",
            "company_name": "Big Max Technologies",
            "work_email": "user@company.com",
            "number_of_staff": "0-50",
            "country": "Kenya",
            "password": "1234"
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
