# Generated by Django 4.1.7 on 2023-03-04 20:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_form2_form2conversions_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='form2conversions',
            name='formID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.form2'),
        ),
    ]