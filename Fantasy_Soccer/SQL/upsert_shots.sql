INSERT INTO raw.shots (SELECT * FROM staging.shots);
CREATE TABLE staging.tmp_shots as (SELECT DISTINCT * FROM raw.shots);
TRUNCATE TABLE raw.shots;
INSERT INTO raw.shots (SELECT * FROM staging.tmp_shots);
DROP TABLE staging.tmp_shots;