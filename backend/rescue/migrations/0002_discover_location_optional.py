from django.db import migrations, models


def fill_empty_addresses(apps, schema_editor):
    RescueCase = apps.get_model('rescue', 'RescueCase')
    RescueCase.objects.filter(discover_address__isnull=True).update(discover_address='')
    RescueCase.objects.filter(discover_address='').update(discover_address='\u672a\u586b\u5199')


class Migration(migrations.Migration):

    dependencies = [
        ('rescue', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rescuecase',
            name='discover_latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='rescuecase',
            name='discover_longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.RunPython(fill_empty_addresses, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='rescuecase',
            name='discover_address',
            field=models.CharField(max_length=255),
        ),
    ]
