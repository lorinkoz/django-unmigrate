# Generated by Django 3.0.5 on 2020-05-02 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0004_merge_20200502_0148"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mymodel",
            name="name",
            field=models.CharField(max_length=30),
        ),
    ]
