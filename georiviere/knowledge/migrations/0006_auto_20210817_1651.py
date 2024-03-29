# Generated by Django 3.1.6 on 2021-08-17 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0005_auto_20210614_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vegetation',
            name='age_class_diversity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='knowledge.vegetationageclassdiversity', verbose_name='Vegetation Class'),
        ),
        migrations.AlterField(
            model_name='vegetation',
            name='specific_diversity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='knowledge.vegetationspecificdiversity', verbose_name='Specific diversity'),
        ),
        migrations.AlterField(
            model_name='vegetation',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='knowledge.vegetationstate', verbose_name='Vegetation state'),
        ),
        migrations.AlterField(
            model_name='vegetation',
            name='strata',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='knowledge.vegetationstrata', verbose_name='Vegetation Strata'),
        ),
        migrations.AlterField(
            model_name='vegetation',
            name='thickness',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='knowledge.vegetationthicknesstype', verbose_name='Thickness type'),
        ),
        migrations.AlterField(
            model_name='work',
            name='bank_effect',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='knowledge.workbankeffect', verbose_name='Bank effect'),
        ),
        migrations.AlterField(
            model_name='work',
            name='code_stake',
            field=models.CharField(blank=True, default='', max_length=128, verbose_name='Code Stake'),
        ),
        migrations.AlterField(
            model_name='work',
            name='downstream_influence',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='knowledge.workdownstreaminfluence', verbose_name='Downsteam influence'),
        ),
        migrations.AlterField(
            model_name='work',
            name='fish_continuity_effect',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='knowledge.workfishcontinuityeffect', verbose_name='Fish Continuity effect'),
        ),
        migrations.AlterField(
            model_name='work',
            name='sediment_effect',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='knowledge.worksedimenteffect', verbose_name='Sediment effect'),
        ),
        migrations.AlterField(
            model_name='work',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='knowledge.workstate', verbose_name='Work state'),
        ),
        migrations.AlterField(
            model_name='work',
            name='upstream_influence',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='knowledge.workupstreaminfluence', verbose_name='Upstream influence'),
        ),
    ]
