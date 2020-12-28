from django.urls import path
from .views import ExpensesSummaryAPIView

urlpatterns = [
    path('',ExpensesSummaryAPIView.as_view(),name='expenseSummary'),
]