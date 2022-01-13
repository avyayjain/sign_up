from .models import BaseUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import api_view
import jwt
import datetime


@api_view(['POST'])
def OperationUser(request):
    email = request.data["email"]
    password = request.data["password"]

    if BaseUser.objects.filter(email = email).exists:
        return Response({
            "message" : "User already exist"
        })
    user = BaseUser.objects.create_user(email = email,password =  password)
    user.is_opsuser = True
    user.save()

    return Response({"message": "Successfully created operations user"},
                    status=status.HTTP_201_CREATED)


@api_view(['POST'])
def ClientUser(request):
    email = request.data["email"]
    password = request.data["password"]
    if BaseUser.objects.filter(email = email).exists:
        return Response({
            "message" : "User already exist"
        })
    user = BaseUser.objects.create_user(email=email, password=password)
    user.is_opsuser = False
    user.save()

    return Response({"message": "Successfully created client user"},
                    status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login(request):
    email = request.data['email']
    password = request.data['password']

    user = BaseUser.objects.filter(email=email).first()
    print(user.check_password(password))

    if user is None:
        raise AuthenticationFailed('USER Not found')

    if user.check_password(password) == True and user.is_opsuser == True:
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token,
            'message': "Ops User Logged in Successfully"
        }

    elif user.check_password(password) == True and user.is_opsuser == False:
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token,
            'message': "Client User Logged in Successfully"
        }
    else:
        response = Response()
        response.data = {
            'message': "Incorrect Password"
        }

    return response




@api_view(['POST'])
def statusclient(request):
    email = request.data.get("email")
    token = request.headers.get("Authorization")
    token = jwt.decode(token, "secret", algorithms=["HS256"])
    user = BaseUser.objects.get(id=token['id'])
    # print(user.is_opsuser)
    client = BaseUser.objects.all()
    if user.is_opsuser:
        cl_user = BaseUser.objects.get(email = email)
        if cl_user:
            if cl_user.is_opsuser:
                return Response({"message": "Sorry , its an Ops user"})
            elif cl_user.is_active:

                cl_user.is_active = False
                cl_user.save()
                return Response({"message": "client with email" + email + " is disabled"})
            else:
                cl_user.is_active = True
                cl_user.save()
                return Response({"message": "client with email" + email + " is enabled"})

        else:
            return Response({"message": "Email doesnt exist"})
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def logout(request):

    response = Response()
    response.delete_cookie('jwt')
    response.data = {
        'message': 'logged out successfully '
    }

    return response
