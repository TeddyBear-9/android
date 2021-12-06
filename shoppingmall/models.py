from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Users(models.Model):
    name = models.CharField(max_length=20, null=False, unique=True)
    icon = models.ImageField(default="")
    email = models.EmailField(default="")
    phone = models.CharField(max_length=20, null=True)
    password = models.CharField(max_length=20, null=False, default="123456")
    sex = models.CharField(max_length=1, default="m")
    login_status = models.BooleanField(default=0)
    subscribe_num = models.IntegerField(default=0, null=False)
    fan_num = models.IntegerField(default=0, null=False)
    last_login_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "username:%s" % self.name

class Fans(models.Model):
    user = models.ForeignKey(Users, db_column="user_id", related_name="user", on_delete=models.CASCADE)
    fan = models.ForeignKey(Users, db_column="fan_id", related_name="fan", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "user:%s,fan:%s,timestamp:%s" % (self.user, self.fan, str(self.timestamp))


class Address(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    address_inf = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, default=None)
    is_default = models.BooleanField(default=False)


class Category(models.Model):
    name = models.CharField(primary_key=True, max_length=10)


class BaseProduce(models.Model):
    name = models.CharField(max_length=200, null=False)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    sales_num = models.IntegerField(default=0)
    comment_num = models.IntegerField(default=0)
    is_active = models.BooleanField("商品是否上架", default=1)


# 子商品
class Produce(models.Model):
    child_name = models.CharField(default="", max_length=30)
    parent_produce = models.ForeignKey(BaseProduce, on_delete=models.CASCADE, related_name="parent")
    price = models.FloatField(null=False)
    order = models.IntegerField(default=1)

    class Meta:
        unique_together = [['child_name', 'parent_produce'], ['order', 'parent_produce']]


class ProduceImages(models.Model):
    produce = models.ForeignKey(BaseProduce, on_delete=models.CASCADE)
    order_number = models.IntegerField(null=False)
    image = models.ImageField(default=None)

    class Meta:
        unique_together = [['produce', 'order_number']]


class Order(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    produce = models.ForeignKey(Produce, on_delete=models.CASCADE, default="", related_name="produce_buy")
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=10, default=None)  # 商品流通状态：待付款 代发货 待收货 待评价 退款、售后
    paymentTime = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['user', 'produce', 'paymentTime']]


class ProduceComment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, primary_key=True)
    base_produce = models.ForeignKey(BaseProduce, on_delete=models.CASCADE)  # 用于建立索引方便查找商品评论
    commentTime = models.DateTimeField(auto_now_add=True)
    comment_like_num = models.IntegerField(default=0)
    star = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])


class Advertisement(models.Model):
    produce = models.ForeignKey(BaseProduce, on_delete=models.CASCADE)
    ad_images = models.ImageField(default=None)


class CartItem(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    produce = models.ForeignKey(Produce, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class Favorites(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    produce = models.ForeignKey(BaseProduce, on_delete=models.CASCADE)


class Post(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    title = models.CharField(max_length=20, null=False)
    content = models.TextField(null=False)
    like_num = models.IntegerField(default=0)
    comment_num = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=1)

    def __str__(self):
        return "user:%s, post title:%s" % (str(self.user), self.title)


class PostImages(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    order_number = models.IntegerField(null=False)
    images = models.ImageField(default=None)


class PostComments(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(null=False)
    timestamp = models.DateTimeField(auto_now_add=True)


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Try:
    name = models.CharField(max_length=20)
    produce = models.ForeignKey(BaseProduce, on_delete=models.CASCADE)
