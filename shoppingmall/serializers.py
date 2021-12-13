from django.db.models import Min
from .models import *
from rest_framework import serializers


class UserDetailSerializer(serializers.ModelSerializer):
    """用户详细信息序列化器"""
    class Meta:
        model = Users
        fields = ['id', 'name', 'email', 'phone', 'subscribe_num', 'fan_num', 'icon']


class UserListSerializer(serializers.ModelSerializer):
    """用户简单信息序列化器"""
    class Meta:
        model = Users
        fields = ['id',
                  'name',
                  'icon']


class OrderListSerizalizer(serializers.ModelSerializer):
    """订单简单信息序列化器"""
    produce = serializers.SerializerMethodField("get_produce")

    class Meta:
        model = Order
        fields = ['id', 'quantity', 'status', 'produce']

    def get_produce(self, obj):
        ser_produce = BaseProduceDetailSerializer(instance=obj.produce)
        return ser_produce.data


class UsersOrderListSerializer(serializers.ModelSerializer):
    """用户全部订单序列化器"""
    orders = serializers.SerializerMethodField("get_all_orders")

    class Meta:
        model = Users
        fields = ['orders']

    def get_all_orders(self, obj):
        orders = Order.objects.filter(user=obj.id)
        ser_orders = OrderListSerizalizer(instance=orders, many=True)
        return ser_orders.data


class UsersMyPostListSeriazlizer(serializers.ModelSerializer):
    """用户发布的所有帖子序列化器"""
    posts = serializers.SerializerMethodField("get_my_posts")

    class Meta:
        model = Users
        fields = ['posts']

    def get_my_posts(self, obj):
        posts = Post.objects.filter(user=obj.id)
        ser_posts = PostListSerializer(instance=posts, many=True)
        return ser_posts.data


class UserLikePostsListSeriazlizer(serializers.ModelSerializer):
    """用户喜欢的所有帖子序列化器"""
    posts = serializers.SerializerMethodField("get_like_posts")

    class Meta:
        model = Users
        fields = ['id', 'posts']

    def get_like_posts(self, obj):
        likes = PostLike.objects.filter(user=obj).select_related('post')
        all_posts = set()
        for like in likes:
            all_posts.add(like.post)
        ser_posts = PostListSerializer(instance=all_posts, many=True)
        return ser_posts.data


class CartItemSerizalier(serializers.ModelSerializer):
    produce = serializers.SerializerMethodField('get_produce')
    """购物车项序列化器"""
    class Meta:
        model = CartItem
        fields = [
            'produce',
            'quantity'
        ]

    def get_produce(self, obj):
        return ProduceDetailSerializer(instance=obj.produce).data


class UserShoppingCartSerizalizer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField("get_items")

    class Meta:
        model = Users
        fields = ["items"]

    def get_items(self, obj):
        items = CartItem.objects.filter(user=obj.id)
        return CartItemSerizalier(instance=items, many=True).data


class LoginOrRegisterSerizalizer(serializers.Serializer):
    """登录注册序列化器"""
    type = serializers.CharField(max_length=10, help_text="login表示登录，register表示注册")
    error = serializers.CharField(max_length=10, read_only=True, required=False)
    name = serializers.CharField(max_length=20, required=True)
    password = serializers.CharField(max_length=20, write_only=True)
    id = serializers.IntegerField(read_only=True, required=False)

    def validate(self, data):
        type = data.get("type")
        username = data.get("name", None)
        password = data.get("password", None)
        # 登录检测是否存在该用户名，并检查密码是否正确
        if type == "login":
            if not Users.objects.filter(name=username).exists():
                raise serializers.ValidationError("用户名不存在", code='authorization')
            elif not Users.objects.filter(name=username, password=password).exists():
                raise serializers.ValidationError('用户名或者密码错误', code='authorization')
        # 注册检测是否已存在用户，创建新用户
        elif type == "register":
            if Users.objects.filter(name=username).exists():
                raise serializers.ValidationError("用户名已存在，请更换", code='authorization')
            else:
                user = Users(name=username, password=password)
                user.save(force_insert=True)
        # 处理异常情况
        else:
            raise serializers.ValidationError("访问方式有误", code='authorization')

        # 访问成功则添加用户id字段返回前端
        data['id'] = Users.objects.get(name=username, password=password).id
        return data


class ProduceImageSerializer(serializers.ModelSerializer):
    """商品图片序列化器"""
    class Meta:
        model = ProduceImages
        fields = ['order_number', 'image']


class ProduceCommentSerializer(serializers.ModelSerializer):
    """商品评论序列化器"""
    user = serializers.SerializerMethodField("get_user")

    class Meta:
        model = ProduceComment
        fields = ['user',
                  'commentTime',
                  'comment_like_num',
                  'star',
                  ]

    def get_user(self, obj):
        ser_user = UserListSerializer(instance=obj.order.user)
        return ser_user.data


class ProduceDetailSerializer(serializers.ModelSerializer):
    """子商品详情序列化器"""
    produce_name = serializers.SerializerMethodField("get_parent_name")

    class Meta:
        model = Produce
        fields = ['produce_name',
                  'child_name',
                  'price',
                  ]

    def get_parent_name(self, obj):
        parent = Produce.objects.get(id=obj.id).parent_produce

        return parent.name


class ProduceListSerializer(serializers.ModelSerializer):
    """子商品简单信息序列化器"""
    class Meta:
        model = Produce
        fields = ['child_name',
                  'price']


class BaseProduceDetailSerializer(serializers.ModelSerializer):
    """商品详情序列化器"""
    images = serializers.SerializerMethodField("get_pic_url_list")
    comments = serializers.SerializerMethodField("get_comment_list")
    sub_produce = serializers.SerializerMethodField('get_sub_produce')

    class Meta:
        model = BaseProduce
        fields = ['name',
                  'sales_num',
                  'comment_num',
                  'images',
                  'comments',
                  'sub_produce']

    def get_pic_url_list(self, obj):
        pics = ProduceImages.objects.filter(produce=obj.id)
        ser_pics = ProduceImageSerializer(instance=pics, many=True)
        return ser_pics.data

    def get_comment_list(self, obj):
        comments = ProduceComment.objects.filter(base_produce=obj.id).order_by('star')
        ser_comments = ProduceCommentSerializer(instance=comments, many=True)
        return ser_comments.data

    def get_sub_produce(self, obj):
        subs = Produce.objects.filter(parent_produce=obj.id)
        ser_subs = ProduceListSerializer(instance=subs, many=True)
        return ser_subs.data


class MallProduceListSerializer(serializers.ModelSerializer):
    """商城首页获取商品最低价格序列化器"""
    min_price = serializers.FloatField(required=True)

    class Meta:
        model = Produce
        fields = ['min_price']


class MallBaseProduceListSerializer(serializers.ModelSerializer):
    """商城首页获取商品最低价格序列化器"""
    
    price = serializers.SerializerMethodField('get_min_price')
    surface = serializers.SerializerMethodField('get_surface')

    class Meta:
        model = BaseProduce
        fields = ['id', 'name', 'price', 'surface']

    # 用于获取商城首页展示商品的最小价格
    def get_min_price(self, obj):
        all_price = Produce.objects.filter(parent_produce=obj.id).aggregate(min_price=Min('price'))
        ser_price = MallProduceListSerializer(all_price)
        return ser_price.data.get("min_price")

    # 用于获取商品的首页展示图片
    def get_surface(self, obj):
        pic = ProduceImages.objects.get(produce=obj.id, order_number=1)
        ser_pic = ProduceImageSerializer(instance=pic)
        return ser_pic.data.get("image")


class PostImageSerializer(serializers.ModelSerializer):
    """帖子图片序列化器"""
    class Meta:
        model = PostImages
        fields = ['order_number', 'image']

class PostCommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField("get_user")
    class Meta:
        model = PostComments
        fields = ['user',
                  'content',
                  'timestamp',]

    def get_user(self, obj):
        return UserListSerializer(instance=obj.user).data

class PostListSerializer(serializers.ModelSerializer):
    """帖子简单信息序列化器"""
    surface = serializers.SerializerMethodField("get_surface")
    user = serializers.SerializerMethodField("get_user")

    class Meta:
        model = Post
        fields = ['user',
                  'title',
                  'like_num',
                  'content',
                  'surface']

    def get_surface(self, obj):
        pic = PostImages.objects.get(post=obj.id, order_number=1)
        ser_pic = PostImageSerializer(instance=pic)
        return ser_pic.data.get("image")

    def get_user(self, obj):
        ser_user = UserListSerializer(instance=obj.user)
        return ser_user.data


class PostDetailSerializer(serializers.ModelSerializer):
    """帖子详情序列化器"""
    user = serializers.SerializerMethodField("get_user")
    images = serializers.SerializerMethodField("get_images")
    comments = serializers.SerializerMethodField("get_comments")

    class Meta:
        model = Post
        fields = ['user',
                  'title',
                  'like_num',
                  'content',
                  'images',
                  'comments']

    def get_user(self, obj):
        ser_user = UserListSerializer(instance=obj.user)
        return ser_user.data

    def get_images(self, obj):
        images = PostImages.objects.filter(post=obj.id)
        return PostImageSerializer(instance=images, many=True).data

    def get_comments(self, obj):
        comments = PostComments.objects.filter(post=obj.id)
        return PostCommentSerializer(instance=comments, many=True).data

class CommunitySubscribeListSerializer(serializers.ModelSerializer):
    """社区订阅序列化器"""
    subscribe_posts = serializers.SerializerMethodField("get_subscribe_posts")

    class Meta:
        model = Users
        fields = ['id', 'subscribe_posts']

    def get_subscribe_posts(self, obj):
        subscribe = Fans.objects.filter(fan=obj.id)
        all_posts = Post.objects.none()
        for each in subscribe:
            posts = Post.objects.filter(user=each.user)
            all_posts = posts | all_posts
        ser_all_posts = PostListSerializer(instance=all_posts, many=True)
        return ser_all_posts.data


class CategoryProduceListSerializer(serializers.ModelSerializer):
    """商品固定分类序列化器"""
    produces = serializers.SerializerMethodField("get_category_produces")

    class Meta:
        model = Category
        fields = ['name', 'produces']

    def get_category_produces(self, obj):
        produces = BaseProduce.objects.filter(category=obj.name, is_active=True)
        ser_produces = MallBaseProduceListSerializer(instance=produces, many=True)
        return ser_produces.data

