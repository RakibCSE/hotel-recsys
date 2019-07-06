# Generated by Django 2.2.1 on 2019-07-02 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hoteldetail',
            name='accommodation_type',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='hoteldetail',
            name='address',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='hoteldetail',
            name='country',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='hoteldetail',
            name='district',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='hoteldetail',
            name='guest_rating',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='hoteldetail',
            name='hotel_latitude',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='hoteldetail',
            name='hotel_longitude',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='hoteldetail',
            name='hotel_name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='hoteldetail',
            name='hotel_price',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='hoteldetail',
            name='region',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='hoteldetail',
            name='review_badge',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='hoteldetail',
            name='star_rating',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='hoteldetail',
            name='thumb_urls',
            field=models.CharField(max_length=5000, null=True),
        ),
    ]