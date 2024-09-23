# Generated by Django 5.1.1 on 2024-09-19 14:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_produto', models.CharField(max_length=50, null=True)),
                ('descricao', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Foto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='fotos_produto/')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fotos', to='mercado.produto')),
            ],
        ),
    ]