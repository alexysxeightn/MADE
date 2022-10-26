WITH top_tags AS (
    SELECT tag_lf, COUNT(*) as count_tag
    FROM artists
    LATERAL VIEW explode(split(tags_lastfm, ';')) tagTable as tag_lf
    WHERE tag_lf != ''
    GROUP BY tag_lf
    ORDER BY count_tag DESC
)
SELECT tag_lf
FROM top_tags
LIMIT 1
