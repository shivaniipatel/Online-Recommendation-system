# Generated by Django 2.1.7 on 2019-03-02 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0009_auto_20190302_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='contact',
            field=models.CharField(max_length=12, null=True),
        ),
    ]