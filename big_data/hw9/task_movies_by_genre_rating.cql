SELECT 
    MIN(rating), AVG(rating), MAX(rating)
FROM 
    movies_by_genre_rating 
WHERE 
    genre = 'Sci-Fi'
    AND year >= 2000;