# Generated by Django 4.1.7 on 2023-03-04 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_alter_formsubmitted_currency_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversions',
            name='denomination',
            field=models.TextField(),
        ),
    ]