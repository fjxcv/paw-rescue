from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lostfound', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lostfoundpost',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='lostfoundpost',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='lostfoundpost',
            name='address_text',
            field=models.CharField(max_length=255),
        ),
    ]
