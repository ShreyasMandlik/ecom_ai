# Generated by Django 5.0.6 on 2025-03-31 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendation_app', '0002_alter_customer_age_alter_customer_avg_order_value_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='llm_analysis',
            field=models.TextField(blank=True),
        ),
    ]
