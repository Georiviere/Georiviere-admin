CREATE FUNCTION elevation() RETURNS trigger SECURITY DEFINER AS $$
DECLARE
    elevation elevation_infos;
BEGIN
    SELECT * FROM ft_elevation_infos(NEW.geom, {{ ALTIMETRIC_PROFILE_STEP }}) INTO elevation;
    -- Update path geometry
    NEW.geom_3d := elevation.draped;
    NEW.length := ST_3DLength(elevation.draped);
    NEW.slope := elevation.slope;
    NEW.min_elevation := elevation.min_elevation;
    NEW.max_elevation := elevation.max_elevation;
    NEW.ascent := elevation.positive_gain;
    NEW.descent := elevation.negative_gain;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
