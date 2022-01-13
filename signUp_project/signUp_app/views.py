from .models import BaseUser
from .serializer import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import api_view
import jwt
import datetime


@api_view(['GET', 'POST'])
def OperationUser(request):
    if request.method == 'POST':
        user = BaseUser.objects.create_user(email=request.data['email'],
                                            password=request.data['password'])
        user.is_opsuser = True
        user.save()
        serializer = UserSerializer(user)
        return Response({"data": serializer.data, "message": "Successfully created operations user"},
                        status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def ClientUser(request):
    if request.method == 'POST':
        user = BaseUser.objects.create_user(email=request.data['email'],
                                            password=request.data['password'])
        user.is_clientuser = True
        user.save()
        serializer = UserSerializer(user)
        return Response({
            "data": serializer.data,
            "message": "Successfully created client user"
        }, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def login(request):
    email = request.data['email']
    password = request.data['password']

    user = BaseUser.objects.filter(email=email).first()

    if user is None:
        raise AuthenticationFailed('USER Not found')

    if not user.check_password(password):
        raise AuthenticationFailed('incorrect Password')

    payload = {
        'id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, 'secret', algorithm='HS256')

    response = Response()

    response.set_cookie(key='jwt', value=token, httponly=True)
    response.data = {
        'jwt': token
    }

    return response


@api_view(['GET', 'POST'])
def getdata(request):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')

    user = BaseUser.objects.filter(id=payload['id']).first()
    serializer = UserSerializer(user)

    return Response(serializer.data)


@api_view(['GET', 'POST'])
def logout(request):
    response = Response()
    response.delete_cookie('jwt')
    response.data = {
        'message': 'logged out successfully '
    }

    return response
