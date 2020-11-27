# Generated by Django 2.1.7 on 2019-02-21 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=20)),
                ('contact', models.IntegerField(max_length=10)),
                ('email', models.CharField(max_length=20)),
                ('signin_details', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='login.SignIn')),
            ],
        ),
    ]