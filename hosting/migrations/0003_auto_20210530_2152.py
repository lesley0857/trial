# Generated by Django 2.1.5 on 2021-05-30 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosting', '0002_auto_20210530_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='profile_pic',
            field=models.ImageField(blank=True, default='Koala.jpg', upload_to=''),
        ),
    ]