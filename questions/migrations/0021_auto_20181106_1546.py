# Generated by Django 2.1.2 on 2018-11-06 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0020_auto_20181106_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likedislike',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.User', verbose_name='Пользователь'),
        ),
    ]
