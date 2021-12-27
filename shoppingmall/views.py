from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, RetrieveAPIView, \
    UpdateAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from .serializers import *
from .models import *


class UsersViewSet(RetrieveUpdateDestroyAPIView,
                   viewsets.GenericViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    # def get_queryset(self):


class MallProduceListView(ListAPIView):
    serializer_class = MallBaseProduceListSerializer
    queryset = BaseProduce.objects.filter(is_active=True)


class CommunityListView(ListAPIView):
    serializer_class = PostListSerializer
    queryset = Post.objects.filter(is_active=True)


class CommunitySubscribeListViewSet(viewsets.GenericViewSet,
                                    RetrieveAPIView):
    serializer_class = CommunitySubscribeListSerializer
    queryset = Users.objects.all()


class MallCategoryProduceListViewSet(viewsets.GenericViewSet,
                                     RetrieveAPIView):
    serializer_class = CategoryProduceListSerializer
    queryset = Category.objects.all()


class UserOrdersListViewSet(viewsets.GenericViewSet,
                                    RetrieveAPIView):
    serializer_class = UsersOrderListSerializer
    queryset = Users.objects.all()


class UserMyPostsListViewSet(viewsets.GenericViewSet,
                                    RetrieveAPIView):
    serializer_class = UsersMyPostListSeriazlizer
    queryset = Users.objects.all()


class UserLikePostsListViewSet(viewsets.GenericViewSet,
                                    RetrieveAPIView):
    serializer_class = UserLikePostsListSeriazlizer
    queryset = Users.objects.all()


class PostDetailViewSet(ModelViewSet):
    serializer_class = PostDetailSerializer
    queryset = Post.objects.all()

    def get_queryset(self):
        post_id = self.request.query_params.get('id', None)
        queryset = Post.objects.all()
        if post_id is not None:
            return queryset.filter(id=post_id)
        else:
            return queryset
