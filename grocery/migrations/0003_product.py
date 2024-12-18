# Generated by Django 3.1.1 on 2024-09-10 18:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grocery', '0002_grocerystore_offers_gold'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock', models.IntegerField()),
                ('grocery_store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='grocery.grocerystore')),
            ],
        ),
    ]
