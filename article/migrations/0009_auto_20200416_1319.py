# Generated by Django 3.0.5 on 2020-04-16 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0008_auto_20200415_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepost',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='article/%Y%m%d/'),
        ),
    ]
