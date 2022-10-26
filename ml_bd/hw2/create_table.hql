CREATE TABLE default.artists (
    mbid STRING,
    artist_mb STRING,
    artist_lastfm STRING,
    country_mb STRING,
    country_lastfm STRING,
    tags_mb STRING,
    tags_lastfm STRING,
    listeners_lastfm INT,
    scrobbles_lastfm INT,
    ambiguous_artist BOOLEAN
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' TBLPROPERTIES (
    "skip.header.line.count" = "1"
);

LOAD DATA LOCAL INPATH '/opt/artists.csv' OVERWRITE INTO TABLE artists;
