# Generated by Django 2.1.5 on 2021-06-09 16:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Checkoutt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Email', models.EmailField(max_length=254)),
                ('Address', models.CharField(max_length=200, null=True)),
                ('Country', django_countries.fields.CountryField(max_length=2)),
                ('state', models.CharField(max_length=200, null=True)),
                ('Zip', models.CharField(max_length=200, null=True)),
                ('Payment_options', models.CharField(max_length=200, null=True)),
                ('user', models.ForeignKey(default=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('phone', models.IntegerField(null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('plans', models.CharField(choices=[('Diamond', 'Diamond'), ('Gold', 'Gold'), ('Silver', 'Silver')], default='PLANS[0]', max_length=200)),
                ('profile_pic', models.ImageField(default='/Koala.jpg/', upload_to='')),
                ('user', models.OneToOneField(default=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered_date', models.DateTimeField(null=True)),
                ('ordered', models.BooleanField(default=False)),
                ('Billing_address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hosting.Checkoutt')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default='0', null=True)),
                ('ordered', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, null=True)),
                ('price', models.FloatField(null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('discount', models.FloatField(blank=True, null=True)),
                ('tag', models.CharField(choices=[('Indoor', 'Indoor'), ('Outdoor', 'Outdoor'), ('Beauty', 'Beauty')], default='TAGS[0]', max_length=200)),
                ('profile_pic', models.ImageField(blank=True, upload_to='')),
            ],
        ),
        migrations.AddField(
            model_name='orderitem',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hosting.Products'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hosting.Order'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
