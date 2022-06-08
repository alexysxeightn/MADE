CREATE TABLE IF NOT EXISTS movies (
    movieid int,
    title text,
    year int,
    genres set<text>,
    PRIMARY KEY(title, year, movieid)
);