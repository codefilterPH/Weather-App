# Generated by Django 4.0.6 on 2022-09-10 05:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='map.countries'),
        ),
        migrations.AlterField(
            model_name='city',
            name='city',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
