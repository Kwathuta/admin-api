# Generated by Django 3.2.9 on 2021-11-23 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payroll',
            name='date',
        ),
        migrations.RemoveField(
            model_name='payroll',
            name='full_name',
        ),
        migrations.RemoveField(
            model_name='payroll',
            name='payment_type',
        ),
        migrations.AddField(
            model_name='payroll',
            name='debit_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='payroll',
            name='deduction',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='payroll',
            name='gross_pay',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='payroll',
            name='month',
            field=models.CharField(choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='payroll',
            name='net_pay',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='payroll',
            name='pay_id',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='payroll',
            name='payroll_status',
            field=models.CharField(choices=[('Successful', 'Successful'), ('Pending', 'Pending')], default='Successful', max_length=20),
        ),
        migrations.AddField(
            model_name='payroll',
            name='staff_paid',
            field=models.IntegerField(null=True),
        ),
    ]
