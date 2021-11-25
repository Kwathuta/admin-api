# from rest_framework.test import APITestCase
# from django.urls import reverse

# from apps.superadmin.models import Employee, Role

# class TestSetUp(APITestCase):

#     def setUp(self):
#         self.create_user_url = reverse('register')
#         self.login_url = reverse('login')
#         self.change_role = reverse('change_role')
#         if len(Role.objects.all()) < 4:
#             Role.objects.create(name="super_admin")
#             Role.objects.create(name="human_resources")
#             Role.objects.create(name="subordinate_staff")
#             Role.objects.create(name="finance")

#         self.super_user = Employee.objects.create_superuser(email = 'mbiraken17@gmail.com',surname = "kenmbira",password = "1234")

#         self.normal_user_data = {
#             'email':'email@gmail.com',
#             'surname':'mbira',
#             'password':'1234',
#             'country':'Kenya',
#             'national_id':1234,
#             'date_of_birth':'2021-11-25',
#             'other_names':'Ken',
#             'employee_id':'1234'
#         }
#         self.super_user_data = {
#             'email':'mbiraken17@gmail.com',
#             'password':'1234'
#         }
#         return super().setUp()

#     def tearDown(self):
#         return super().tearDown()
