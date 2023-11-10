# Generated by Django 4.2.6 on 2023-11-10 19:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("coinRush", "0043_alter_stock_image_alter_user_created_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stock",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        ),
        migrations.AlterField(
            model_name="user",
            name="created_date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 11, 10, 19, 37, 21, 18677, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
