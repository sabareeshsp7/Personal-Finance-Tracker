from django.shortcuts import render
import datetime
from django.contrib.auth import authenticate
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Expense

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, ExpenseSerializer
from .models import User

from .models import Budget
from .serializers import BudgetSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

class LoginView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response({"error": "Wrong Credentials"}, status=400)

class LogoutView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response({"success": "Successfully logged out."})


class FinancialReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        expenses = Expense.objects.filter(user=request.user)
        if start_date:
            expenses = expenses.filter(date__gte=start_date)
        if end_date:
            expenses = expenses.filter(date__lte=end_date)

        total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        expenses_by_category = expenses.values('category').annotate(total=Sum('amount'))

        return Response({
            'total_expenses': total_expenses,
            'expenses_by_category': expenses_by_category
        })

class DashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        expenses = Expense.objects.filter(user=request.user)
        total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        expenses_by_category = expenses.values('category').annotate(total=Sum('amount'))
        recent_expenses = expenses.order_by('-date')[:5]

        return Response({
            'total_expenses': total_expenses,
            'expenses_by_category': expenses_by_category,
            'recent_expenses': ExpenseSerializer(recent_expenses, many=True).data
        })
        
    

class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BudgetAlertView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        budgets = Budget.objects.filter(user=request.user)
        alerts = []

        for budget in budgets:
            total_expenses = Expense.objects.filter(
                user=request.user,
                category=budget.category,
                date__month=datetime.now().month
            ).aggregate(Sum('amount'))['amount__sum'] or 0

            if total_expenses > budget.amount:
                alerts.append({
                    'category': budget.category,
                    'budget': budget.amount,
                    'spent': total_expenses,
                    'overspent': total_expenses - budget.amount
                })

        return Response(alerts)