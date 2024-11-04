# Generated by Django 5.1.2 on 2024-11-03 21:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0005_mentor_groups'),
        ('info_system', '0002_remove_group_manager_group_mentor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='mentor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mentored_groups', to='auth_app.mentor', verbose_name='Ментор'),
        ),
    ]