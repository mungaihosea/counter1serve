from .serializers import PostSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework import serializers, status
from blog_app.models import Post
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView


#returns all Post requests from the database
@api_view(['GET'])
def api_list_view(request):
    queryset = Post.objects.all()
    serializable_queryset = queryset.values()
    return Response(data = serializable_queryset)


class ApiListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination


#returns a specific blog based on the slug provided
@api_view(['GET'])
#setting the permissions decorator to a blank list makes the endpoint open
#works fot the authorization decorator as well
def api_detail_view(request, slug):
    data = {}
    try:
        serializer = PostSerializer(Post.objects.get(id = slug))
        data = serializer.data
        return Response(data = data)
    except Post.DoesNotExist:
        data['error'] = "An error occured"
        return Response(data = data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_create_view(request):
    data = {}
    user = request.user
    blog_post = Post(user = user)

    serializer = PostSerializer(blog_post, request.data)
    if serializer.is_valid():
        data['success'] = "Blog post created successfully"
        serializer.save()
        return Response(data)
    else:
        return Response(data = serializer.errors)


@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def api_delete_view(request, slug):
    data = {}
    try:
        blog_post = Post.objects.get(id = slug)
        user = request.user
        if blog_post.user != user:
            return Response({"permission denied": "You don't have permission to delete that Post"})
        blog_post.delete()
        data['success'] = "Post deleted successfully"
        return Response(data)

    except Post.DoesNotExist:
        data['error'] = "Post does not exist"
        return Response(data, status.HTTP_404_NOT_FOUND)
    
@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def api_edit_view(request, slug):
    data = {}

    try:
        blog_post = Post.objects.get(id = slug)
        user = request.user

        if blog_post.user != user:
            return Response({"response": "you don't have permission to edit that"})

        serializer = PostSerializer(blog_post, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "post modified successfully"})
        else:
            return Response(serializer.errors)
    except Post.DoesNotExist:
        return Response(data = {"Error": "Post not found"}, status = status.HTTP_404_NOT_FOUND)
    

@api_view(['POST'])
def api_adduser_view(request):
    serializer = UserSerializer(data = request.data)
    if serializer.is_valid():
        user = serializer.save()
        data = {}
        data['response'] = "user added succesfully"
        data['username'] = user.username
        data['email'] = user.email
        token = Token.objects.get(user=user).key
        data['token'] = token
        return Response(data = data)
    else:
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
