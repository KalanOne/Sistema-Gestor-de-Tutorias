# Generated by Django 4.1.2 on 2022-10-17 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tutoria', '0004_alter_institucion_ruta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institucion',
            name='ruta',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]