# Views for the User API

# rest_framework offers a lot of the logic that we need for creating objects in the database by providing base cases that we can use for our views while also providing tools to override behavior if necessary
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
# Importing out customer AuthTokenSerializer from user/serializers.py to link the serializer and the associated view
from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)

#CreateAPIView handles an http post request that is designed for creating objects in db
# All we need to do is define is the serializer and set the serializer class on this view so django_restframework knows what serializer we want to use
class CreateUserView(generics.CreateAPIView):
    # Create a new user in the system
    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    # Create a new auth token for user
    # Customizing the serializer to use our custom AuthTokenSerializer because we want to use email rather than username
    serializer_class = AuthTokenSerializer
    # Allows us to use browsable user interface (not enabled by default)
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
