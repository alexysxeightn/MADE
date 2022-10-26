WITH
top_tags AS (
    SELECT tag_lf, COUNT(*) as count_tag
    FROM artists
    LATERAL VIEW explode(split(tags_lastfm, ';')) tagTable as tag_lf
    WHERE tag_lf != ''
    GROUP BY tag_lf
    ORDER BY count_tag DESC
    LIMIT 10
),
artist_listeners AS (
    SELECT tag_lf, artist_lastfm, listeners_lastfm
    FROM artists
    LATERAL VIEW explode(split(tags_lastfm, ';')) tagTable as tag_lf
)
SELECT DISTINCT artist_lastfm, listeners_lastfm
FROM artist_listeners
WHERE tag_lf in (SELECT tag_lf FROM top_tags)
ORDER BY listeners_lastfm DESC
LIMIT 10
