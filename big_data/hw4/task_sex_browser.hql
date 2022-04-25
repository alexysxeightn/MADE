set hive.auto.convert.join=false;
set mapreduce.job.reduces=4;

SELECT
    users.browser,
    SUM(IF(users.sex = "male", 1, 0)) as male_cnt,
    SUM(IF(users.sex = "female", 1, 0)) as female_cnt
    FROM logs INNER JOIN users ON logs.ip = users.ip
GROUP BY users.browser
LIMIT 10;