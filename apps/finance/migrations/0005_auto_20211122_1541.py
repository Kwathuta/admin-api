# Generated by Django 3.2.9 on 2021-11-22 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0004_staff_date_processed'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=40)),
                ('merchant', models.CharField(default='MERCHANTS', max_length=100)),
                ('date_processed', models.DateTimeField(auto_now_add=True)),
                ('approved_expenses', models.IntegerField(default='0')),
                ('total_amount', models.DecimalField(decimal_places=2, default='0', max_digits=40)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('accepted', 'accepted'), ('rejected', 'rejected')], default='pending', max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='staff',
            name='department',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='insurance',
            field=models.DecimalField(decimal_places=2, max_digits=40, null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='mobile_number',
            field=models.IntegerField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='position',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
