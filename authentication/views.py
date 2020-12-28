from django.shortcuts import render
from rest_framework import generics,status,views
from .serializers import UserSerializers,EmailVerificationSerializer,LoginSerializer,ResendTokenSerializer,RequestPasswordResetSerializer,SetNewPasswordSerializer
from .models import User
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import login,authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,smart_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode

# Create your views here.

class RegisterView(generics.GenericAPIView):

    serializer_class = UserSerializers
    queryset = User.objects.all()


    def get(self,request):
        allUsrers = self.get_queryset()
        serializer = self.serializer_class(allUsrers,many=True)
        return Response(serializer.data)

    def post(self,request):
        print("user 1")
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception = True)
        print("user creation start")
        serializer.save()
        user_data = serializer.data
        registerUser = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(registerUser).access_token
        relatedUrl = 'http://'+get_current_site(request).domain+reverse('verify_email')+'?token='+str(token)

        email_body = 'Hi '+ registerUser.username+" plaese use the below link to verify account "+relatedUrl

        data = {
            'email_subject':'verify your email',
            'email_body': email_body,
            'user_email':registerUser.email
        }
        Is_Sended = Util.send_mail(data)
        print(Is_Sended)
            

        return Response(user_data,status = status.HTTP_201_CREATED)

class VerifyEmail(views.APIView):

    serializer_class = EmailVerificationSerializer

    
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY,description='Description',type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self,request):
        print(request.user)
        user_token = request.GET.get('token','')
        try:
            payLoad = jwt.decode(user_token,settings.SECRET_KEY)
            print(payLoad)
            user = User.objects.get(id = payLoad['user_id'])
            print(request.user)
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response({'email':'email verified successfully'},status= status.HTTP_200_OK)
            else:
                return Response({'email':'email is already verified'},status= status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error':'token expired'},status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError:
            return Response({'error':'invalid token'},status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data

        return Response(serializer.data,status=status.HTTP_200_OK)

class RequestPasswordResetApiView(generics.GenericAPIView):
    serializer_class = RequestPasswordResetSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        print("sravan")
        email = request.data.get('email','')
        try:
            user = User.objects.get(email =email)
            print("hi")
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            print("hi1")
            token = PasswordResetTokenGenerator().make_token(user)
            print("hi2")
            related_url = 'http://'+get_current_site(request).domain+reverse('PasswordTokenCheckApi',kwargs={'uidb64':uidb64,'token':token})
            email_body = 'Hello '+ user.username+" plaese use the below link to reset_password "+related_url
            data = {
                'email_subject':'Reset  your password',
                'email_body': email_body,
                'user_email':user.email
             }
            Util.send_mail(data)
            return Response({'success':'mail sened succesfully'}, status=status.HTTP_200_OK)

                                                                                    
        except:
            return Response({'error':'mail not succesfully'}, status=status.HTTP_200_OK)


class PasswordTokenCheckApi(views.APIView):
    def get(self,request,uidb64,token):
        try:
            id=smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                return Response({'error':'Token is not valid'})
            else:
                return Response({'success':True,'message':'credntials are valid','uidb64':uidb64,'token':token},status=status.HTTP_200_OK)

        except:
            return Response({'error':'invalid Token'},status=status.HTTP_400_BAD_REQUEST)

class SetNewPasswordApiView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    def patch(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success':'Password Changed Successfully'},status=status.HTTP_200_OK)

class ResendVerifyEmailAPIView(generics.GenericAPIView):
    serializer_class = ResendTokenSerializer
    
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.data)
        email = serializer.data['email']
        user  = User.objects.get(email=email)

        token = RefreshToken.for_user(user).access_token
        relatedUrl = 'http://'+get_current_site(request).domain+reverse('verify_email')+'?token='+str(token)

        email_body = 'Hi '+ user.username+" plaese use the below link to verify account "+relatedUrl

        data = {
            'email_subject':'verify your email',
            'email_body': email_body,
            'user_email':user.email
        }
        Is_Sended = Util.send_mail(data)

        return Response({'success':'mail sended successfully'},status=status.HTTP_200_OK)