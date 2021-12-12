from django.db.models import Min
from .models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'name', 'email', 'phone', 'subscribe_num', 'fan_num']


class MallProduceListSerializer(serializers.ModelSerializer):
    min_price = serializers.FloatField(required=True)

    class Meta:
        model = Produce
        fields = ['min_price']


class MallBaseProduceListSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField('get_min_price')

    class Meta:
        model = BaseProduce
        fields = ['id', 'name', 'price']

    # 用于获取商城首页展示商品的最小价格
    def get_min_price(self, obj):
        all_price = Produce.objects.filter(parent_produce=obj.id).aggregate(min_price=Min('price'))
        ser_price = MallProduceListSerializer(all_price)
        return ser_price.data.get("min_price")


class ProduceDetailSerializer(serializers.ModelSerializer):
    produce_name = serializers.SerializerMethodField("get_parent_title")

    class Meta:
        model = Produce
        fields = ['child_name', 'price', 'produce_name']

    def get_parent_title(self, obj):
        parent = Produce.objects.get(id=obj.id).parent_produce

        return parent.name


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['user', 'title', 'like_num', 'content']


class CommunitySubscribeListSerializer(serializers.ModelSerializer):
    subscribe_posts = serializers.SerializerMethodField("get_subscribe_posts")

    class Meta:
        model = Users
        fields = ['id', 'subscribe_posts']

    def get_subscribe_posts(self, obj):
        subscribe = Fans.objects.filter(fan=obj.id)
        print(subscribe)
        all_posts = Post.objects.none()
        for each in subscribe:
            posts = Post.objects.filter(user=each.user)
            all_posts = posts | all_posts
        ser_all_posts = PostListSerializer(instance=all_posts, many=True)
        return ser_all_posts.data


class CategoryProduceListSerializer(serializers.ModelSerializer):
    produces = serializers.SerializerMethodField("get_category_produces")

    class Meta:
        model = Category
        fields = ['name', 'produces']

    def get_category_produces(self, obj):
        produces = BaseProduce.objects.filter(category=obj.name, is_active=True)
        ser_produces = MallBaseProduceListSerializer(instance=produces, many=True)
        return ser_produces.data


class OrderListSerizalizer(serializers.ModelSerializer):
    produce = serializers.SerializerMethodField("get_produce")

    class Meta:
        model = Order
        fields = ['id', 'quantity', 'status', 'produce']

    def get_produce(self, obj):
        ser_produce = ProduceDetailSerializer(instance=obj.produce)
        return ser_produce.data


class UsersOrderListSerializer(serializers.ModelSerializer):
    orders = serializers.SerializerMethodField("get_all_orders")

    class Meta:
        model = Users
        fields = ['id', 'orders']

    def get_all_orders(self, obj):
        orders = Order.objects.filter(user=obj.id)
        ser_orders = OrderListSerizalizer(instance=orders, many=True)
        return ser_orders.data


class UsersMyPostListSeriazlizer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField("get_my_posts")

    class Meta:
        model = Users
        fields = ['id', 'posts']

    def get_my_posts(self, obj):
        posts = Post.objects.filter(user=obj.id)
        ser_posts = PostListSerializer(instance=posts, many=True)
        return ser_posts.data


class UserLikePostsListSeriazlizer(serializers.ModelSerializer):
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


class LoginOrRegisterSerizalizer(serializers.Serializer):
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








