# Generated by Django 3.1.14 on 2023-12-18 14:05

from django.db import migrations
import pgtrigger.compiler
import pgtrigger.migrations


class Migration(migrations.Migration):

    dependencies = [
        ('river', '0029_auto_20231218_1403'),
    ]

    operations = [
        pgtrigger.migrations.RemoveTrigger(
            model_name='stream',
            name='create_topologies',
        ),
        pgtrigger.migrations.AddTrigger(
            model_name='stream',
            trigger=pgtrigger.compiler.Trigger(name='create_topologies', sql=pgtrigger.compiler.UpsertTriggerSql(declare='DECLARE topology_morphology integer; topology_status integer;', func="\n                        INSERT INTO river_topology (stream_id, start_position, end_position, qualified)\n                        VALUES (NEW.id, 0, 1, FALSE)  RETURNING id INTO topology_morphology;\n                        INSERT INTO description_morphology (topology_id, geom, description, date_insert, date_update)\n                                                    VALUES (topology_morphology, NEW.geom, '', NOW(), NOW());\n                        INSERT INTO river_topology (stream_id, start_position, end_position, qualified)\n                        VALUES (NEW.id, 0, 1, FALSE)  RETURNING id INTO topology_status;\n                        INSERT INTO description_status (topology_id, geom, regulation, referencial, descrption, date_insert, date_update)\n                                                    VALUES (topology_status, NEW.geom, FALSE, FALSE, '', NOW(), NOW());\n                        RETURN NEW;\n                    ", hash='f5c7079e6d4e21c67d642ea14d61d4e2f39787b0', operation='INSERT', pgid='pgtrigger_create_topologies_e8d7d', table='river_stream', when='AFTER')),
        ),
    ]