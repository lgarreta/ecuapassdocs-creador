# Generated by Django 5.0.1 on 2024-03-05 03:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appdocs', '0010_alter_empresa_numeroid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartaportedoc',
            name='txt20',
        ),
        migrations.RemoveField(
            model_name='cartaportedoc',
            name='txt23',
        ),
    ]
