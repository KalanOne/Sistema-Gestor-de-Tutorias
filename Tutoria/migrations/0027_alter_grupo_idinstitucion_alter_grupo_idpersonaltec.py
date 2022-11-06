# Generated by Django 4.1.2 on 2022-11-04 03:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Tutoria', '0026_alter_grupo_grupo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grupo',
            name='idInstitucion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Tutoria.institucion'),
        ),
        migrations.AlterField(
            model_name='grupo',
            name='idPersonalTec',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Tutoria.personaltec'),
        ),
    ]
