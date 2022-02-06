# Finlab_Data_Center by Django

## Purpose
Use Django framework to make a data-center website, in order to schedule crawlers or ETL functions by django-Q, which is a multiprocessing task queue for Django and has high performance and easy way to controll in django-admin website. 
In order to monitor ETL processes, we store the hook result(log) in django_admin database, then we could use these data to push and analysis info to our web or third party.

## Data Flow
![](https://i.imgur.com/7ag8rpu.jpg)


## Data center basic env framework
![](https://i.imgur.com/Cx2Brvl.jpg)

## MySQL Auth
```
mysql -u root
CREATE USER 'finlab'@'localhost' IDENTIFIED BY 'finlab';
GRANT ALL PRIVILEGES ON * . * TO 'finlab'@'localhost';

# change passward
ALTER USER 'finlab'@'localhost' IDENTIFIED BY 'passward';
```
## TW_stock_setup
```
git clone https://gitlab.com/finlab_company_class/tw_stock.git
cp -r tw_stock/data finlab_data_center/tw_stock_class/
```

### GCP Cloud SQL:
add [IP4(search)](http://ipv4.whatismyv6.com/) in gcp sql connection
## Django command
### static file

[use for django admin css no show in gunicorn server,run this command at first time in local use ](https://zhuanlan.zhihu.com/p/31475023)
`python manage.py collectstatic`

### Set env and install module

```
virtualenv venv
source venv/bin/activate
# primary module
pip install -r requirements-to-freeze.txt
# related module in requirements.txt
pip freeze > requirements.txt
```


### DB related command
Only admin_db router could be migrate, because we need elastic in stock database.Use raw sql to define tables in stock database, remember to record raw sql files in  sql-records directory.


```
# default setting is dev
python manage.py migrate --database=admin_db
python manage.py migrate --settings=finlab_data_center.settings.pro --database=admin_db
```
### Create superuser
`python manage.py createsuperuser --database=admin_db`

### Run jupyter by django-plus kernal
`python manage.py shell_plus --notebook`

#### add below code in ipynb file to connect django env
```
import sys,os
sys.path.append("..")
import django
django.setup()
```

### Run python shell
`python manage.py shell`

### Run Server
```
# only test
python manage.py runserver
# use gunicorn in production for security
gunicorn finlab_data_center.wsgi:application
```


### Start app
`python manage.py startapp us_data`

### [Inspect DB](https://docs.djangoproject.com/en/3.1/howto/legacy-databases/)
use legacy db to export django-model format in model file
`python manage.py inspectdb --database=us_db > us_data/models.py`
## Create New Table Flow
1. Define raw sql, and paste raw sql in records dir.
2. Use inspectdb to print model codes in django
   ex:
   ```
    # show on terminal
    python manage.py inspectdb --database=us_db
    # export to modelfile
    python manage.py inspectdb --database=us_db > us_data/models.py
    ```

3. Write crawlers and use `CrawlerProcess.specified_date_crawl or SqlImporter.add_to_sql` to create and test init data,**don't use CrawlerProcess.auto_update_crawl firstly**.
   

## Crawlers
use etl/import_sql.py to control crawlers to import data.
### Demo

1. tw_data
![tw_data](https://i.imgur.com/sSnOcXg.png)

2. us_data
![us_data](https://i.imgur.com/mkyzD3r.png)

## [Django Q](https://django-q.readthedocs.io/en/latest/index.html)
### Run django-Q
`python manage.py qcluster`
### Use task func
we have two task funcs(to process for time series or non time series) and one hook func.

![](https://i.imgur.com/uT83NqY.jpg)
### [Set django-Q cluster](https://django-q.readthedocs.io/en/latest/configure.html)
![](https://i.imgur.com/RGhkkFh.jpg)
### [Set django-Q admin_site](https://django-q.readthedocs.io/en/latest/admin.html?highlight=admin#admin-pages)
![](https://i.imgur.com/yEWyYLe.jpg)
### Schedule board
![](https://i.imgur.com/a7uDGgl.png)
### CRUD for tasks
args only accept str or number

![](https://i.imgur.com/OyeqNLX.png)
![](https://i.imgur.com/w9te1ol.png)


## File framework for app
1. crawlers.py: write crawlers
2. tasks.py: write schedule task functions
3. models.py: define data format.
## Notifications
use email to sent schdule daily report

## Server(Gunicorn)
## Deploy

### Docker command(see /scripts)

#### build、tag、push
```
docker build -t finlab-data-center -f Dockerfile .

docker tag finlab-data-center asia.gcr.io/rare-mender-288209/finlab-data-center:v0.1.3

docker push asia.gcr.io/rare-mender-288209/finlab-data-center:v0.1.3
```
#### run
```
docker run --env PORT=8001 --env DJANGO_ENV=pro -it -p 8001:8001  finlab-data-center
```

#### use volume,Synchronous update with local, no need to rebuild

```
docker run --env PORT=8001 --env DJANGO_ENV=pro -it -p 8001:8001 -v "$(pwd):/app" finlab-data-center /bin/bash
```
### [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine/docs/tutorials/hello-app?hl=zh-tw)

#### Create Cluster
```
# init
gcloud config set project rare-mender-288209
gcloud config set compute/zone asia-east1-a

gcloud container clusters create finlab-micro-service --num-nodes=1

gcloud container clusters get-credentials finlab-micro-service

kubectl create deployment finlab-data-center --image=asia.gcr.io/rare-mender-288209/finlab-data-center:v0.1.3

kubectl expose deployment finlab-data-center --type LoadBalancer \
  --port 80 --target-port 8001

kubectl delete service finlab-data-center

gcloud container clusters delete finlab-data-center
```
#### [GKE connect to Cloud SQL Proxy](https://cloud.google.com/sql/docs/mysql/connect-kubernetes-engine)

##### [medium reference](https://medium.com/google-cloud/connecting-cloud-sql-kubernetes-sidecar-46e016e07bb4)

##### 1.use secret to set env args, sql proxy host must be localhost
```
kubectl create secret generic cloudsql-db-credentials --from-literal=DBACCOUNT=finlab_admin --from-literal=DBPASSWORD=qetuadgj --from-literal=DBHOST=127.0.0.1
```
##### [2.create service account](https://blog.johnwu.cc/article/gcp-kubernetes-connect-to-cloudsql.html)
##### 3.set iam service account key
```
gcloud iam service-accounts keys create ~/key.json \
  --iam-account cloudsql-instance@rare-mender-288209.iam.gserviceaccount.com

kubectl create secret generic cloudsql-instance-credentials --from-file=service_account.json="/Users/benbilly3/key.json"
```

### first deploy(use k8s_deploy.yaml)

#### [how to write k8s deploy yaml?](https://github.com/GoogleCloudPlatform/cloudsql-proxy/blob/master/examples/kubernetes/proxy_with_sa_key.yaml) 
`kubectl create -f k8s_deploy.yaml `
### rolling update(change image version)
`kubectl set image deployment/finlab-data-center finlab-data-center=asia.gcr.io/rare-mender-288209/finlab-data-center:v0.1.3`
## Other notes
1. config_json: note env args like db connection, api_key
2. db_router.py: control multiple db connection
3. settings dir: default env setting is dev, both two env are inherited from base.py. django-controller is setting in base.py.
4. CHANGELOG.md: record work comments gor everyversion
5. /scripts:record the command.sh

## Reference 
[Django](https://www.djangoproject.com/)

[Django-Q](https://django-q.readthedocs.io/en/latest/)

[Django-Q introduce in PyCon ](https://www.youtube.com/watch?v=Ljs9e0kI7Ow)

[Asynchronous tasks in Django with Django Q](https://www.valentinog.com/blog/django-q/)

[GKE](https://cloud.google.com/kubernetes-engine/docs/tutorials/hello-app?hl=zh-tw#cloud-shell_3)
[Asynchronous tasks in Django with Django Q](https://www.valentinog.com/blog/django-q/)