from django.shortcuts import render
from django.http import JsonResponse
from .models import Approve,Support,Staff,Payroll,Expenses
from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ApproveSerializer,SupportSerializer,StaffSerializer,PayrollSerializer,ExpensesSerializer

# Create your views here.
class ApproveDetail(APIView):  # get, update, delete single employee
   
    def get_object(self, pk):
        try:
            return Approve.objects.get(pk=pk)
        except Approve.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):  # get employee
        notes = self.get_object(pk)
        serializers = ApproveSerializer(notes)
        return Response(serializers.data)

    def put(self, request, pk, format=None):  # update employee
        notes = self.get_object(pk)
        serializers = ApproveSerializer(notes, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):  # delete employee
        notes = self.get_object(pk)
        notes.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ApproveList(APIView):  # get all employee
   

    def get(self, request, format=None):  # get all employee
        all_notes = Approve.objects.all()
        serializers = ApproveSerializer(all_notes, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):  # create new employee
        serializers = ApproveSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageList(APIView):  # get all message
   

    def get(self, request, format=None):  # get all message
        all_message = Support.objects.all()
        serializers = SupportSerializer(all_message, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):  # create new message
        serializers = SupportSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)     

class StaffDetail(APIView):  # get, update, delete single staff
   
    def get_object(self, pk):
        try:
            return Staff.objects.get(pk=pk)
        except Staff.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):  # get employee
        staff = self.get_object(pk)
        serializers = StaffSerializer(staff)
        return Response(serializers.data)

    def put(self, request, pk, format=None):  # update employee
        staff = self.get_object(pk)
        serializers = StaffSerializer(staff, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):  # delete employee
        staff = self.get_object(pk)
        staff.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class StaffList(APIView):  # get all staff
   

    def get(self, request, format=None):  # get all staff
        all_staff = Staff.objects.all()
        serializers = StaffSerializer(all_staff, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):  # create new staff
        serializers = StaffSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)    


class PayDetail(APIView):  # get, update, delete single payroll
   
    def get_object(self, pk):
        try:
            return Payroll.objects.get(pk=pk)
        except Payroll.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):  # get payroll
        pay = self.get_object(pk)
        serializers = PayrollSerializer(pay)
        return Response(serializers.data)

    def put(self, request, pk, format=None):  # update payroll
        pay = self.get_object(pk)
        serializers = PayrollSerializer(pay, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):  # delete payroll
        pay = self.get_object(pk)
        pay.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PayList(APIView):  # get all payroll
   

    def get(self, request, format=None):  # get all payroll
        all_pay = Payroll.objects.all()
        serializers = PayrollSerializer(all_pay, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):  # create new payroll
        serializers = PayrollSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)                 

class ExpensesList(APIView):


    def get(self, request, format=None):
        all_expenses = Expenses.objects.all()
        serializers = ExpensesSerializer(all_expenses, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = ExpensesSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class ExpenseDetail(APIView):  # get, update, delete single expense
   
    def get_object(self, pk):
        try:
            return Expenses.objects.get(pk=pk)
        except Expenses.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):  # get expense
        expay = self.get_object(pk)
        serializers = ExpensesSerializer(expay)
        return Response(serializers.data)

    def put(self, request, pk, format=None):  # put expense
        expay = self.get_object(pk)
        serializers = ExpensesSerializer(expay, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):  # delete expense
        expay = self.get_object(pk)
        expay.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)        

class PayrollView(APIView):
    def get(self, request):
        obj = Payroll.objects.all()
        serializer = PayrollSerializer(obj, many=True)
        return Response(serializer.data, status=200)
    def post(self, request):
        data = request.data
        serializer = PayrollSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)     

class Payrollbyid(APIView):
    def get_object(self, id):
        try:
            return Payroll.objects.get(id=id)
        except Payroll.DoesNotExist as e:
            return Response({"error": "Not found."},status=404)
    def get(self, request, id=None):
        instance = self.get_object(id)
        serializer = PayrollSerializer(instance)
        return Response(serializer.data)
    def put(self, request, id=None):
        data = request.data
        instance = self.get_object(id)
        serializer = PayrollSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    def delete(self, request, id=None):
        instance = self.get_object(id)
        serializer = PayrollSerializer(instance)
        instance.delete()
        return Response(serializer.data)           