# Generated by Django 2.1.2 on 2018-11-06 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0012_remove_question_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='rating',
            field=models.IntegerField(default=0, verbose_name='Рейтинг пользователя'),
        ),
    ]