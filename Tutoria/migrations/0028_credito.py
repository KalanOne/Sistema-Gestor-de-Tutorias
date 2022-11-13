# Generated by Django 4.1.2 on 2022-11-10 04:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Tutoria', '0027_alter_grupo_idinstitucion_alter_grupo_idpersonaltec'),
    ]

    operations = [
        migrations.CreateModel(
            name='Credito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(upload_to='Tutorado/Creditos')),
                ('comentarios', models.CharField(blank=True, max_length=200, null=True)),
                ('idEstado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tutoria.estado')),
                ('idTutorado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tutoria.tutorado')),
            ],
            options={
                'verbose_name': 'Credito',
                'verbose_name_plural': 'Creditos',
                'db_table': 'credito',
                'ordering': ['id'],
            },
        ),
    ]