ALTER TABLE customer ADD COLUMN email VARCHAR(100);

UPDATE customer SET email = CONCAT(LOWER(REPLACE(name, ' ', '.')), '@example.com');
