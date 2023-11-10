# Generated by Django 4.2.6 on 2023-11-10 18:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("coinRush", "0029_alter_stock_coin_image_alter_user_created_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stock",
            name="coin_image",
            field=models.ImageField(blank=True, null=True, upload_to="images/"),
        ),
        migrations.AlterField(
            model_name="user",
            name="created_date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 11, 10, 18, 13, 12, 894044, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
