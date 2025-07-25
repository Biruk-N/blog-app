# Generated by Django 5.0.1 on 2025-07-25 21:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reactions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='reaction',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reactions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='reaction',
            index=models.Index(fields=['post', 'reaction_type'], name='reactions_r_post_id_36c0cb_idx'),
        ),
        migrations.AddIndex(
            model_name='reaction',
            index=models.Index(fields=['user', 'created_at'], name='reactions_r_user_id_09910f_idx'),
        ),
        migrations.AddIndex(
            model_name='reaction',
            index=models.Index(fields=['post', 'user'], name='reactions_r_post_id_41243a_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='reaction',
            unique_together={('post', 'user', 'reaction_type')},
        ),
    ]
