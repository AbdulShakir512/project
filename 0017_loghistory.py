# Generated by Django 4.1.7 on 2023-03-20 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0016_alter_form1submitted_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='logHistory',
            fields=[
                ('logID', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.TextField()),
            ],
        ),
    ]
