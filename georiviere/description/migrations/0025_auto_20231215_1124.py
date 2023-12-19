# Generated by Django 3.1.14 on 2023-12-15 11:24

from django.db import migrations
import pgtrigger.compiler
import pgtrigger.migrations


class Migration(migrations.Migration):

    dependencies = [
        ('description', '0024_auto_20230323_1621'),
    ]

    operations = [
        pgtrigger.migrations.AddTrigger(
            model_name='land',
            trigger=pgtrigger.compiler.Trigger(name='keep_in_sync', sql=pgtrigger.compiler.UpsertTriggerSql(declare='DECLARE elevation elevation_infos;', func='\n                    SELECT * FROM ft_elevation_infos(NEW.geom, 20) INTO elevation;\n                    -- Update path geometry\n                    NEW.geom_3d := elevation.draped;\n                    NEW.length := ST_3DLength(elevation.draped);\n                    NEW.slope := elevation.slope;\n                    NEW.min_elevation := elevation.min_elevation;\n                    NEW.max_elevation := elevation.max_elevation;\n                    NEW.ascent := elevation.positive_gain;\n                    NEW.descent := elevation.negative_gain;\n\n                    RETURN NEW;\n                ', hash='82ffa7255d1e65c383b05ef0fa226da73a7ad6c8', operation='UPDATE OF "geom" OR INSERT', pgid='pgtrigger_keep_in_sync_fb8bb', table='description_land', when='BEFORE')),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name='morphology',
            trigger=pgtrigger.compiler.Trigger(name='keep_in_sync', sql=pgtrigger.compiler.UpsertTriggerSql(declare='DECLARE elevation elevation_infos;', func='\n                    SELECT * FROM ft_elevation_infos(NEW.geom, 20) INTO elevation;\n                    -- Update path geometry\n                    NEW.geom_3d := elevation.draped;\n                    NEW.length := ST_3DLength(elevation.draped);\n                    NEW.slope := elevation.slope;\n                    NEW.min_elevation := elevation.min_elevation;\n                    NEW.max_elevation := elevation.max_elevation;\n                    NEW.ascent := elevation.positive_gain;\n                    NEW.descent := elevation.negative_gain;\n\n                    RETURN NEW;\n                ', hash='f2e3c5183c820b762d1336a39135727ffc39c5e3', operation='UPDATE OF "geom" OR INSERT', pgid='pgtrigger_keep_in_sync_472ec', table='description_morphology', when='BEFORE')),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name='status',
            trigger=pgtrigger.compiler.Trigger(name='keep_in_sync', sql=pgtrigger.compiler.UpsertTriggerSql(declare='DECLARE elevation elevation_infos;', func='\n                    SELECT * FROM ft_elevation_infos(NEW.geom, 20) INTO elevation;\n                    -- Update path geometry\n                    NEW.geom_3d := elevation.draped;\n                    NEW.length := ST_3DLength(elevation.draped);\n                    NEW.slope := elevation.slope;\n                    NEW.min_elevation := elevation.min_elevation;\n                    NEW.max_elevation := elevation.max_elevation;\n                    NEW.ascent := elevation.positive_gain;\n                    NEW.descent := elevation.negative_gain;\n\n                    RETURN NEW;\n                ', hash='9ebcbb87cf2196d3c04e0e624571d3a49b1ebb69', operation='UPDATE OF "geom" OR INSERT', pgid='pgtrigger_keep_in_sync_aa87c', table='description_status', when='BEFORE')),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name='usage',
            trigger=pgtrigger.compiler.Trigger(name='keep_in_sync', sql=pgtrigger.compiler.UpsertTriggerSql(declare='DECLARE elevation elevation_infos;', func='\n                    SELECT * FROM ft_elevation_infos(NEW.geom, 20) INTO elevation;\n                    -- Update path geometry\n                    NEW.geom_3d := elevation.draped;\n                    NEW.length := ST_3DLength(elevation.draped);\n                    NEW.slope := elevation.slope;\n                    NEW.min_elevation := elevation.min_elevation;\n                    NEW.max_elevation := elevation.max_elevation;\n                    NEW.ascent := elevation.positive_gain;\n                    NEW.descent := elevation.negative_gain;\n\n                    RETURN NEW;\n                ', hash='c18fa3553e1c897d5a5e5f3b6cc5836c86429190', operation='UPDATE OF "geom" OR INSERT', pgid='pgtrigger_keep_in_sync_71b71', table='description_usage', when='BEFORE')),
        ),
    ]