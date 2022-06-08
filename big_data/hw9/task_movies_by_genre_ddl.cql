CREATE TABLE IF NOT EXISTS movies_by_genre (
    movieid int,
    title text,
    year int,
    genre text,
    PRIMARY KEY((genre), year, movieid)
)
WITH CLUSTERING ORDER BY (year DESC);