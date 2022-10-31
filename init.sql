CREATE TABLE IF NOT EXISTS chinese (
    id INT PRIMARY KEY AUTO_INCREMENT,
    methods INT CHECK (methods >= 0 and methods <= 6) NOT NULL,
    address CHAR(100) NOT NULL,
    no_resolve BOOL NOT NULL DEFAULT false
) CHARACTER SET utf8 COLLATE utf8_unicode_ci;
