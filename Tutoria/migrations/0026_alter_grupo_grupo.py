# Generated by Django 4.1.2 on 2022-11-04 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tutoria', '0025_alter_cuestionario_idestado_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grupo',
            name='grupo',
            field=models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], max_length=100, null=True),
        ),
    ]