WITH russian_rap AS (
    SELECT tag_lf, artist_lastfm, listeners_lastfm
    FROM artists
    LATERAL VIEW explode(split(tags_lastfm, ';')) tagTable as tag_lf
    WHERE country_lastfm = 'Russia' AND tag_lf = 'rap'
)
SELECT DISTINCT artist_lastfm, listeners_lastfm
FROM russian_rap
ORDER BY listeners_lastfm DESC
LIMIT 10
