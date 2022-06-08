CREATE TABLE IF NOT EXISTS movies_by_genre_rating (
    movieid int,
    title text,
    year int,
    genre text, 
    rating float,
    PRIMARY KEY (genre, year, rating, movieid)
)
WITH CLUSTERING ORDER BY (year ASC, rating DESC);