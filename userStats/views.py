from django.shortcuts import render
from expenses.models import Expenses
import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Sum

# Create your views here.

class ExpensesSummaryAPIView(APIView):

    def get_categories(self,expenses):
        return expenses.category

    def get_categories_totalAMount(self,category,expense):
        totalAmount = expense.filter(category__iexact=category).aggregate(amount = Sum('amount'))
        print(totalAmount)
        return totalAmount


    def get(self,request):
        today_date = datetime.date.today()
        aYearAgo = today_date-datetime.timedelta(days=30*12)
        expense = Expenses.objects.filter(owner=request.user,date__gte=aYearAgo,date__lte=today_date)
        categories = list(set(map(self.get_categories,expense)))
        final = {}
        print(categories)
        for category in categories:
            final[category] = self.get_categories_totalAMount(category,expense)

        return Response({'category_data':final},status=status.HTTP_200_OK)


