from rest_framework.test import APITestCase
from django.urls import reverse

from apps.superadmin.models import Role,User

class TestSetUp(APITestCase):

    def setUp(self):
        self.create_user_url = reverse('register')
        self.login_url = reverse('login')
        self.change_role = reverse('change_role')
        if len(Role.objects.all()) < 3:
            Role.objects.create(name="super_admin")
            Role.objects.create(name="human_resources")
            Role.objects.create(name="subordinate_staff")

        self.super_user = User.objects.create_superuser(email = 'mbiraken17@gmail.com',username = "kenmbira",password = "1234")

        self.normal_user_data = {
            'email':'email@gmail.com',
            'username':'email',
            'password':'1234',
            'nationality':'Kenyan',
            'national_id':1234
        }
        self.super_user_data = {
            'email':'mbiraken17@gmail.com',
            'password':'1234'
        }
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
