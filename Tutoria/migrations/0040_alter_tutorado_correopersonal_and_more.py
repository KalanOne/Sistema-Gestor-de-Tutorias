# Generated by Django 4.1.2 on 2022-11-19 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tutoria', '0039_alter_tutorado_domicilio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorado',
            name='correoPersonal',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='tutorado',
            name='semestre',
            field=models.PositiveIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='tutorado',
            name='telefono',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]