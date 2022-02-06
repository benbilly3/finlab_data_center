docker run --env PORT=8001 --env DJANGO_ENV=pro -it -p 8001:8001  finlab-data-center
docker run --env PORT=8001 --env DJANGO_ENV=pro -it -p 8001:8001 -v "$(pwd):/app" finlab-data-center /bin/bash