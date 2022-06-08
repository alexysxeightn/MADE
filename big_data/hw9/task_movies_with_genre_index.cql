SELECT 
    COUNT(*) 
FROM 
    movies_by_genre 
WHERE 
    genre = 'Horror'
    AND year >= 1980 
    AND year <= 1990
ALLOW FILTERING;