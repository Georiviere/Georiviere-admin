Publication
===========

CI
--

* Each edition runs a CI build.
* All GeoRiviere-admin maintainers can review or merge Pull Requests.
* First time contributor not in maintainer team can request to be added. Maintainers can accept its first pull request to allow CI build.


Release
-------

To release a new version :

* set version to georiviere/VERSION file.
* set changelog infos in docs/changelog.rst
* push or merge to master
* Go to https://github.com/Georiviere/Georiviere-admin/releases.
* Click on "Draft a new release"
* set new tag according older ones.
* Copy / paste changelog for version in release notes.
* In the end, CI publish publish new docker image to github packages.


Docker image
------------

* Docker image is published after each release in Georiviere github repository: ghcr.io/georiviere/georiviere-admin:latest
