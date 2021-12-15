from django.db.models import Min
from .models import *
from rest_framework import serializers


class UserListSerializer(serializers.ModelSerializer):
    """用户简单信息序列化器"""

    class Meta:
        model = Users
        fields = ['id',
                  'name',
                  'icon']
        read_only_fields = ['name',
                            'icon']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'id',
            'address_inf',
            'phone'
        ]


class PostListSerializer(serializers.ModelSerializer):
    """帖子简单信息序列化器"""
    surface = serializers.SerializerMethodField("get_surface")
    user = serializers.CharField(source='user.name')
    user_icon = serializers.ImageField(source='user.icon')

    class Meta:
        model = Post
        fields = ['title',
                  'content',
                  'user_icon',
                  'user',
                  'like_num',
                  'surface']

    def get_surface(self, obj):
        pic = PostImages.objects.get(post=obj.id, order_number=1)
        ser_pic = PostImageSerializer(instance=pic)
        return ser_pic.data.get("image")


class PostLikeListSerializer(serializers.ModelSerializer):
    post = PostListSerializer()

    class Meta:
        model = PostLike
        fields = ['post']


class UserDetailSerializer(serializers.ModelSerializer):
    user_post = PostListSerializer(many=True)
    """用户详细信息序列化器"""

    class Meta:
        model = Users
        fields = ['id',
                  'name',
                  # 'email',
                  # 'phone',
                  'subscribe_num',
                  'fan_num',
                  'icon',
                  'user_post']


class ProduceDetailSerializer(serializers.ModelSerializer):
    """子商品详情序列化器"""
    title = serializers.CharField(source='parent_produce.name')
    surface = serializers.SerializerMethodField('get_surface')

    class Meta:
        model = Produce
        fields = ['title',
                  'child_name',
                  'price',
                  'surface']

    def get_surface(self, obj):
        return ProduceImageSerializer(instance=ProduceImages.objects.get(produce=obj.parent_produce.id,
                                                                         order_number=1)).data.get('image')


class ProduceListSerializer(serializers.ModelSerializer):
    """子商品简单信息序列化器"""

    class Meta:
        model = Produce
        fields = ['child_name',
                  'price']


class OrderListSerializer(serializers.ModelSerializer):
    """订单简单信息序列化器"""
    produce = ProduceDetailSerializer()

    class Meta:
        model = Order
        fields = ['id',
                  'quantity',
                  'status',
                  'produce']


class OrderDetailSerializer(serializers.ModelSerializer):
    # 用于反序列化
    produce_id = serializers.IntegerField(write_only=True, required=True)
    address_id = serializers.IntegerField(write_only=True, required=True)

    produce = ProduceDetailSerializer(read_only=True)
    address = AddressSerializer(read_only=True, )

    class Meta:
        model = Order
        fields = ['id',
                  'produce',
                  'address',
                  'quantity',
                  'status',
                  'paymentTime',
                  'produce_id',
                  'address_id']
        read_only_fields = [
            'produce',
            'address',
            'status',
            'paymentTime'
        ]
        extra_kwargs = {'quantity': {'required': True}}

    def create(self, validated_data):
        address = Address.objects.get(id=validated_data.get('address_id'))
        user = address.user
        produce = Produce.objects.get(id=validated_data.get("produce_id"))

        instance = Order.objects.create(user=user,
                                        produce=produce,
                                        address=address,
                                        quantity=validated_data.get('quantity'),
                                        status="未发货")
        return instance


class UsersOrderListSerializer(serializers.ModelSerializer):
    """用户全部订单序列化器"""
    orders = OrderListSerializer(many=True)

    class Meta:
        model = Users
        fields = ['orders']


class UsersMyPostListSeriazlizer(serializers.ModelSerializer):
    """用户发布的所有帖子序列化器"""
    posts = PostListSerializer(many=True)

    class Meta:
        model = Users
        fields = ['posts']
    #
    # def get_my_posts(self, obj):
    #     posts = Post.objects.filter(user=obj.id)
    #     ser_posts = PostListSerializer(instance=posts, many=True)
    #     return ser_posts.data


class UserLikePostsListSeriazlizer(serializers.ModelSerializer):
    """用户喜欢的所有帖子序列化器"""
    love = PostLikeListSerializer(many=True)

    class Meta:
        model = Users
        fields = ['love']


class CartItemSerizalier(serializers.ModelSerializer):
    produce = ProduceDetailSerializer()
    """购物车项序列化器"""

    class Meta:
        model = CartItem
        fields = [
            'produce',
            'quantity'
        ]


class UserShoppingCartSerizalizer(serializers.ModelSerializer):
    items = CartItemSerizalier(many=True)

    class Meta:
        model = Users
        fields = ["items"]


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


class BaseProduceDetailSerializer(serializers.ModelSerializer):
    """商品详情序列化器"""
    images = ProduceImageSerializer(many=True)
    comments = ProduceCommentSerializer(many=True)
    sub_produce = ProduceListSerializer(many=True)

    class Meta:
        model = BaseProduce
        fields = ['name',
                  'sales_num',
                  'comment_num',
                  'images',
                  'comments',
                  'sub_produce']


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
                  'timestamp', ]

    def get_user(self, obj):
        return UserListSerializer(instance=obj.user).data


class PostDetailSerializer(serializers.ModelSerializer):
    """帖子详情序列化器"""
    user = UserListSerializer()
    images = PostImageSerializer(many=True, required=True)
    comments = PostCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['user',
                  'title',
                  'like_num',
                  'content',
                  'images',
                  'comments']


class PostCreateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    post_id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=20, write_only=True)
    content = serializers.CharField(max_length=1000, write_only=True)
    images = serializers.ListField(child=serializers.ImageField(allow_empty_file=False),
                                   allow_empty=False,
                                   max_length=6,
                                   write_only=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        user = Users.objects.get(pk=validated_data.get('user_id'))
        post = Post.objects.create(user=user,
                                   title=validated_data.get('title'),
                                   content=validated_data.get('content'))
        index = 1

        for image in validated_data.get('images'):
            print(index)
            PostImages.objects.create(post=post,
                                      order_number=index,
                                      image=image)
            index += 1
        return post


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
