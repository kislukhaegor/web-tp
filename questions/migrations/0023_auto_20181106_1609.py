# Generated by Django 2.1.2 on 2018-11-06 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0022_auto_20181106_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='upload',
            field=models.ImageField(default='uploads/default/default.png', upload_to='uploads/%Y/%m/%d/'),
        ),
    ]
