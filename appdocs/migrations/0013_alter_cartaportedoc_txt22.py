# Generated by Django 5.0.1 on 2024-03-22 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appdocs', '0012_remove_manifiestodoc_txt36_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartaportedoc',
            name='txt22',
            field=models.CharField(max_length=300, null=True),
        ),
    ]