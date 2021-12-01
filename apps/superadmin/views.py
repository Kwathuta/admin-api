from rest_framework.response import Response
from rest_framework.schemas import get_schema_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
from apps.superadmin.serializers import *
from apps.superadmin.permissions import *

class UserView(APIView):
    """This handles user functionality

    Args:
        generics ([type]): [description]
    """
    schema = get_schema_view()
    permission_classes = [IsAuthenticated & CreateUserPermission]

    @swagger_auto_schema(request_body=CreateEmployeeSerializer)
    def post(self,request,format=None):
        data = {}
        serializer = CreateEmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(request)
            data['success'] = "The account was successfully created"
            responseStatus = status.HTTP_201_CREATED
            return Response(data,status = responseStatus)

        else:
            data = serializer.errors
            print(data)
            responseStatus = status.HTTP_400_BAD_REQUEST
            return Response(data,status = responseStatus)

class LoginView(APIView):
    """This handles a user login request

    Args:
        APIView ([type]): [description]

    Returns:
        [type]: [description]
    """
    @swagger_auto_schema(request_body=LoginSerializer,responses={200: GetUserSerializer()})
    def post(self,request,format=None):
        data = {}
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validate_user()
            data['user'] = GetUserSerializer(user).data
            token, created = Token.objects.get_or_create(user=user)
            data['token'] = token.key
            responseStatus = status.HTTP_200_OK
            return Response(data,status = responseStatus)

        else:
            data = serializer.errors
            return Response(data,status = status.HTTP_400_BAD_REQUEST)

class UserDetailsView(APIView):
    """This returns a user instance depending on the token given

    Args:
        APIView ([type]): [description]

    Returns:
        [type]: [description]
    """
    @swagger_auto_schema(responses={200: UserDetailsSerializer()})
    def get(self,request,token):
        data = {}
        try:
            validated_token = Token.objects.get(key=token)
            data['user'] = UserDetailsSerializer(validated_token.user).data
            responseStatus = status.HTTP_200_OK
        except Exception as e:
            print(e)
            data['error'] = e
            responseStatus = status.HTTP_404_NOT_FOUND

        return Response(data,status=responseStatus)

class EmployeeDetailsView(APIView):
    """This gets the details of one employee according to the id given

    Args:
        APIView ([type]): [description]

    Returns:
        [type]: [description]
    """
    @swagger_auto_schema(responses={200: UserDetailsSerializer()})
    def get(self,request,id):
        data = {}
        try:
            user = Employee.objects.get(pk=id)
            data['user'] = UserDetailsSerializer(user).data
            responseStatus = status.HTTP_200_OK
        except Exception as e:
            print(e)
            data['error'] = e
            responseStatus = status.HTTP_404_NOT_FOUND

        return Response(data,status=responseStatus)

class ChangeRole(APIView):
    """[summary]

    Args:
        APIView ([type]): [description]
    """
    permission_classes = [IsAuthenticated & ChangeRolePermission]

    @swagger_auto_schema(request_body=SetRoleSerializer)
    def post(self,request,format=None):
        data = {}
        serializer = SetRoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data['success'] = "The user's role was successfully updated"
            responseStatus = status.HTTP_200_OK


        else:
            data = serializer.errors
            responseStatus = status.HTTP_400_BAD_REQUEST

        return Response(data,status = responseStatus)

class DeleteUser(APIView):
    """[summary]

    Args:
        APIView ([type]): [description]
    """
    permission_classes = [IsAuthenticated & DeleteUserPermission]

    @swagger_auto_schema(request_body=DeleteUserSerializer)
    def put(self,request,format=None):
        data = {}
        serializer = DeleteUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data['success'] = "The user's status was successfully updated"
            responseStatus = status.HTTP_200_OK


        else:
            data = serializer.errors
            responseStatus = status.HTTP_400_BAD_REQUEST

        return Response(data,status = responseStatus)


class RoleView(APIView):
    """This retrieves a list of roles

    Args:
        APIView ([type]): [description]
    """

    def get(self,request,format=None):
        data = {}
        data['roles'] = RoleSerializer(Role.objects.all(),many=True).data
        return Response(data,status = status.HTTP_200_OK)

class RoleEmployeeView(APIView):
    """This retrieves a list of employees in a company that are in a given role

    Args:
        APIView ([type]): [description]

    Returns:
        [type]: [description]
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: UserDetailsSerializer()})
    def get(self,request,role_id):
        data = {}

        try:
            role = Role.objects.get(pk = role_id)

            employees = Employee.objects.filter(employmentinformation__company = request.user.employmentinformation.company,role = role)
            data['employees'] = UserDetailsSerializer(employees,many=True).data
            responseStatus = status.HTTP_200_OK
        except:
            data["error"] = "There was an error parsing your request"
            responseStatus = status.HTTP_404_NOT_FOUND

        return Response(data,responseStatus)

class CompanyCreation(APIView):
    """A company creation endpoint

    Args:
        APIView ([type]): [description]

    Returns:
        [type]: [description]
    """
    @swagger_auto_schema(request_body=CompanyCreationSerializer)
    def post(self,request,format=None):
        data = {}
        serializer = CompanyCreationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(request)
            data['success'] = "The company has been registered successfully"
            responseStatus = status.HTTP_201_CREATED

        else:
            data = serializer.errors
            responseStatus = status.HTTP_400_BAD_REQUEST

        return Response(data,status = responseStatus)


from django.contrib.auth import login
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from apps.superadmin.tokens import account_activation_token

class ActivateAccount(APIView):
    def get(self, request, uidb64, token, *args, **kwargs):
        data = {}
        try:
            uid = uidb64
            user = Employee.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Employee.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            data['success'] = "Your account was successfully activated"

            return Response(data,status = status.HTTP_200_OK)
        else:
            data = 'The confirmation link was invalid, possibly because it has already been used.'
            return Response(data,status.HTTP_400_BAD_REQUEST)

class EmployeeFiltersView(APIView):
    """This returns a list of employees in a company that fit within a set filter

    Args:
        APIView ([type]): [description]
    """

    def get(self,request,employment_type_id,department_id,employment_status):
        data = {}
        try:
            company = Company.objects.get(pk = request.user.employmentinformation.company.pk)

        except:
            data['error'] = "Your company was not found!"
            return Response(data,status.HTTP_404_NOT_FOUND)

        if employment_type_id > 0 and department_id > 0:
            employment_type = EmploymentType.objects.get(pk = employment_type_id)
            department = Department.objects.get(pk = department_id)

            employees = Employee.objects.filter(employmentinformation__company = request.user.employmentinformation.company,employmentinformation__employment_type = employment_type,employmentinformation__department = department).exclude(national_id__exact="")

        elif employment_type_id > 0:
            employment_type = EmploymentType.objects.get(pk = employment_type_id)
            employees = Employee.objects.filter(employmentinformation__company = request.user.employmentinformation.company,employmentinformation__employment_type = employment_type).exclude(national_id__exact="")

        elif department_id > 0:
            department = Department.objects.get(pk = department_id)
            employees = Employee.objects.filter(employmentinformation__company = request.user.employmentinformation.company,employmentinformation__department = department).exclude(national_id__exact="")

        else:
            if employment_status == "active":
                employees = Employee.objects.filter(employmentinformation__company = request.user.employmentinformation.company).exclude(national_id__exact="").exclude(is_active = False)

            elif employment_status == "terminated":
                employees = Employee.objects.filter(employmentinformation__company = request.user.employmentinformation.company).exclude(national_id__exact="").exclude(is_active = True)

            else:
                employees = Employee.objects.filter(employmentinformation__company = request.user.employmentinformation.company).exclude(national_id__exact="")


        data['employees'] = UserDetailsSerializer(employees,many=True).data
        responseStatus = status.HTTP_200_OK

        return Response(data,responseStatus)
