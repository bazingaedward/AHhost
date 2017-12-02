# AHhost

A Django-based WebGIS web app for data Visualization and Manipulation

---

## Demos
![screenshot](https://github.com/bazingaedward/AHhost/blob/master/screenshot.png)

## Features
- modular design
- openlayer webgis framework
- 100% finished AJAX example

## Quick Start
- 1. download source code

```
git clone git@github.com:bazingaedward/AHhost.git
```

- 2. Prepare docker images with nginx and python3.4
```
# run images with file volumn mount
docker run -it <imageName> -v ...
# get container id
docker ps -a
# start container
docker start <containerID>
# attach container with root
docker attach <containerID>
```

- 3. pip install requirement

```
pip install -r requirements.txt
git clone git@github.com:bazingaedward/AHhost.git
cd AHhost
./startsrv
```

- 4. start server

```
./startsrv
```

## Tech Stacks:
- [structFilter](https://github.com/evoluteur/structured-filter)
- [Openlayers 4](http://openlayers.org/)
- [DataTable.js](https://datatables.net/)
- [Bootstrap 3](https://getbootstrap.com/docs/3.3/components/)
- [JQuery UI 1.12.1](https://jqueryui.com/)
- [JQuery](https://jquery.com/)
- [Webpack](http://webpack.github.io/)
- [Docker](https://www.docker.com/)

## Django Installed apps
- django-cms<3.5
- djangocms-admin-style>=1.2,<1.3
- django-treebeard>=4.0,<5.0
- djangocms-file
- djangocms-text-ckeditor>=3.2.1
- djangocms-link>=1.8
- djangocms-style>=1.7
- djangocms-googlemap>=0.5
- djangocms-snippet>=1.9
- djangocms-video>=2.0
- djangocms-column>=1.6
- django-pandas
- django-filebrowser
- easy_thumbnails
- django-filer>=1.2
- cmsplugin-filer>=1.1
- Django<1.9
- pytz
- django-classy-tags>=0.7
- html5lib>=0.999999,<0.99999999
- Pillow>=3.0
- django-sekizai>=0.9
- six
- requests
- bs4
- numpy
- pandas
- xlrd
- sqlalchemy
- rasterstats
- pyshp
- netCDF4
- geojson

## License
[MIT](https://tldrlegal.com/license/mit-license)
