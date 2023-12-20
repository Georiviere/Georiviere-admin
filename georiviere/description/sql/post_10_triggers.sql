CREATE TRIGGER description_morphology_10_elevation
BEFORE INSERT OR UPDATE OF geom ON description_morphology
FOR EACH ROW EXECUTE PROCEDURE elevation();

CREATE TRIGGER description_status_10_elevation
BEFORE INSERT OR UPDATE OF geom ON description_status
FOR EACH ROW EXECUTE PROCEDURE elevation();

CREATE TRIGGER description_land_10_elevation
BEFORE INSERT OR UPDATE OF geom ON description_land
FOR EACH ROW EXECUTE PROCEDURE elevation();

CREATE TRIGGER description_usage_10_elevation
BEFORE INSERT OR UPDATE OF geom ON description_usage
FOR EACH ROW EXECUTE PROCEDURE elevation();