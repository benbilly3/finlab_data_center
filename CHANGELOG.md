# Changelog
# [v0.1.3] - from 2020-11-17 to 2020-12-15
### Added
  - InsiderShareholdingDeclarationTransferCrawlerTW
  - deploy k8s by yaml file and kubectl and gcp command
  - service connect sql by Cloud SQL Proxy
  - sql_interface to get and update static data.
  - divide tw_data(price,month_rev_tej) to pickle
  - crontab in django Q schedule
### Fixed
  - stock-price data error, move rotc
### Chored
  - divide rotc_stock-price table

  
# [v0.1.2] - from 2020-10-22 to 2020-11-3
### Added
  - deploy on k8s
### Fixed
  - add apt git install and ssh StrictHostKeyChecking in Dockerfile 
### Chored
  - use https method to push git in tw_stock_class/finlab/git.py
  - StockListTaifex table
  - entrypoint scripts
  - mail notification format
  - google email security password
### Tested
  - tw_data crawlers
  
  
# [v0.1.1] - from 2020-10-05 to 2020-10-19
### Added
  - tw_stock_class crawlers, TwStockClassPickler, git_commit, crawl_gitlab_backup, tasks
  - tw_stock_class crawlers gitlab backup resource
  - daily crawlers report notifications by email
  - SlickchartsCrawler to get index_components and weight form dowjones,nasdaq100,sp500
  - Dockerfile and docker-compose deploy
  - guncorn wsgi server
### Fixed
  - sharadar sp500 data format
### Chored
  - add "!" as breakpoint in import_to_sql msg format,in order to sort out log
### Noted
  - Online class need pandas==1.0.3,dataframe object is diff


# [v0.1.0] - from 2020-09-06 to 2020-09-18
### Added
  - init django framework(include server, jupyter extension)
  - set db_routers and db
  - set dev and pro env to translation
  - add import_sql.py tools for df import
  - set django-Q env for cluster,tasks func, django_admin
  - sharadar-crawlers and related models in us_data
  - crawlers and related models in tw_data.
  - readme for finlab-data-center
  - import sharadar sf1 data 
  - import tw_data from old db
### Tested
  - django-Q schedule for sharadar and tw_data basic crawlers
  
