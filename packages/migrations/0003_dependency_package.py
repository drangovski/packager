# Generated by Django 4.0.6 on 2022-07-04 22:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0002_dependency'),
    ]

    operations = [
        migrations.AddField(
            model_name='dependency',
            name='package',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.DO_NOTHING, related_name='for_package', to='packages.package'),
            preserve_default=False,
        ),
    ]
