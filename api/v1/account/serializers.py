import random

from django.contrib.auth import authenticate
from rest_framework import serializers

from accounts.validation import PhoneNumberValidator
from api.v1.account.token import get_tokens_for_user
from accounts.models import User, Otp


class UserRegisterSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("phone_number", "password", "full_name", "email", "token")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        return User.objects.create_user(
            password=password,
            **validated_data
        )

    def get_token(self, obj):
        request = self.context.get('request')
        # if user is new_user return token
        if request and request.method == 'POST':
            return get_tokens_for_user(obj)
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            "token": data.get("token"),
        }


class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        # authenticate user
        user = authenticate(
            request=self.context.get('request'),
            phone_number=phone_number,
            password=password,
        )

        # invalid phone and password
        if not user:
            raise serializers.ValidationError(
                "phone and password is invalid",
                code='authorization'
            )

        # user inactive
        if not user.is_active:
            raise serializers.ValidationError(
                "This account is inactive.",
                code='inactive'
            )

        # verify user
        # if not user.is_verify:
        #     raise serializers.ValidationError(
        #         "This account is not verified please login as otp",
        #         code='unverified'
        #     )
        token = get_tokens_for_user(user)
        attrs['token'] = token
        attrs['tole'] = user.user_type
        attrs['is_staff'] = user.is_staff
        return attrs


class RequestOtpSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        validators=[PhoneNumberValidator()],
    )

    def create(self, validated_data):
        # get phone
        phone = validated_data.get('phone_number')

        # get request
        request = self.context.get('request')

        # get user
        get_user = User.objects.filter(
            phone_number=phone
        ).only(
            "phone_number"
        )

        # check user
        if get_user:
            return Otp.objects.create(
                phone_number=phone,
                device_ip=request.META.get('REMOTE_ADDR', "X_FORWARDED_FOR"),
                otp_code=random.randint(100000, 999999)
            )
        else:
            raise serializers.ValidationError(
                detail={"message": "your account not exits please signup"},
                code="not_found"
            )

    def to_representation(self, instance):
        return {
            "message": "code send"
        }


class RequestVerifyOtpSerializer(serializers.Serializer):
    otp_phone = serializers.CharField()

    def validate(self, attrs):
        # get object request
        request = self.context.get('request')

        # get opt
        otp = attrs.get("otp_phone")

        # get user ip
        user_ip = request.META.get('REMOTE_ADDR', "X_FORWARDED_FOR")

        # filter otp
        otp = Otp.objects.filter(
            otp_code=otp,
            device_ip=user_ip
        )

        # check otp
        if not otp:
            raise serializers.ValidationError(
                detail={"message": "your otp code is invalid"},
                code="invalid_otp_code"
            )
        else:
            # get obj otp and check expired otp
            otp = otp.first()
            if otp.is_expired:
                raise serializers.ValidationError(
                    detail={"message": "your otp code is expired"},
                    code="expired_otp_code"
                )

            # get obj user
            user = User.objects.filter(phone_number=otp.phone_number).only("phone_number")

            # check user and return token
            if not user:
                raise serializers.ValidationError(
                    detail={"message": "your otp code is invalid"},
                    code="invalid_otp_code"
                )
            else:
                token = get_tokens_for_user(user.last())
                attrs["token"] = token
                otp.delete()
                return attrs


class AdminUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "groups",
            "user_permissions",
            "password"
        )


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "full_name",
            "email",
            "nation_code",
            "is_staff"
        )
        read_only_fields = ("is_staff",)
