# Generated by Django 4.1.7 on 2023-03-18 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0014_rename_conversions_form1conversions_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='form1submitted',
            name='returned',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='form2submitted',
            name='returned',
            field=models.BooleanField(default=False),
        ),
    ]