# Generated by Django 4.1.7 on 2023-03-18 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0013_currencylist_amount'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Conversions',
            new_name='form1conversions',
        ),
        migrations.RenameModel(
            old_name='FormSubmitted',
            new_name='form1submitted',
        ),
        migrations.RenameModel(
            old_name='Form2',
            new_name='form2submitted',
        ),
    ]
