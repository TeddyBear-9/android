# Generated by Django 3.2.9 on 2021-12-13 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoppingmall', '0010_auto_20211213_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postimages',
            name='image',
            field=models.ImageField(default=None, upload_to='post_imgs'),
        ),
    ]
