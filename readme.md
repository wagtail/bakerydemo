Setup Cache layer for Django REST Framework
===========================================

This is a folk repository https://github.com/wagtail/bakerydemo for experiencing the building of a cache layer on top of Django Web Framework.

### Getting Started
Add `.env` file in root project folder with content:
```
MEDIA_URL=http://www.bakery.localhost/media/
STATIC_URL=http://www.bakery.localhost/static/
```

Start the docker-compose setup.
```
docker-compose up -d app
```

Access the `app` container
```
docker-compose exec app sh
```

Inside `app` container, generate sample data on the first run.
```
bin/dj-initdata.sh
bin/dj-collectstatic.sh
```

Inside `app` container, run Django server at default port `8000`.
```
bin/dj-run.sh
```

On host machine, you can access the prebuilt Django at `/admin/`, Wagtail webpage at `/`, Wagtail api (built on top of DRF) at `/api/v2/pages/` as below:
```
http://localhost:8000/
http://localhost:8000/admin/
http://localhost:8000/api/v2/pages/
```
