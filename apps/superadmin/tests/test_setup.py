# from rest_framework.test import APITestCase
# from django.urls import reverse
# from apps.human_resource.models import Department, EmploymentType

# from apps.superadmin.models import Employee, Role

# class TestSetUp(APITestCase):

#     def setUp(self):
#         self.create_user_url = reverse('register')
#         self.login_url = reverse('login')
#         self.change_role_url = reverse('change_role')
#         self.create_company_url = reverse('register_company')
#         if len(Role.objects.all()) < 4:
#             Role.objects.create(name="super_admin")
#             Role.objects.create(name="human_resources")
#             Role.objects.create(name="subordinate_staff")
#             Role.objects.create(name="finance")

#         if len(Department.objects.all()) < 4:
#             Department.objects.create(name="super_admin")
#             Department.objects.create(name="human_resources")
#             Department.objects.create(name="subordinate_staff")
#             Department.objects.create(name="finance")

#         if len(EmploymentType.objects.all()) < 4:
#             EmploymentType.objects.create(name="contract")
#             EmploymentType.objects.create(name="permanent")
#             EmploymentType.objects.create(name="internship")
#             EmploymentType.objects.create(name="consultancy")        

#         self.company_details = {
#             "first_name": "Maxwell",
#             "last_name": "Munene",
#             "company_name": "Big Max Technologies",
#             "work_email": "user@company.com",
#             "number_of_staff": "0-50",
#             "country": "Kenya",
#             "password": "1234"
#         }

#         self.first_super_admin = {
#             "email": "user@company.com",
#             "password": "1234",
#         }

#         self.normal_user_data = {
#             "department": 1,
#             "employment_type": 1,
#             "position": "manager",
#             "employment_date": "2021-11-25",
#             "gross_salary": "100",
#             "marital_status": "married",
#             "emergency_contact": "Philip",
#             "emergency_contact_number": "0758926990",
#             "bank_name": "Equity",
#             "bank_branch": "Nakuru",
#             "account_number": "1234567",
#             "phone_number": "0722443604",
#             "surname": "Kevo",
#             "employee_id": "13",
#             "date_of_birth": "2021-11-25",
#             "country": "Kenya",
#             "email": "kevocb@gmail.com",
#             "other_names": "Gitahi",
#             "national_id": "12345674",
#             "password": "1234"
#         }

#         return super().setUp()

#     def tearDown(self):
#         return super().tearDown()
