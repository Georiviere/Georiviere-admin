CREATE TRIGGER river_stream_10_elevation
BEFORE INSERT OR UPDATE OF geom ON river_stream
FOR EACH ROW EXECUTE PROCEDURE elevation();

CREATE FUNCTION update_topology_geom() RETURNS trigger SECURITY DEFINER AS $$
DECLARE
    stream_geom geometry;
BEGIN
    SELECT r.geom FROM river_stream r WHERE NEW.stream_id = r.id INTO stream_geom;
    UPDATE description_morphology
    SET geom = ST_LINESUBSTRING(stream_geom, NEW.start_position, NEW.end_position)
    WHERE topology_id = NEW.id;
    UPDATE description_status
    SET geom = ST_LINESUBSTRING(stream_geom, NEW.start_position, NEW.end_position)
    WHERE topology_id = NEW.id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER core_path_10_elevation_iu_tgr
BEFORE INSERT OR UPDATE ON river_topology
FOR EACH ROW EXECUTE PROCEDURE update_topology_geom();

CREATE FUNCTION create_topologies() RETURNS trigger SECURITY DEFINER AS $$
DECLARE
    topology_morphology integer;
    topology_status integer;
BEGIN
    INSERT INTO river_topology (stream_id, start_position, end_position, qualified)
    VALUES (NEW.id, 0, 1, FALSE)  RETURNING id INTO topology_morphology;
    INSERT INTO description_morphology (topology_id, geom, description, date_insert, date_update)
                                                VALUES (topology_morphology, NEW.geom, '', NOW(), NOW());
    INSERT INTO river_topology (stream_id, start_position, end_position, qualified)
    VALUES (NEW.id, 0, 1, FALSE)  RETURNING id INTO topology_status;
    INSERT INTO description_status (topology_id, geom, regulation, referencial, description, date_insert, date_update)
                                               VALUES (topology_status, NEW.geom, FALSE, FALSE, '', NOW(), NOW());
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER core_path_10_elevation_iu_tgr
AFTER INSERT ON river_stream
FOR EACH ROW EXECUTE PROCEDURE create_topologies();