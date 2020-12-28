from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .serializers import ExpensesSerializers
from .models import Expenses
from rest_framework import permissions
from .permissions import IsOwner

# Create your views here.

class ExpensesListApiView(ListCreateAPIView):
    queryset= Expenses.objects.all()
    serializer_class = ExpensesSerializers
    permissions_classes = (permissions.IsAuthenticated,)

    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class ExpensesDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset= Expenses.objects.all()
    serializer_class = ExpensesSerializers
    permissions_classes = (permissions.IsAuthenticated,IsOwner)

    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    
