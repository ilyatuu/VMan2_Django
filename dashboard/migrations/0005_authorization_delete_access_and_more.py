# Generated by Django 4.0.5 on 2022-07-12 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_csmfdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='authorization',
            name='delete_access',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='authorization',
            name='update_access',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='authorization',
            name='view_access',
            field=models.BooleanField(default=False),
        ),
    ]
