# Generated by Django 4.2 on 2023-05-01 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_application_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('Approved ', 'Approved'), ('Denied', 'Denied'), ('Pending', 'Pending')], default='Pending', max_length=9),
        ),
    ]
