from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password_confirm= serializers.CharField(write_only=True, required= True)
    """Serializers for user object"""
    class Meta:
        model= get_user_model()
        fields= ('email', 'password', 'password_confirm')
        extra_kwargs= {'password':{'write_only':True, 'min_length':8}}
    def validate(self, attrs):
        password= attrs.get('password')
        password_confirm= attrs.get('password_confirm')
        if password!=password_confirm:
            raise serializers.ValidationError('Passwords do not match.')
        del attrs['password_confirm']
        return attrs
    def create(self, validated_data):
        """Create a new user with encrypted password and return it."""
        return get_user_model().objects.create_user(**validated_data)
    
class AuthTokenSerializer(serializers.Serializer):
    """Serializer for user authentication object."""
    email= serializers.EmailField()
    password= serializers.CharField(
        style= { 'input_type': 'password' },
        trim_whitespace= False
    )
    def validate(self, attrs):
        """Validate and authenticate users."""
        email= attrs.get('email')
        password= attrs.get('password')

        user= authenticate(
            request= self.context.get('request'),
            username=email,
            password= password
        )
        if not user:
            msg= _('Invalid credentials. Please try again.')
            raise serializers.ValidationError(msg, code='authentication')
        attrs['user']=user
        return attrs
