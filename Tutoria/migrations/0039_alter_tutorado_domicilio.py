# Generated by Django 4.1.2 on 2022-11-19 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tutoria', '0038_alter_tutorado_correopersonal_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorado',
            name='domicilio',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
