# Generated by Django 4.1.2 on 2022-12-01 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tutoria', '0049_alter_personaltec_correopersonal_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grupo',
            name='grupo',
            field=models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], max_length=100, null=True),
        ),
    ]
