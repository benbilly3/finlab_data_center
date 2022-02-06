CREATE TABLE `tw_data`.`insider_shareholding_declaration_transfer` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date` DATETIME NOT NULL,
  `stock_id` VARCHAR(16) NULL,
  `stock_name` VARCHAR(16) NULL,
  `declarant_identity` VARCHAR(32) NULL,
  `name` VARCHAR(128) NULL,
  `shares_transfer_method` VARCHAR(32) NULL,
  `transferred_shares_num` FLOAT NULL,
  `maximum_transferable_shares_in_one_day` FLOAT NULL,
  `assignee` VARCHAR(128) NULL,
  `current_shares`  FLOAT NULL,
  `current_shares_trust`  FLOAT NULL,
  `transferred_own_shares_total_num`  FLOAT NULL,
  `transferred_trust_shares_total_num`  FLOAT NULL,
  `after_transfer_own_shareholding`  FLOAT NULL,
  `after_transfer_trust_shareholding`  FLOAT NULL,
  `declare_uncompleted_transfer` INT NULL,
  `start_date` DATETIME NOT NULL,
  `end_date` DATETIME NOT NULL,
  `market` VARCHAR(4) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `unique_idx` (`stock_id` ASC, `date` ASC, `name` ASC, `assignee` ASC) VISIBLE,
  INDEX `stock_id_idx` (`stock_id` ASC) VISIBLE,
  INDEX `date_idx` (`date` ASC) VISIBLE,
  INDEX `name_idx` (`name` ASC) VISIBLE);