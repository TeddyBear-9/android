# Generated by Django 3.2.9 on 2021-12-13 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoppingmall', '0008_rename_comment_user_postlike_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='icon',
            field=models.ImageField(default='', upload_to='user_icon'),
        ),
    ]
