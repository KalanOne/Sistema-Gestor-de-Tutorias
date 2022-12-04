# Generated by Django 4.1.2 on 2022-11-19 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tutoria', '0037_excel2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorado',
            name='correoPersonal',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='tutorado',
            name='domicilio',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='tutorado',
            name='semestre',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tutorado',
            name='telefono',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
