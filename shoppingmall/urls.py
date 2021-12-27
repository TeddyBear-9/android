from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

# 定义视图处理的路由器
router = DefaultRouter()
router.register(r'users', views.UsersViewSet)
router.register(r'community/subscribe', views.CommunitySubscribeListViewSet)
router.register(r'community/posts', views.PostViewSet)
router.register(r'malls/category', views.MallCategoryProduceListViewSet)
router.register(r"malls/produces", views.BaseProduceDetailViewSet)
router.register(r'malls/orders', views.OrderDetailViewSet)
router.register(r'users/orders', views.UserOrdersListViewSet)
router.register(r'users/myposts', views.UserMyPostsListViewSet)
router.register(r'users/likeposts', views.UserLikePostsListViewSet)
router.register(r'users/carts', views.UserCartViewSet)
router.register(r'users/address', views.UserDefaultAddressViewSet)

urlpatterns = [
    # re_path(r'^users/(?P<uid>\d+)$', views.UsersViewSet.as_view(actions=)),  # 用户详情视图
    # path('me/login/', views.login, name='login'),
    path(r'malls/', views.MallProduceListView.as_view(), name="malls"),
    path(r'community/recommend/', views.CommunityListView.as_view(), name="community/recommend"),
    path(r'community/posts/comments/', views.PostCommentsCreateView.as_view(), name="user-comment-post"),
    path(r'community/posts/like', views.PostLikeCreateView.as_view(), name='like-post'),
    path(r'login/', views.LoginOrRegisterView.as_view(), name='login'),
    path(r'register/', views.LoginOrRegisterView.as_view(), name='register'),
    path(r'malls/produces/comments/', views.ProduceCommentsCreateView.as_view(), name="user-comment-produce"),
    # path(r'community/posts/', views.PostCreateView.as_view(), name="create_post", namespace='swagger_ignore')

]
urlpatterns += router.urls

