from rest_framework import serializers
from blog_app.models import Post
from django.contrib.auth.models import User

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'img', 'timestamp']


class UserSerializer(serializers.ModelSerializer):
    #create a field
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only = True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password' : {"write_only": True}
        }

    def save(self):
        user = User()
        user.email = self.validated_data['email']
        user.username = self.validated_data['username']
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({"Password": "The passwords do not match"})
        
        user.set_password('password')
        user.save()
        return user