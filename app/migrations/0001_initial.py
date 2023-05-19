# Generated by Django 4.2.1 on 2023-05-19 09:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=20, unique=True)),
                ('operator_code', models.CharField(max_length=10)),
                ('tag', models.CharField(blank=True, max_length=20, null=True)),
                ('tz', models.CharField(default='UTC', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('sent_at', models.DateTimeField(blank=True, null=True)),
                ('body', models.TextField()),
                ('operator_code', models.CharField(max_length=10)),
                ('tag', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('status', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='app.mailing')),
            ],
        ),
        migrations.CreateModel(
            name='MailingStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_messages', models.IntegerField(default=0)),
                ('no_messages_ok', models.IntegerField(default=0)),
                ('no_messages_fail', models.IntegerField(default=0)),
                ('completed', models.BooleanField(default=False)),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stats', to='app.mailing')),
            ],
        ),
        migrations.CreateModel(
            name='ClientMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clients', to='app.client')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='app.message')),
            ],
        ),
    ]
