# Generated by Django 3.2.3 on 2021-06-22 18:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password_expire_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
