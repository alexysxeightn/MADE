SELECT `date`, COUNT(*) as cnt
FROM logs
GROUP BY `date`
ORDER BY cnt DESC
LIMIT 10;