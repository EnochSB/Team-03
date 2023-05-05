# Generated by Django 3.2.18 on 2023-05-05 14:36

import dinings.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0005_auto_20220424_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='AtmosphereTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Dining',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField(null=True)),
                ('image1', models.ImageField(blank=True, upload_to=dinings.models.dining_img_path)),
                ('image2', models.ImageField(blank=True, upload_to=dinings.models.dining_img_path)),
                ('image3', models.ImageField(blank=True, upload_to=dinings.models.dining_img_path)),
                ('image4', models.ImageField(blank=True, upload_to=dinings.models.dining_img_path)),
                ('image5', models.ImageField(blank=True, upload_to=dinings.models.dining_img_path)),
                ('address_mc_do', models.CharField(max_length=20)),
                ('address_city', models.CharField(max_length=20)),
                ('address_dong', models.CharField(max_length=20)),
                ('address_detail', models.CharField(max_length=20)),
                ('opening_hours', models.CharField(max_length=20)),
                ('phone_number', models.CharField(blank=True, max_length=20)),
                ('like_users', models.ManyToManyField(related_name='like_dinings', to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
        migrations.CreateModel(
            name='FacilityTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='PurposeTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(null=True)),
                ('image1', models.ImageField(blank=True, upload_to=dinings.models.review_img_path)),
                ('image2', models.ImageField(blank=True, upload_to=dinings.models.review_img_path)),
                ('image3', models.ImageField(blank=True, upload_to=dinings.models.review_img_path)),
                ('image4', models.ImageField(blank=True, upload_to=dinings.models.review_img_path)),
                ('image5', models.ImageField(blank=True, upload_to=dinings.models.review_img_path)),
                ('rating', models.FloatField(verbose_name='평점')),
                ('rating_taste', models.FloatField(verbose_name='맛')),
                ('rating_price', models.FloatField(verbose_name='가격')),
                ('rating_kind', models.FloatField(verbose_name='서비스')),
                ('atmosphere_tags', models.ManyToManyField(related_name='atmosphere_reviews', to='dinings.AtmosphereTag')),
                ('dining', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dinings.dining')),
                ('facility_tags', models.ManyToManyField(related_name='facility_reviews', to='dinings.FacilityTag')),
                ('like_users', models.ManyToManyField(related_name='like_reviews', to=settings.AUTH_USER_MODEL)),
                ('purpose_tags', models.ManyToManyField(related_name='purpose_reviews', to='dinings.PurposeTag')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.PositiveIntegerField()),
                ('dining', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dinings.dining')),
            ],
        ),
    ]
