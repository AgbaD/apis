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
            link += token + "/"
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


# Misc


class AllMovies(APIView):

    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetMovie(APIView):

    def get(self, request, pk):
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Http404
        serializer = MovieSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)


# make payment
# get receipt


# ADMIN ~Formed by running `python manage.py createsuperuser`~


class CreateMovie(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        if not request.user.is_staff:
            return Response({'detail': 'You are not authorised to perform action'}, status=status.HTTP_401_UNAUTHORIZED)
        data['user_id'] = request.user.id
        serializer = MovieSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Http404

    def put(self, request, pk):
        if not request.user.is_staff:
            return Response({'detail': 'You are not authorised to perform action'}, status=status.HTTP_401_UNAUTHORIZED)
        movie = self.get_object(pk)
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not request.user.is_staff:
            return Response({'detail': 'You are not authorised to perform action'}, status=status.HTTP_401_UNAUTHORIZED)
        movie = self.get_object(pk)
        movie.delete()
        return Response({'detail': 'Movie deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class GetUsers(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        all_users = []
        for user in users:
            user_dict = {
                'user_name': user.username,
                'firstname': user.first_name,
                'lastname': user.last_name,
                'id': user.id
            }
            all_users.append(user_dict)
        return Response(all_users, status=status.HTTP_200_OK)


