from rest_framework import serializers

from accounts.models import User

class RegisterSerializer(serializers.Serializer):
    firstName = serializers.CharField()
    lastName = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.CharField()
    
    def create(self, validated_data):
        user = User(
            first_name = validated_data['firstName'],
            last_name = validated_data['lastName'],
            email = validated_data['email'],
            role = validated_data['role'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def validate(self, validated_data):
        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return validated_data