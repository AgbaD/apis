import jwt, os
from .models import Movie
from django.http import Http404
from .serializers import MovieSerializer
from django.contrib.auth.models import User, auth

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# Create your views here.

# User


class Register(APIView):

    def post(self, request):
        data = request.data
        email = data['email'].lower()
        firstname = data['firstname']
        lastname = data['lastname']
        password = data['password']

        if User.objects.filter(email=email).exists():
            return Response({"msg": "Email has already been used"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                user = User.objects.create_user(
                    username=email,
                    first_name=firstname,
                    last_name=lastname,
                    email=email,
                    password=password
                )
                Token.objects.create(user=user)
                return Response({"msg": "Account created successfully"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(e.message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdatePassword(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        data = request.data
        if user.check_password(data['password']):
            user.set_password(data['new_password'])
            user.save()
            return Response({'msg': 'Password has been changed'}, status=status.HTTP_202_ACCEPTED)
        return Response({"msg": "Previous password is incorrect"}, status=status.HTTP_401_UNAUTHORIZED)


class ForgotPassword(APIView):

    def post(self, request):
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            secret = os.getenv('JWT_SECRET') or "khfdogifkjhbldjhfkbv"
            token = jwt.encode({'email': email}, secret, algorithm='HS256')
            link = request.build_absolute_uri('/change_password/')  # change_password_from_forgot_password
            link += token
            return Response({'link': link}, status=status.HTTP_200_OK)
        else:
            return Response({'msg': "User not found. Please check email"}, status=status.HTTP_404_NOT_FOUND)


class ChangePasswordFromForgot(APIView):

    def put(self, request, payload):
        secret = os.getenv('JWT_SECRET') or "khfdogifkjhbldjhfkbv"
        tok = jwt.decode(payload, secret, algorithms=['HS256'])
        email = tok['email']
        password = request.data['password']
        user = User.objects.get(email=email)
        if user:
            user.set_password(password)
            user.save()
            return Response({'msg': 'Password has been changed'}, status=status.HTTP_202_ACCEPTED)
        return Response({'msg': 'Link is faulty, please check'}, status=status.HTTP_400_BAD_REQUEST)


# get all movies
# get movie
# buy ticket
# get receipt


# ADMIN ~Formed by running `python manage.py createsuperuser`~
# create movie
# edit movie
# delete movie

