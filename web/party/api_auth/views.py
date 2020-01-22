from django.utils.translation import gettext as _
from django.contrib.auth import logout
from django.contrib.auth import get_user_model

from rest_framework import permissions, exceptions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from party.account.serializers import RegisterSerializer, UserMeSerializer, UserSerializer
from party.api_auth.forms import LoginForm, ActivateAccountForm, ResendActivationForm, LostPasswordForm, \
    CreateNewPasswordForm

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


class LostPasswordRequestView(APIView):
    def post(self, request):
        response = LostPasswordForm(request.data).save()
        if response['status'] == 'error':
            return Response(status=400, data=response['data'])
        return Response({'status': 'success', 'activation_code': response['data']})


class CreateNewPasswordView(APIView):
    def post(self, request):
        response = CreateNewPasswordForm(request.data).save()

        if response['status'] == 'error':
            return Response(status=400, data=response['data'])

        user, token = response['data']

        serializer = UserSerializer(user, context={'request': request})

        result = serializer.data
        result['token'] = token
        user.save_last_login()

        return Response(result, status=201)


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        data = request.data.copy()
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        if not request.user.check_password(old_password):
            return Response(status=400, data={'old_password': [_('Wrong old password provided'), ]})
        request.user.set_password(new_password)
        request.user.save()
        return Response({'status': 'success'})

