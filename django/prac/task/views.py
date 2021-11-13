import uuid
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import jwt, os
import hashlib
from .models import Player
from .serializer import PlayerSerializer, PlayerRegSerializer
from datetime import datetime, timedelta
from dotenv import load_dotenv
from functools import wraps

load_dotenv()
# Create your views here.


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        print()
        print(token)
        print()
        if not token:
            return Response({
                'msg': 'error',
                'detail': 'Access token is missing!'
            }, status=status.HTTP_401_UNAUTHORIZED)

        try:
            data = jwt.decode(token, os.getenv('KEY'), algorithms=['HS256'])
            user = Player.objects.get(public_id=data['pid'])
        except:
            return Response({
                'msg': 'error',
                'detail': 'Access token is invalid!'
            }, status=status.HTTP_401_UNAUTHORIZED)
        return f(user, *args, **kwargs)
    return decorated


def hash_password(password):
    return hashlib.sha512(password.encode()).hexdigest()


class Register(APIView):

    def post(self, request):
        data = request.data
        data['public_id'] = str(uuid.uuid4())
        serializer1 = PlayerRegSerializer(data=data)
        serializer2 = PlayerSerializer(data=data)
        if serializer1.is_valid():
            serializer1.save()
            return Response(serializer2.initial_data, status=status.HTTP_201_CREATED)
        return Response(serializer1.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):

    def post(self, request):
        data = request.data
        if not Player.objects.filter(email=data['email']).exists():
            return Response({
                'msg': 'error',
                'detail': 'Email is incorrect!'
            }, status=status.HTTP_400_BAD_REQUEST)

        player = Player.objects.get(email=data['email'])
        print(PlayerSerializer(player).data)
        if data['password'] != player.password:
            return Response({
                'msg': 'error',
                'detail': 'Password is incorrect!'
            }, status=status.HTTP_400_BAD_REQUEST)
        token = jwt.encode({
            'pid': player.public_id,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, os.getenv('KEY'), 'HS256')
        return Response({
            'msg': 'success',
            'data': {
                'token': token
            }
        }, status=status.HTTP_200_OK)


class Profile(APIView):

    @token_required
    def get(self, user, request):
        serializer = PlayerSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
