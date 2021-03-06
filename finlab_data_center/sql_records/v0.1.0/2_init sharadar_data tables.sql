CREATE TABLE `dev_us_data`.`sharadar_sep` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `stock_id` VARCHAR(16) NOT NULL,
  `date` DATETIME NOT NULL,
  `open` FLOAT NULL,
  `high` FLOAT NULL,
  `low` FLOAT NULL,
  `close` FLOAT NULL,
  `volume` FLOAT NULL,
  `dividends` FLOAT NULL,
  `closeunadj` FLOAT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `unique_idx` (`stock_id` ASC, `date` ASC) VISIBLE);


CREATE TABLE `dev_us_data`.`sharader_sp500` (
  `id` INT NOT NULL,
  `stock_id` VARCHAR(16) NOT NULL,
  `date` DATETIME NOT NULL,
  `action` VARCHAR(16) NULL,
  `name` VARCHAR(64) NULL,
  `contraticker` VARCHAR(64) NULL,
  `contraname` VARCHAR(64) NULL,
  UNIQUE INDEX `unique_idx` (`stock_id` ASC) VISIBLE,
  PRIMARY KEY (`id`));


 CREATE TABLE `dev_us_data`.`sharadar_sf1` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `stock_id` VARCHAR(16) NOT NULL,
  `date` DATETIME NOT NULL,
  `dimension` VARCHAR(8) NULL,
  `calendardate` DATETIME NULL,
  `reportperiod` DATETIME NULL,
  `lastupdated` DATETIME NULL,
  `accoci` FLOAT NULL,
  `assets` FLOAT NULL,
  `assetsavg` FLOAT NULL,
  `assetsc` FLOAT NULL,
  `assetsnc` FLOAT NULL,
  `assetturnover` FLOAT NULL,
  `bvps` FLOAT NULL,
  `capex` FLOAT NULL,
  `cashneq` FLOAT NULL,
  `cashnequsd` FLOAT NULL,
  `cor` FLOAT NULL,
  `consolinc` FLOAT NULL,
  `currentratio` FLOAT NULL,
  `de` FLOAT NULL,
  `debt` FLOAT NULL,
  `debtc` FLOAT NULL,
  `debtnc` FLOAT NULL,
  `debtusd` FLOAT NULL,
  `deferredrev` FLOAT NULL,
  `depamor` FLOAT NULL,
  `deposits` FLOAT NULL,
  `divyield` FLOAT NULL,
  `dps` FLOAT NULL,
  `ebit` FLOAT NULL,
  `ebitda` FLOAT NULL,
  `ebitdamargin` FLOAT NULL,
  `ebitdausd` FLOAT NULL,
  `ebitusd` FLOAT NULL,
  `ebt` FLOAT NULL,
  `eps` FLOAT NULL,
  `epsdil` FLOAT NULL,
  `epsusd` FLOAT NULL,
  `equity` FLOAT NULL,
  `equityavg` FLOAT NULL,
  `equityusd` FLOAT NULL,
  `ev` FLOAT NULL,
  `evebit` FLOAT NULL,
  `evebitda` FLOAT NULL,
  `fcf` FLOAT NULL,
  `fcfps` FLOAT NULL,
  `fxusd` FLOAT NULL,
  `gp` FLOAT NULL,
  `grossmargin` FLOAT NULL,
  `intangibles` FLOAT NULL,
  `intexp` FLOAT NULL,
  `invcap` FLOAT NULL,
  `invcapavg` FLOAT NULL,
  `inventory` FLOAT NULL,
  `investments` FLOAT NULL,
  `investmentsc` FLOAT NULL,
  `investmentsnc` FLOAT NULL,
  `liabilities` FLOAT NULL,
  `liabilitiesc` FLOAT NULL,
  `liabilitiesnc` FLOAT NULL,
  `marketcap` FLOAT NULL,
  `ncf` FLOAT NULL,
  `ncfbus` FLOAT NULL,
  `ncfcommon` FLOAT NULL,
  `ncfdebt` FLOAT NULL,
  `ncfdiv` FLOAT NULL,
  `ncff` FLOAT NULL,
  `ncfi` FLOAT NULL,
  `ncfinv` FLOAT NULL,
  `ncfo` FLOAT NULL,
  `ncfx` FLOAT NULL,
  `netinc` FLOAT NULL,
  `netinccmn` FLOAT NULL,
  `netinccmnusd` FLOAT NULL,
  `netincdis` FLOAT NULL,
  `netincnci` FLOAT NULL,
  `netmargin` FLOAT NULL,
  `opex` FLOAT NULL,
  `opinc` FLOAT NULL,
  `payables` FLOAT NULL,
  `payoutratio` FLOAT NULL,
  `pb` FLOAT NULL,
  `pe` FLOAT NULL,
  `pe1` FLOAT NULL,
  `ppnenet` FLOAT NULL,
  `prefdivis` FLOAT NULL,
  `price` FLOAT NULL,
  `ps` FLOAT NULL,
  `ps1` FLOAT NULL,
  `receivables` FLOAT NULL,
  `retearn` FLOAT NULL,
  `revenue` FLOAT NULL,
  `revenueusd` FLOAT NULL,
  `rnd` FLOAT NULL,
  `roa` FLOAT NULL,
  `roe` FLOAT NULL,
  `roic` FLOAT NULL,
  `ros` FLOAT NULL,
  `sbcomp` FLOAT NULL,
  `sgna` FLOAT NULL,
  `sharefactor` FLOAT NULL,
  `sharesbas` FLOAT NULL,
  `shareswa` FLOAT NULL,
  `shareswadil` FLOAT NULL,
  `sps` FLOAT NULL,
  `tangibles` FLOAT NULL,
  `taxassets` FLOAT NULL,
  `taxexp` FLOAT NULL,
  `taxliabilities` FLOAT NULL,
  `tbvps` FLOAT NULL,
  `workingcapital` FLOAT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `unique_idx` (`stock_id` ASC, `calendardate` ASC, `dimension` ASC) VISIBLE);


CREATE TABLE `dev_us_data`.`sharadar_sf3a` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `stock_id` VARCHAR(16) NOT NULL,
  `date` DATETIME NOT NULL,
  `name` VARCHAR(64) NOT NULL,
  `shrholders` FLOAT NULL,
  `cllholders` FLOAT NULL,
  `putholders` FLOAT NULL,
  `wntholders` FLOAT NULL,
  `dbtholders` FLOAT NULL,
  `prfholders` FLOAT NULL,
  `fndholders` FLOAT NULL,
  `undholders` FLOAT NULL,
  `shrunits` FLOAT NULL,
  `cllunits` FLOAT NULL,
  `putunits` FLOAT NULL,
  `wntunits` FLOAT NULL,
  `dbtunits` FLOAT NULL,
  `prfunits` FLOAT NULL,
  `fndunits` FLOAT NULL,
  `undunits` FLOAT NULL,
  `shrvalue` FLOAT NULL,
  `cllvalue` FLOAT NULL,
  `putvalue` FLOAT NULL,
  `wntvalue` FLOAT NULL,
  `dbtvalue` FLOAT NULL,
  `prfvalue` FLOAT NULL,
  `fndvalue` FLOAT NULL,
  `undvalue` FLOAT NULL,
  `totalvalue` FLOAT NULL,
  `percentoftotal` FLOAT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `unique_idx` (`stock_id` ASC, `date` ASC) VISIBLE);


CREATE TABLE `dev_us_data`.`sharadar_sf3b` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `investorname` VARCHAR(64) NOT NULL,
  `date` DATETIME NOT NULL,
  `shrholdings` FLOAT NULL,
  `cllholdings` FLOAT NULL,
  `putholdings` FLOAT NULL,
  `wntholdings` FLOAT NULL,
  `dbtholdings` FLOAT NULL,
  `prfholdings` FLOAT NULL,
  `fndholdings` FLOAT NULL,
  `undholdings` FLOAT NULL,
  `shrunits` FLOAT NULL,
  `cllunits` FLOAT NULL,
  `putunits` FLOAT NULL,
  `wntunits` FLOAT NULL,
  `dbtunits` FLOAT NULL,
  `prfunits` FLOAT NULL,
  `fndunits` FLOAT NULL,
  `undunits` FLOAT NULL,
  `shrvalue` FLOAT NULL,
  `cllvalue` FLOAT NULL,
  `putvalue` FLOAT NULL,
  `wntvalue` FLOAT NULL,
  `dbtvalue` FLOAT NULL,
  `prfvalue` FLOAT NULL,
  `fndvalue` FLOAT NULL,
  `undvalue` FLOAT NULL,
  `totalvalue` FLOAT NULL,
  `percentoftotal` FLOAT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `unique_idx` (`investorname` ASC, `date` ASC) VISIBLE);


 CREATE TABLE `dev_us_data`.`sharadar_actions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `stock_id` VARCHAR(16) NOT NULL,
  `date` DATETIME NOT NULL,
  `action` VARCHAR(64) NULL,
  `name` VARCHAR(64) NULL,
  `value` FLOAT NULL,
  `contraticker` VARCHAR(32) NULL,
  `contraname` VARCHAR(32) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `unique_idx` (`stock_id` ASC, `date` ASC) VISIBLE);


CREATE TABLE `dev_us_data`.`sharadar_daily` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `stock_id` VARCHAR(16) NOT NULL,
  `date` DATETIME NOT NULL,
  `ev` FLOAT NULL,
  `evebit` FLOAT NULL,
  `evebitda` FLOAT NULL,
  `marketcap` FLOAT NULL,
  `pb` FLOAT NULL,
  `pe` FLOAT NULL,
  `ps` FLOAT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `unique_idx` (`stock_id` ASC, `date` ASC) VISIBLE);


CREATE TABLE `dev_us_data`.`sharadar_tickers` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `stock_id` VARCHAR(16) NOT NULL,
  `table` VARCHAR(16) NOT NULL,
  `permaticker` VARCHAR(16),
  `name` VARCHAR(64),
  `exchange` VARCHAR(16),
  `isdelisted` VARCHAR(4),
  `category` VARCHAR(16),
  `cusips` VARCHAR(16),
  `siccode` VARCHAR(16),
  `sicsector` VARCHAR(16),
  `sicindustry` VARCHAR(16),
  `famasector` VARCHAR(16),
  `famaindustry` VARCHAR(16),
  `sector` VARCHAR(16),
  `industry` VARCHAR(16),
  `scalemarketcap` VARCHAR(16),
  `scalerevenue` VARCHAR(16),
  `relatedtickers` VARCHAR(16),
  `currency` VARCHAR(8),
  `location` VARCHAR(64),
  `lastupdated` DATETIME,
  `firstadded` DATETIME,
  `firstpricedate` DATETIME,
  `lastpricedate` DATETIME,
  `firstquarter` DATETIME,
  `lastquarter` DATETIME,
  `secfilings` TEXT,
  `companysite` TEXT,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `unique_idx` (`stock_id` ASC, `table` ASC) VISIBLE);


CREATE TABLE `dev_us_data`.`index_components` (
  `id` INT NOT NULL,
  `stock_id` VARCHAR(16) NOT NULL,
  `name` VARCHAR(32) NULL DEFAULT NULL,
  `weight` FLOAT NULL DEFAULT NULL,
  `index_name` VARCHAR(32) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `unique_idx` (`stock_id` ASC, `index_name` ASC) VISIBLE);


