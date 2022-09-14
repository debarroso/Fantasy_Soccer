INSERT INTO raw.shots (SELECT * FROM temp.shots);
CREATE TABLE temp.tmp_shots as (SELECT DISTINCT * FROM raw.shots);
TRUNCATE TABLE raw.shots;
INSERT INTO raw.shots (SELECT * FROM temp.tmp_shots);
DROP TABLE temp.tmp_shots;