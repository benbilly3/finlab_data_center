CREATE TABLE `dev_tw_data`.`stock_price` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `stock_id` VARCHAR(8) NOT NULL,
  `date` DATETIME NOT NULL,
  `stock_name` VARCHAR(16) NOT NULL,
  `vol` FLOAT NULL DEFAULT NULL,
  `turnover_price` FLOAT NULL DEFAULT NULL,
  `close` FLOAT NULL DEFAULT NULL,
  `open` FLOAT NULL DEFAULT NULL,
  `low` FLOAT NULL DEFAULT NULL,
  `high` FLOAT  NULL DEFAULT NULL,
  `transactions_number` FLOAT NULL DEFAULT NULL,
  `finally_reveal_buy_price` FLOAT NULL DEFAULT NULL,
  `finally_reveal_sell_price` FLOAT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `unique_idx` (`stock_id` ASC, `date` ASC) VISIBLE,
  INDEX `stock_id_idx` (`stock_id` ASC) VISIBLE,
  INDEX `date_idx` (`date` ASC) VISIBLE,
  INDEX `stock_name_idx` (`stock_name` ASC) VISIBLE);


CREATE TABLE `dev_tw_data`.`rotc_stock_price` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `stock_id` VARCHAR(8) NOT NULL,
  `date` DATETIME NOT NULL,
  `stock_name` VARCHAR(16) NOT NULL,
  `vol` FLOAT NULL DEFAULT NULL,
  `turnover_price` FLOAT NULL DEFAULT NULL,
  `mean_price` FLOAT NULL DEFAULT NULL,
  `close` FLOAT NULL DEFAULT NULL,
  `open` FLOAT NULL DEFAULT NULL,
  `low` FLOAT NULL DEFAULT NULL,
  `high` FLOAT  NULL DEFAULT NULL,
  `transactions_number` FLOAT NULL DEFAULT NULL,
  `finally_reveal_buy_price` FLOAT NULL DEFAULT NULL,
  `finally_reveal_sell_price` FLOAT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `unique_idx` (`stock_id` ASC, `date` ASC) VISIBLE,
  INDEX `stock_id_idx` (`stock_id` ASC) VISIBLE,
  INDEX `date_idx` (`date` ASC) VISIBLE,
  INDEX `stock_name_idx` (`stock_name` ASC) VISIBLE);