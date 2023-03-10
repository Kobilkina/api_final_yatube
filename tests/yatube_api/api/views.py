from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Group, Post, Comment, Follow

from .serializers import GroupSerializer, FollowSerializer
from .serializers import PostSerializer, CommentSerializer
from .permissions import ReadOnly

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    #def get_group(self):
    #    group_id = self.kwargs.get('group')
    #    return get_object_or_404(Group, id=group_id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        #serializer.save(author=self.request.user, group=self.get_group())

    def perform_update(self, serializer):
        if self.get_object().author == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied('dont touch')

    def destroy(self, request, pk=None, *args, **kwargs):
        if self.get_object().author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super(PostViewSet, self).destroy(request, pk, *args, **kwargs)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    #def get_permissions(self):
    #    if self.action == 'retrieve':
    #        return (ReadOnly(),)
    #    return super().get_permissions()

    def get_post(self):
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, pk=post_id)

    def get_queryset(self):
        return self.get_post().comments.all().select_related('author', 'post')

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user, post=self.get_post())

    def perform_update(self, serializer):
        if self.get_object().author == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied('dont touch')

    def destroy(self, request, *args, **kwargs):
        if self.get_object().author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super(CommentViewSet, self).destroy(request, *args, **kwargs)


class FollowViewSet(viewsets.ModelViewSet):
    #queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.SearchFilter]
    search_fields = ('following__username',)
    #http_method_names = ["get", "post"]

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    #def get_following(self):
    #    following = self.kwargs.get('following')
    #    return get_object_or_404(User, username=following)

    #def get_queryset(self):
    #    return self.queryset.filter(user=self.request.user)
        #return self.request.user.follower.all()

    #def perform_create(self, serializer):
    #    if 'following' not in self.kwargs:
    #        return Response(status=status.HTTP_400_BAD_REQUEST)
        #following = self.kwargs.get('following')
        #if following == '':
        #    return Response(status=status.HTTP_400_BAD_REQUEST)
        #if self.request.user == self.get_following():
        #    return Response(status=status.HTTP_400_BAD_REQUEST)
    #    serializer.save(user=self.request.user)  #, following=self.get_following())


    #def get_queryset(self):
    #    search = self.kwargs['search']
    #    if search:
    #        return self.queryset.filter(following=search, user=self.request.user)
    #    return self.queryset.filter(user=self.request.user)