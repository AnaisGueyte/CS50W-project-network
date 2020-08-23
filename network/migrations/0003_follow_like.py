# Generated by Django 3.0.8 on 2020-07-16 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('follow_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=11)),
                ('following_id', models.CharField(max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('like_id', models.AutoField(primary_key=True, serialize=False)),
                ('post_id', models.CharField(max_length=11)),
                ('username_id', models.CharField(max_length=11)),
            ],
        ),
    ]