from django.http import response
from apps.superadmin.tests.test_setup import TestSetUp
from apps.superadmin.models import *
from rest_framework import status
from django.core import mail

from apps.superadmin.tokens import *
from apps.superadmin.models import *
from apps.human_resource.models import *

class TestViews(TestSetUp):
    """Tests for superadmin module

    Args:
        TestSetUp ([type]): [description]
    """

    def test_roles_creation(self):
        """This test if all the roles are created on app initialization
        """
        self.assertTrue(Role.objects.all().count(),4)

    def test_company_creation(self):
        """This tests if a company can be created
        """
        res = self.client.post(self.create_company_url,self.company_details)

        self.assertEqual(res.status_code,status.HTTP_201_CREATED)

        my_company = Company.objects.get(name = self.company_details['company_name'])
        self.assertTrue(my_company is not None)

    def test_login_without_activating_token(self):
        """This will test a user loggin in without activating their account
        """
        self.client.post(self.create_company_url,self.company_details)

        res = self.client.post(self.login_url,self.first_super_admin)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

        user = Employee.objects.get(is_active=False)
        self.assertTrue(user is not None)

    def test_activate_account(self):
        """This will test the activate account functionality
        """
        self.client.post(self.create_company_url,self.company_details)
        self.assertEqual(len(mail.outbox), 1)
        response = self.client.get(mail.outbox[0].body)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_create_user_while_unauthorised(self):
        """This tests if a user can create an employee without credentials
        """
        res = self.client.post(self.login_url,self.normal_user_data)
        self.assertEqual(res.status_code, 400)

    def authenticate(self,user_data):
        response = self.client.post(self.login_url,user_data)
        self.client.credentials(HTTP_AUTHORIZATION = f"Token {response.data['token']}")

    def test_create_user_while_authorised(self):
        """This will tes if a user can be created
        """
        self.client.post(self.create_company_url,self.company_details)
        self.client.get(mail.outbox[0].body)
        self.authenticate(self.first_super_admin)
        res = self.client.post(self.create_user_url,self.normal_user_data)
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)

    def test_change_role(self):
        """This will test if a user's role can be changed
        """
        self.client.post(self.create_company_url,self.company_details)
        self.client.get(mail.outbox[0].body)
        self.authenticate(self.first_super_admin)
        self.client.post(self.create_user_url,self.normal_user_data)

        user = Employee.objects.get(email = self.normal_user_data['email'])
        role = Role.objects.get(name="human_resources")

        role_changer = {
            'user':user.pk,
            'role':role.pk
        }

        response = self.client.post(self.change_role_url,role_changer)

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        user_now = Employee.objects.get(email = self.normal_user_data['email'])
        self.assertEqual(user_now.role,role)

    def test_change_role_for_self(self):
        """This will test if a user's role can be changed by the same user
        """
        self.client.post(self.create_company_url,self.company_details)
        self.client.get(mail.outbox[0].body)
        self.authenticate(self.first_super_admin)

        user = Employee.objects.get(email = self.first_super_admin['email'])
        role = Role.objects.get(name="human_resources")

        role_changer = {
            'user':user.pk,
            'role':role.pk
        }

        response = self.client.post(self.change_role_url,role_changer)

        self.assertTrue(response.status_code == status.HTTP_403_FORBIDDEN)

    def test_create_super_user(self):
        """This will test if an initial superuser can be created
        """
        self.client.post(self.create_company_url,self.company_details)
        self.client.get(mail.outbox[0].body)
        self.authenticate(self.first_super_admin)
        user = Employee.objects.get(email = self.first_super_admin['email'])
        self.assertTrue(user.role.name == "super_admin")

    def test_change_role_for_other_company(self):
        """This will check if a user can change the role of an employee for another company
        """

        self.client.post(self.create_company_url,self.company_details)
        self.client.get(mail.outbox[0].body)
        self.authenticate(self.first_super_admin)
        self.client.post(self.create_user_url,self.normal_user_data)

        other_company_details = {
            "first_name": "Roy",
            "last_name": "Rasugu",
            "company_name": "Rasugu Technologies",
            "work_email": "rasugu@company.com",
            "number_of_staff": "0-50",
            "country": "Kenya",
            "password": "1234"
        }

        other_normal_user_data = {
            "department": 1,
            "employment_type": 1,
            "position": "manager",
            "employment_date": "2021-11-25",
            "gross_salary": "100",
            "marital_status": "married",
            "emergency_contact": "Ken",
            "emergency_contact_number": "0755626990",
            "bank_name": "Equity",
            "bank_branch": "Nakuru",
            "account_number": "1234567",
            "phone_number": "0732443604",
            "surname": "Aisha",
            "employee_id": "14",
            "date_of_birth": "2021-11-25",
            "country": "Kenya",
            "email": "aisha@gmail.com",
            "other_names": "Ahmed",
            "national_id": "12347674",
            "password": "1234"
        }

        self.client.post(self.create_company_url,other_company_details)

        Employee(surname=other_normal_user_data['surname'],employee_id = other_normal_user_data['employee_id'],other_names=other_normal_user_data['other_names'],email = other_normal_user_data['email'],national_id = other_normal_user_data['national_id'],date_of_birth = other_normal_user_data['date_of_birth'],country = other_normal_user_data['country'],role = Role.objects.get(name="subordinate_staff")).save()
        company = Company.objects.get(name='Rasugu Technologies')
        other_normal_user = Employee.objects.get(email = other_normal_user_data['email'])
        employee_employment = EmploymentInformation.objects.get(employee = other_normal_user)
        employee_employment.company = company
        employee_employment.save()
        other_normal_user = Employee.objects.get(email = other_normal_user_data['email'])
        
        role = Role.objects.get(name="human_resources")

        role_changer = {
            'user':other_normal_user.pk,
            'role':role.pk
        }

        response = self.client.post(self.change_role_url,role_changer)

        self.assertTrue(response.status_code == status.HTTP_403_FORBIDDEN)

    def test_delete_user(self):
        """This tests if a user can be deleted
        """
        self.client.post(self.create_company_url,self.company_details)
        self.client.get(mail.outbox[0].body)
        self.authenticate(self.first_super_admin)
        self.client.post(self.create_user_url,self.normal_user_data)

        user = Employee.objects.get(email = self.normal_user_data['email'])

        user_data = {
            "user":str(user.pk)
        }

        response = self.client.put(self.delete_user_url,user_data)

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        user_now = Employee.objects.get(email = self.normal_user_data['email'])
        self.assertEqual(user_now.is_active,False)

    def test_reinstate_user(self):
        """This tests if a user can be deleted
        """
        self.client.post(self.create_company_url,self.company_details)
        self.client.get(mail.outbox[0].body)
        self.authenticate(self.first_super_admin)
        self.client.post(self.create_user_url,self.normal_user_data)

        user = Employee.objects.get(email = self.normal_user_data['email'])

        user_data = {
            "user":str(user.pk)
        }

        self.client.put(self.delete_user_url,user_data)
        self.client.put(self.delete_user_url,user_data)

        user_now = Employee.objects.get(email = self.normal_user_data['email'])
        self.assertEqual(user_now.is_active,True)

    def test_other_user_delete_superuser(self):
        """This will check if another user who is not a superuser can delete a superuser
        """
        self.client.post(self.create_company_url,self.company_details)
        self.client.get(mail.outbox[0].body)
        self.authenticate(self.first_super_admin)
        self.client.post(self.create_user_url,self.normal_user_data)

        change_to_hr = Employee.objects.get(email=self.first_super_admin['email'])
        change_to_hr.role = Role.objects.get(name="human_resources")
        change_to_hr.save()


        user = Employee.objects.get(email = self.normal_user_data['email'])
        user.role = Role.objects.get(name="super_admin")
        user.save()

        user_data = {
            "user":str(user.pk)
        }

        response = self.client.put(self.delete_user_url,user_data)

        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)