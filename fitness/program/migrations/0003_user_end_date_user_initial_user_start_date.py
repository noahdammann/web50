# Generated by Django 4.1.1 on 2022-11-18 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0002_alter_user_goal_alter_user_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='initial',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='start_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
