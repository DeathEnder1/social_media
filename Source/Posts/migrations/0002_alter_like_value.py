# Generated by Django 4.2.6 on 2023-10-23 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='value',
            field=models.CharField(choices=[('like', 'like'), ('unlike', 'unlike')], max_length=20),
        ),
    ]
