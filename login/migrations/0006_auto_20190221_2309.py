# Generated by Django 2.1.7 on 2019-02-21 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_auto_20190221_2308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signin',
            name='username',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
