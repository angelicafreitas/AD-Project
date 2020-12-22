DROP PROCEDURE IF EXISTS gun.generate_Dates;
DELIMITER |
CREATE PROCEDURE gun.generate_Dates(date_start DATE, date_end DATE)
BEGIN
	WHILE date_start <= date_end DO
		INSERT INTO gun.dim_date (date) VALUES (date_start);
		SET date_start = date_add(date_start, INTERVAL 1 DAY);
	END WHILE;
END;
|
DELIMITER ;