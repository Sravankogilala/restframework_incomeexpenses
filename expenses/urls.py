from django.urls import path
from .views import ExpensesListApiView,ExpensesDetailApiView

urlpatterns = [
    path('',ExpensesListApiView.as_view(),name='ExpensesList'),
    path('<int:id>/',ExpensesDetailApiView.as_view(),name='ExpensesDetail'),
]