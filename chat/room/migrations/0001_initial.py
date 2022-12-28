# Generated by Django 4.1.4 on 2022-12-28 09:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('chatter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='chatter.chatter')),
            ],
        ),
    ]
