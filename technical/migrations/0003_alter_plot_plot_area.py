# Generated by Django 5.1.2 on 2024-10-29 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('technical', '0002_alter_plot_cluped'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plot',
            name='plot_area',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]