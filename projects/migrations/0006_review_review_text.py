# Generated by Django 4.1.7 on 2023-07-23 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_alter_project_options_review_owner_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='review_text',
            field=models.TextField(default=''),
        ),
    ]
