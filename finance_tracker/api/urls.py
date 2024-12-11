from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, LogoutView, FinancialReportView, DashboardView
from .views import BudgetViewSet, BudgetAlertView

router = DefaultRouter()
router.register(r'budgets', BudgetViewSet, basename='budget')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('financial-report/', FinancialReportView.as_view(), name='financial-report'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('', include(router.urls)),
    path('budget-alerts/', BudgetAlertView.as_view(), name='budget-alerts'),
]

from .views import FinancialReportView

from .views import BudgetViewSet, BudgetAlertView

router.register(r'budgets', BudgetViewSet, basename='budget')

