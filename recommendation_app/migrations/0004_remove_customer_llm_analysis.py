# Generated by Django 5.1.7 on 2025-04-02 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recommendation_app', '0003_customer_llm_analysis'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='llm_analysis',
        ),
    ]
