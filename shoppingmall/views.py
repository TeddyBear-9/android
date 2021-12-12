from rest_framework import viewsets, status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, RetrieveAPIView, \
    GenericAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet

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


class LoginOrRegisterView(CreateAPIView):
    serializer_class = LoginOrRegisterSerizalizer
    queryset = Users.objects.all()

    def post(self, request, *args, **kwargs):
        serializers = LoginOrRegisterSerizalizer(data=request.data)

        if not serializers.is_valid(raise_exception=True):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(data=serializers.data, status=status.HTTP_200_OK)




