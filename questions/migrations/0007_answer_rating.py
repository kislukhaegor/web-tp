# Generated by Django 2.1.2 on 2018-11-05 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0006_question_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
