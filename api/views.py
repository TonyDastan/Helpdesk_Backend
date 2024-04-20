from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.models import User
from api.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token


class RegisterUser(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        data = request.data
        print(data)
        serializer = UserSerializer(data=data)
        if not serializer.is_valid():
            errors = serializer.errors
            return Response({'save': False, 'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            email = data['email']
            user = User.objects.filter(email=email)
            if user:
                return Response({'save': False, 'errors': 'User with this email already exists'},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            message = {'save': True}
            return Response(message)
        
        message = {'save': False, 'errors': serializer.errors}
        return Response(message)


class LoginUser(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        username = request.data.get('username')
        password = request.data.get('password')
        print('Data', username, password)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            user_id = User.objects.get(username=username)
            user_info = UserSerializer(instance=user_id, many=False).data
            token, created = Token.objects.get_or_create(user=user)
            response = {
                'token': token,
                'user': user_info
            }
            return Response(response)
        else:
            response = {
                'msg': 'Invalid username or password',
            }
            return Response(response)


class GetUser(APIView):
    @staticmethod
    def get(request, query_type):
        if query_type == 'single':
            try:
                user_id = request.GET.get('user_id')
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'message': 'User Does Not Exist'})
            return Response(UserSerializer(instance=user, many=False).data)
        elif query_type == 'all':
            queryset = User.objects.all()
            return Response(UserSerializer(instance=queryset, many=True).data)
        else:
            return Response({'message': 'Wrong Request!'})


