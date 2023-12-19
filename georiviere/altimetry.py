import pgtrigger
from geotrek.altimetry.models import AltimetryMixin as BaseAltimetryMixin


class AltimetryMixin(BaseAltimetryMixin):
    class Meta:
        abstract = True
        triggers = [
            pgtrigger.Trigger(
                name="keep_in_sync",
                operation=pgtrigger.UpdateOf('geom') | pgtrigger.Insert,
                when=pgtrigger.Before,
                declare=[('elevation', 'elevation_infos')],
                func="""
                    SELECT * FROM ft_elevation_infos(NEW.geom, 20) INTO elevation;
                    -- Update path geometry
                    NEW.geom_3d := elevation.draped;
                    NEW.length := ST_3DLength(elevation.draped);
                    NEW.slope := elevation.slope;
                    NEW.min_elevation := elevation.min_elevation;
                    NEW.max_elevation := elevation.max_elevation;
                    NEW.ascent := elevation.positive_gain;
                    NEW.descent := elevation.negative_gain;
                    RETURN NEW;
                """
            )
        ]
