# Generated by Django 5.0.3 on 2024-06-13 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('highrise_app', '0002_sagemitra_new_sm_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='sagemitra',
            name='new_sm_contact',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
    ]
