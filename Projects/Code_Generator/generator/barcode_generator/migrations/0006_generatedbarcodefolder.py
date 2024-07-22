# Generated by Django 5.0.7 on 2024-07-17 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barcode_generator', '0005_remove_barcode_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneratedBarcodeFolder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('folder_name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]