from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

# 定义视图处理的路由器
router = DefaultRouter()
router.register(r'users', views.UsersViewSet)
router.register(r'community/subscribe', views.CommunitySubscribeListViewSet)
router.register(r'malls/category', views.MallCategoryProduceListViewSet)
router.register(r'users/orders', views.UserOrdersListViewSet)
router.register(r'users/myposts', views.UserMyPostsListViewSet)
router.register(r'users/likeposts', views.UserLikePostsListViewSet)

urlpatterns = [
    # re_path(r'^users/(?P<uid>\d+)$', views.UsersViewSet.as_view(actions=)),  # 用户详情视图
    # path('me/login/', views.login, name='login'),
    path(r'malls/', views.MallProduceListView.as_view(), name="malls"),
    path(r'community/recommend/', views.CommunityListView.as_view(), name="community/recommend"),
]
urlpatterns += router.urls
