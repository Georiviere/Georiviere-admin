CREATE TRIGGER proceeding_proceeding_10_elevation
BEFORE INSERT OR UPDATE OF geom ON proceeding_proceeding
FOR EACH ROW EXECUTE PROCEDURE elevation();
