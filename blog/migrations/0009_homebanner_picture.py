# Generated by Django 5.0.2 on 2024-04-08 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_alter_homebanner_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='homebanner',
            name='picture',
            field=models.ImageField(default='home-right.png', upload_to='HomeBanner/'),
        ),
    ]
