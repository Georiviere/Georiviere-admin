# Georiviere-admin

# Hébergement

## Mots de passe

https://password.makina-corpus.net/#/workspaces/w/makinacorpus-passwords/vaults/v/django/cards/c/georiviere/secrets

## Serveur de préprod (Staging)

https://staging-georiviere-admin.makina-corpus.net/

* accès via :

```bash
ssh georiviereadmin-staging@staging-georiviere-admin.makina-corpus.net
```  

check @rde si votre clé ssh ne vous permet pas de vous connecter

Dossier du projet :

```bash
cd /srv/docker-envs/georiviereadmin-staging/georiviere
``` 

utilisateur à utiliser :

```bash
georiviereadmin-staging
```


## Development install

```
cp .env.dist .env
docker-compose build
docker-compose up -d postgres
docker-compose up
docker-compose run --rm web ./manage.py migrate
docker-compose run --rm web ./manage.py compilemessages
docker-compose run --rm web ./manage.py createsuperuser
```

# Commands

* import_stations

```bash
./manage.py import_stations --department 35,29,01
```

Load all stations in provided departments

Integrer les types de descriptions :
```
docker-compose run --rm web ./manage.py loaddata description.json
```

## Credits

* Geotrek Team & credits
* Makina Corpus

Icons :

* Stream : Creative Commons, Adrien Coquet, FR
* Work : construction sign work from [SVG Repo](https://www.svgrepo.com/svg/307735/construction-sign-work) - CC0
* Observation : observation from [SVG Repo](https://www.svgrepo.com/svg/293710/observation) - CC0
* Knowledge : idea from [SVG Repo](https://www.svgrepo.com/svg/293713/idea) - CC0
* Finance & administration : report from [SVG Repo](https://www.svgrepo.com/svg/58321/report) - CC0
* Studies : research from [SVG Repo](https://www.svgrepo.com/svg/109479/research)
* Description : Makina Corpus, derivated from [SVG Repo](https://www.svgrepo.com/svg/258092/route-start) - CC0
