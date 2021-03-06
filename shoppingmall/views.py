from rest_framework import viewsets, status, mixins
from rest_framework.mixins import CreateModelMixin
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, RetrieveAPIView, \
    UpdateAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
    GenericAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import *
from .models import *


class UsersViewSet(RetrieveUpdateDestroyAPIView,
                   viewsets.GenericViewSet, ):
    queryset = Users.objects.all()
    serializer_class = UserDetailSerializer


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


class UserCartViewSet(viewsets.GenericViewSet,
                      RetrieveAPIView):
    queryset = Users.objects.all()
    serializer_class = UserShoppingCartSerizalizer


class LoginOrRegisterView(CreateAPIView):
    serializer_class = LoginOrRegisterSerizalizer
    queryset = Users.objects.all()

    def post(self, request, *args, **kwargs):
        serializers = LoginOrRegisterSerizalizer(data=request.data)

        if not serializers.is_valid(raise_exception=True):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(data=serializers.data, status=status.HTTP_200_OK)


class MallProduceListView(ListAPIView):
    serializer_class = MallBaseProduceListSerializer
    queryset = BaseProduce.objects.filter(is_active=True)


class MallCategoryProduceListViewSet(viewsets.GenericViewSet,
                                     RetrieveAPIView,):
    serializer_class = CategoryProduceListSerializer
    queryset = Category.objects.all()


class BaseProduceDetailViewSet(viewsets.GenericViewSet,
                               RetrieveAPIView):
    serializer_class = BaseProduceDetailSerializer
    queryset = BaseProduce.objects.all()


class CommunityListView(ListAPIView):
    serializer_class = PostListSerializer
    queryset = Post.objects.filter(is_active=True)


class CommunitySubscribeListViewSet(viewsets.GenericViewSet,
                                    RetrieveAPIView):
    parser_classes = [MultiPartParser, ]
    serializer_class = CommunitySubscribeListSerializer
    queryset = Users.objects.all()


class PostViewSet(viewsets.GenericViewSet,
                  RetrieveAPIView, DestroyAPIView):
    queryset = Post.objects.filter(is_active=True)
    serializer_class = PostDetailSerializer


class PostCreateView(CreateAPIView):

    parser_classes = (MultiPartParser, )
    serializer_class = PostCreateSerializer
    queryset = Post.objects.all()


class OrderDetailViewSet(viewsets.GenericViewSet,
                         RetrieveAPIView,
                         CreateAPIView,
                         UpdateAPIView):
    serializer_class = OrderDetailSerializer
    queryset = Order.objects.all()


class UserDefaultAddressViewSet(viewsets.GenericViewSet,
                                RetrieveAPIView,):
    serializer_class = UserDefaultAddressSerializer
    queryset = Users.objects.all()


class ProduceCommentsCreateView(CreateAPIView):
    serializer_class = CommentCreateSerializer
    queryset = ProduceComment.objects.all()


class PostCommentsCreateView(CreateAPIView):
    serializer_class = PostCommentSerializer
    queryset = PostComments.objects.all()


class PostLikeCreateView(CreateAPIView):
    serializer_class = PostLikeCreateSerializer
    queryset = PostLike.objects.all()



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
