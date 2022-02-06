docker build -t finlab-data-center -f Dockerfile .

docker tag finlab-data-center asia.gcr.io/rare-mender-288209/finlab-data-center:v0.1.3-3

docker push asia.gcr.io/rare-mender-288209/finlab-data-center:v0.1.3-3

kubectl set image deployment/finlab-data-center finlab-data-center=asia.gcr.io/rare-mender-288209/finlab-data-center:v0.1.3-3