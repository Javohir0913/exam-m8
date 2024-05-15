from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


UserModel = get_user_model()


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(style={'input_type': 'password'})
    code = serializers.CharField(max_length=8)


class ConfirmPassword(serializers.Serializer):
    confirm_password = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = ConfirmPassword(write_only=True)

    def validate(self, data):
        if data['password'] != data['confirm_password']['confirm_password']:
            print(data['confirm_password']['confirm_password'])
            raise serializers.ValidationError({"confirm_password": "Password and confirm password fields must match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        user = UserModel.objects.create_user(**validated_data)
        return user

    class Meta:
        model = UserModel
        fields = ('username', 'email', 'password', 'confirm_password', 'first_name', 'last_name', 'photo',
                  'birth_day', 'organization', 'another_information', 'scientific_degree')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'first_name', 'last_name', 'email', 'date_joined', 'last_login', 'photo')
        read_only_fields = ('date_joined', 'last_login')
        extra_kwargs = {
            'email': {'required': False},
        }