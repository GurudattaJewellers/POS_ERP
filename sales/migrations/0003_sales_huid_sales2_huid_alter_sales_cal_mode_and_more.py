# Generated by Django 4.1.3 on 2023-03-28 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_sales_box_id_sales2_box_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales',
            name='HUID',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='sales2',
            name='HUID',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='sales',
            name='cal_mode',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='sales',
            name='gross_weight',
            field=models.DecimalField(decimal_places=3, max_digits=10),
        ),
        migrations.AlterField(
            model_name='sales',
            name='stone_cost',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='sales2',
            name='cal_mode',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='sales2',
            name='gross_weight',
            field=models.DecimalField(decimal_places=3, max_digits=10),
        ),
        migrations.AlterField(
            model_name='sales2',
            name='stone_cost',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]