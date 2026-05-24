-- Create database
CREATE DATABASE IF NOT EXISTS afriq_tshirts;
USE afriq_tshirts;

-- =========================
-- T_SHIRTS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS t_shirts (
    t_shirt_id INT AUTO_INCREMENT PRIMARY KEY,
    brand ENUM('Van Huesen', 'Levi', 'Nike', 'Adidas') NOT NULL,
    color ENUM('Red', 'Blue', 'Black', 'White') NOT NULL,
    size ENUM('XS', 'S', 'M', 'L', 'XL') NOT NULL,
    price INT NOT NULL,
    stock_quantity INT NOT NULL,
    UNIQUE KEY brand_color_size (brand, color, size)
) ENGINE=InnoDB;

-- =========================
-- DISCOUNTS TABLE (FIXED)
-- =========================
CREATE TABLE IF NOT EXISTS discounts (
    discount_id INT AUTO_INCREMENT PRIMARY KEY,
    t_shirt_id INT NOT NULL,
    pct_discount DECIMAL(5,2) NOT NULL,
    CONSTRAINT fk_discount_tshirt
        FOREIGN KEY (t_shirt_id)
        REFERENCES t_shirts(t_shirt_id)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- =========================
-- STORED PROCEDURE
-- =========================
DELIMITER $$

DROP PROCEDURE IF EXISTS PopulateTShirts $$

CREATE PROCEDURE PopulateTShirts()
BEGIN
    DECLARE counter INT DEFAULT 0;
    DECLARE max_records INT DEFAULT 100;

    DECLARE brand_val VARCHAR(20);
    DECLARE color_val VARCHAR(10);
    DECLARE size_val VARCHAR(5);
    DECLARE price_val INT;
    DECLARE stock_val INT;

    WHILE counter < max_records DO

        SET brand_val = ELT(FLOOR(1 + RAND() * 4), 'Van Huesen', 'Levi', 'Nike', 'Adidas');
        SET color_val = ELT(FLOOR(1 + RAND() * 4), 'Red', 'Blue', 'Black', 'White');
        SET size_val  = ELT(FLOOR(1 + RAND() * 5), 'XS', 'S', 'M', 'L', 'XL');

        SET price_val = FLOOR(10 + RAND() * 41);
        SET stock_val = FLOOR(10 + RAND() * 91);

        BEGIN
            DECLARE CONTINUE HANDLER FOR 1062 BEGIN END;

            INSERT INTO t_shirts (brand, color, size, price, stock_quantity)
            VALUES (brand_val, color_val, size_val, price_val, stock_val);

            SET counter = counter + 1;
        END;

    END WHILE;
END $$

DELIMITER ;

-- =========================
-- POPULATE DATA
-- =========================
CALL PopulateTShirts();

-- =========================
-- SAMPLE DISCOUNTS
-- =========================
INSERT INTO discounts (t_shirt_id, pct_discount)
VALUES
(1, 10.00),
(2, 15.00),
(3, 20.00),
(4, 5.00),
(5, 25.00),
(6, 10.00),
(7, 30.00),
(8, 35.00),
(9, 40.00),
(10, 45.00);