from django.utils.translation import gettext as _
from django.contrib.auth import logout
from django.contrib.auth import get_user_model

from rest_framework import permissions, exceptions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from party.account.serializers import RegisterSerializer, UserMeSerializer, UserSerializer
from party.api_auth.forms import LoginForm, ActivateAccountForm, ResendActivationForm

User = get_user_model()


class LoginView(APIView):
    def post(self, request):
        result = LoginForm(request.data).save()

        if result['status'] == 'error':
            return Response(status=400, data=result['data'])

        user, token = result['data']
        serializer = UserMeSerializer(user, context={'request': request})
        user.save()

        return Response(serializer.data)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        user = request.user
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            raise exceptions.NotFound(_('User is not signed in'))
        logout(request)
        token.delete()

        return Response({'status': 'success'})


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)


class ActivateAccountView(APIView):
    def post(self, request):
        result = ActivateAccountForm(request.data).save()

        if result['status'] == 'error':
            return Response(status=400, data=result['data'])

        user = result['data']

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        token = user.get_token()
        serializer = UserSerializer(user, context={'request': request})

        result = serializer.data
        result['token'] = token.key

        return Response(result)


class ResendActivationCodeView(APIView):
    def post(self, request):
        response = ResendActivationForm(request.data).save()
        if response['status'] == 'error':
            return Response(status=400, data=response['data'])
        return Response({'status': 'success', 'activation_code': response['data']})
