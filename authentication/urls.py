from django.urls import path
from .views import RegisterView,VerifyEmail,LoginView,RequestPasswordResetApiView,PasswordTokenCheckApi,SetNewPasswordApiView,ResendVerifyEmailAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/',RegisterView.as_view(),name = 'register'),
    path('verify_email',VerifyEmail.as_view(),name='verify_email'),
    path('Login',LoginView.as_view(),name='login'),
    path('request_password_reset/',RequestPasswordResetApiView.as_view(),name='RequestPasswordResetApiView'),
    path('passwordchecktoken/<uidb64>/<token>/',PasswordTokenCheckApi.as_view(),name='PasswordTokenCheckApi'),
    path('ResetPassword/',SetNewPasswordApiView.as_view(),name='ResetPassword'),
    path('ResendVerifyEmailAPIView/',ResendVerifyEmailAPIView.as_view(),name='ResendVerifyEmailAPIView'),
    path('refreshtoken/',TokenRefreshView.as_view(),name='refreshToken'),
]