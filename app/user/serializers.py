# Serializers for the user API View

from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

from rest_framework import serializers

# ModelSerializers allow us to validate and save things to a model that we define in our serializer
class UserSerializer(serializers.ModelSerializer):
    # Serializer for the user object

    class Meta:
        model = get_user_model()
        # Fields we want to be available in the serializer. What fields should be saved in model that is created. These three items are the minimum that need to be required. We only want to allow fields that can be changed through API (vs. fields like 'is_admin' that we don't want user to be able to provide)
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        # Create and return a user with encrypted password
        # We're overriding method that serializer has for creating a new model object.
        # The default behavior is to create a model object with whatever parameters are passed in.
        # We want password to pass through encryption, so we want to use create_user method so that we can call get_user
        return get_user_model().objects.create_user(**validated_data)

class AuthTokenSerializer(serializers.Serializer):
    # Serializer for the user auth token
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        # "Validate and authenticate the user. This will be called at validation stage when data is posted to our view (data is passed to Serializer, which then validates that the data is correct)"
        email = attrs.get('email')
        password = attrs.get('password')
        # built in django authenticate method.
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs
