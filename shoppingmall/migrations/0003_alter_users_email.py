# Generated by Django 3.2.9 on 2021-12-02 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoppingmall', '0002_auto_20211201_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.EmailField(default='', max_length=254),
        ),
    ]
