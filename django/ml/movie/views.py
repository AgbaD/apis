import json, jwt
from .models import Movie
from django.conf import settings
from django.core.email import send_mail
from .serializers import MovieSerializer
from django.contrib.auth.models import User, auth

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
# Authentication


@api_view(['POST'])
def register(request):
    data = request.data
    email = data['email'].lower()
    firstname = data['firstname']
    lastname = data['lastname']
    password = data['password']

    if User.objects.get(email=email).exists():
        return Response(json.dumps({"msg": "Email has already been used"}), status=status.HTTP_400_BAD_REQUEST)
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
            return Response(json.dumps({"msg": "Account created successfully"}), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(e.message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_password(request):
    user = request.user
    data = request.data
    if user.check_password(data['password']):
        user.set_password([data['new_password']])
        user.save()
        return Response(json.dumps({'msg': 'Password has been changed'}), status=status.HTTP_202_ACCEPTED)
    return Response(json.dumps({"msg": "Previous password is incorrect"}), status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def forgot_password(request):
    email = request.data['email']
    if User.objects.get(email=email).exists():
        secret = os.getenv('JWT_SECRET')
        token = jwt.encode({'email': email}, secret, algorithm='HS256')
        link = request.build_absolute_url('/change_password/')



@api_view(['PUT'])
def change_password_from_forgot(request, payload):
    secret = os.getenv('JWT_SECRET')
    tok = jwt.decode(payload, secret, algorithms=['HS256'])
    email = tok['email']
    password = request.data['password']
    user = User.objects.get(email=email)
    if user:
        user.set_password([password])
        user.save()
        return Response(json.dumps({'msg': 'Password has been changed'}), status=status.HTTP_202_ACCEPTED)
    return Response(json.dumps({'msg': 'Link is faulty, please check'}), status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def movie(request, pk=None):
    try:
        mov = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MovieSerializer(mov)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = MovieSerializer(mov, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        mov.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view([ 'GET', 'POST' ])
def movies(request):
    if request.method == 'GET':
        all_movies = Movie.objects.all()
        serializer = MovieSerializer(all_movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
