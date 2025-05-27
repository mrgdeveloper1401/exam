from rest_framework import viewsets, permissions, mixins, views, response, generics

from accounts.models import User
from . import serializers
from .permissions import NotAuthenticated


class UserRegisterViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = serializers.UserRegisterSerializer
    permission_classes = (NotAuthenticated,)


class UserLoginView(views.APIView):
    serializer_class = serializers.UserLoginSerializer
    permission_classes = (NotAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # get token after validated data
        token = serializer.validated_data['token']
        role = serializer.validated_data['tole']
        is_staff = serializer.validated_data['is_staff']
        return response.Response(
            {
                'token': token,
                "is_staff": is_staff,
                "role": role
            }
        )


class RequestOtpView(generics.CreateAPIView):
    serializer_class = serializers.RequestOtpSerializer
    permission_classes = (NotAuthenticated,)
    queryset = User.objects.only(
        "phone_number"
    )


class RequestOtpVerifyView(views.APIView):
    serializer_class = serializers.RequestVerifyOtpSerializer
    permission_classes = (NotAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']
        return response.Response(token)


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AdminUserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()

    def get_queryset(self):
        if not self.request.user.is_staff:
            return self.queryset.filter(id=self.request.user.id)
        else:
            return super().get_queryset()

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return self.serializer_class
        else:
            return serializers.UserProfileSerializer
