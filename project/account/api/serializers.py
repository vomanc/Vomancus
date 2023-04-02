""" My serializers """
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from account.models import AccountsModel


class AccountSerializers(serializers.ModelSerializer):
    """ View account """
    class Meta:
        model = AccountsModel
        fields = (
            'first_name', 'last_name', 'username', 'email',
            'gender', 'twitter', 'mastodon', 'signal',
            'github', 'date_of_birth'
        )


class RegistrationSerializers(serializers.ModelSerializer):
    """ Account Registration """
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=AccountsModel.objects.all())])
    password1 = serializers.CharField(write_only=True, required=True,
                                      validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = AccountsModel
        fields = ('username', 'password1', 'password2', 'email')
        extra_kwargs = {
            'username': {'required': True},
            # 'password1': {'required': True}
        }

    def validate(self, attrs):
        """ Check validate """
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = AccountsModel.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user
