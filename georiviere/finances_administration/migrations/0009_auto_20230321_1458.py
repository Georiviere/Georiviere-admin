# Generated by Django 3.1.14 on 2023-03-21 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authent', '0005_remove_userprofile_language'),
        ('finances_administration', '0008_auto_20211206_1526'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdministrativePhase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=128, verbose_name='Name')),
                ('estimated_budget', models.DecimalField(decimal_places=2, default=0, max_digits=19, verbose_name='Estimated budget')),
                ('revised_budget', models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True, verbose_name='Revised budget')),
                ('administrative_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phases', to='finances_administration.administrativefile', verbose_name='Phases')),
            ],
            options={
                'verbose_name': 'Administrative phase',
                'verbose_name_plural': 'Administrative phases',
            },
        ),
        migrations.CreateModel(
            name='AdministrativeDeferral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(blank=True, max_length=128, null=True, verbose_name='Label')),
                ('structure', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authent.structure', verbose_name='Related structure')),
            ],
            options={
                'verbose_name': 'Administrative deferral',
                'verbose_name_plural': 'Administrative deferrals',
            },
        ),
        migrations.AddField(
            model_name='administrativeoperation',
            name='deferral',
            field=models.ManyToManyField(blank=True, related_name='operations', to='finances_administration.AdministrativeDeferral', verbose_name='Deferral'),
        ),
        migrations.AddField(
            model_name='administrativeoperation',
            name='phase',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='operations', to='finances_administration.administrativephase', verbose_name='Phase'),
        ),
    ]