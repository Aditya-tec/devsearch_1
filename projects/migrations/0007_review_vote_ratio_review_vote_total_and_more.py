# Generated by Django 4.1.7 on 2023-07-30 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_review_review_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='vote_ratio',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='review',
            name='vote_total',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='value',
            field=models.CharField(choices=[('up', 'Up Vote'), ('down', 'Down Vote')], max_length=200),
        ),
    ]
