DROP TYPE IF EXISTS elevation_infos;
CREATE TYPE elevation_infos AS (
    draped geometry,
    slope float,
    min_elevation integer,
    max_elevation integer,
    positive_gain integer,
    negative_gain integer
);