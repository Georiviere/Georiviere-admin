# Generated by Django 3.1.14 on 2024-04-12 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0023_auto_20230220_1703'),
        ('contribution', '0013_customcontributiontype_linked_to_station'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customcontributiontypefield',
            options={'ordering': ('order', 'custom_type'), 'verbose_name': 'Custom contribution type field', 'verbose_name_plural': 'Custom contribution type fields'},
        ),
        migrations.RemoveField(
            model_name='customcontribution',
            name='properties',
        ),
        migrations.RemoveField(
            model_name='customcontributiontype',
            name='linked_to_station',
        ),
        migrations.AddField(
            model_name='customcontribution',
            name='data',
            field=models.JSONField(blank=True, default=dict, verbose_name='Data'),
        ),
        migrations.AddField(
            model_name='customcontributiontype',
            name='stations',
            field=models.ManyToManyField(blank=True, to='observations.Station', verbose_name='Stations'),
        ),
        migrations.AddField(
            model_name='customcontributiontypefield',
            name='customization',
            field=models.JSONField(blank=True, default=dict, help_text='Field customization.', verbose_name='Customization'),
        ),
        migrations.AddField(
            model_name='customcontributiontypefield',
            name='help_text',
            field=models.CharField(blank=True, default='', help_text='Set a help text for the field.', max_length=256, verbose_name='Help text'),
        ),
        migrations.AlterField(
            model_name='customcontribution',
            name='custom_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contributions', to='contribution.customcontributiontype', verbose_name='Custom contribution type'),
        ),
        migrations.AlterField(
            model_name='customcontributiontypefield',
            name='custom_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='contribution.customcontributiontype', verbose_name='Custom contribution type.'),
        ),
        migrations.AlterField(
            model_name='customcontributiontypefield',
            name='key',
            field=models.SlugField(editable=False, help_text='Key used in JSON data field.', max_length=150, verbose_name='Key'),
        ),
        migrations.AlterField(
            model_name='customcontributiontypefield',
            name='label',
            field=models.CharField(help_text='Field label.', max_length=128, verbose_name='Label'),
        ),
        migrations.AlterField(
            model_name='customcontributiontypefield',
            name='options',
            field=models.JSONField(blank=True, default=dict, editable=False, help_text='Internal options for type JSON schema.', verbose_name='Options'),
        ),
        migrations.AlterField(
            model_name='customcontributiontypefield',
            name='order',
            field=models.PositiveSmallIntegerField(default=0, help_text='Order of field in form.', verbose_name='Order'),
        ),
        migrations.AlterField(
            model_name='customcontributiontypefield',
            name='required',
            field=models.BooleanField(default=False, help_text='Set if field is required to validate form.', verbose_name='Required'),
        ),
        migrations.AlterField(
            model_name='customcontributiontypefield',
            name='value_type',
            field=models.CharField(choices=[('string', 'String'), ('text', 'Text'), ('integer', 'Integer'), ('float', 'Float'), ('date', 'Date'), ('datetime', 'Datetime'), ('boolean', 'Boolean')], default='text', max_length=16, verbose_name='Type'),
        ),
        migrations.AlterIndexTogether(
            name='customcontributiontypefield',
            index_together={('order', 'custom_type')},
        ),
    ]
