# Generated by Django 2.0.6 on 2018-06-11 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prediction',
            name='_predictor',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='prediction',
            name='_visiting_team_goals',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
