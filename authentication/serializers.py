from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate,login
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,smart_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode

class UserSerializers(serializers.ModelSerializer):
    password = serializers.CharField(max_length=20,min_length=6,write_only=True)
    class Meta:
        model = User
        fields = ['email','username','password']

    def validate(self,attrs):
        email = attrs.get('email','')
        username = attrs.get('username','')

        if not username.isalnum():
            raise serializers.ValidationError('Only alpha numeric is allowed')

        return attrs
    def create(self,validated_data):
        print("user creation")
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=1000)

    class Meta:
        model=User
        fields=['token']

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100,min_length=10)
    password = serializers.CharField(min_length=6,write_only=True)
    username = serializers.CharField(max_length=100,min_length=10,read_only=True)
    tokens = serializers.CharField(max_length=100,min_length=10,read_only=True)

    class Meta:
        model = User
        fields=['email','password','username','tokens']

    def validate(self,attrs):
        email = attrs.get('email','')
        password = attrs.get('password','')

        if email is None or password is None:
            raise serializers.ValidationError("please enter proper crendtials")
        else:
            user = authenticate(email=email,password=password)

            if not user:
                raise AuthenticationFailed('please confirm your crendtials')
            elif not user.is_active:
                raise AuthenticationFailed('your login is diabled please contact admin')

            return{
                'email':user.email,
                'username':user.username,
                'tokens':user.tokens
            }

class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6,write_only=True)
    token = serializers.CharField(min_length=1,write_only=True)
    uidb64 = serializers.CharField(min_length=1,write_only=True)

    def validate(self,attrs):
        uidb64 = attrs.get('uidb64')
        token = attrs.get('token')
        password = attrs.get('password')

        id = smart_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)
        if not PasswordResetTokenGenerator().check_token(user,token):
            raise AuthenticationFailed('The token is expired')
        else:
            user.set_password(password)
            user.save()
            return (user)

class ResendTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']

    def validate(self,attrs):
            email = attrs.get('email')
            print(email)

            if email is None:
                raise serializers.ValidationError('please enter proper email addres')
            else:
                try:
                    user= User.objects.get(email=email)
                    print(user)
                    return {
                        'email':user.email
                    }
                except User.DoesNotExist:
                    raise serializers.ValidationError('no user found please enter proper email')

                except:
                    raise serializers.ValidationError('user with this email not found')

    
