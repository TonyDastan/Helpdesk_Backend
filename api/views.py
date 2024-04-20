from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.models import User
from api.serializers import CustomUserSerializer
from rest_framework.response import Response
from rest_framework import status

class RegisterUser(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        data = request.data
        print(data)
        serializer = CustomUserSerializer(data=data)
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
