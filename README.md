# Safe dict

## Application architecture

Application contains two projects, js project located in `frontend` directory responsible for client side, and second python project located in `backend` responsible for server side computing.

### Backend project structure

### `db `module

Module responsible for connection with MySQL DB, uses [SQLalchemy ORM](http://docs.sqlalchemy.org/en/latest/orm/) framework for DB connectivity and [tornado.concurrent](http://www.tornadoweb.org/en/stable/concurrent.html) to calling a blocking methods asynchronously.

## `scrapper` module

Module responsible for scrapping whole webpages as text, uses [tornado.httpclient](http://www.tornadoweb.org/en/stable/httpclient.html) for asynchronously requests.

## `witai` module

This module exposes api to [wit.ai](https://wit.ai/) service, [tornado.httpclient](http://www.tornadoweb.org/en/stable/httpclient.html) for asynchronously requests.

## `server` module

This is module responsible for exposing Microservise-api for ordinary users, only for writing (insert, update) on database. **For safety this module and any of its dependencies should not use private key.** 


## `server-admin` module

This is module responsible for exposing Microservise-api for admin and allows to read from db.

## `train` module

This is module train our service with data provide by Wikipedia.

## Quickstart for developing

1. Start mysql db from backend/docker-compose.yml
2. DB structure will be created during first start of module `server` or `server_admin`, in case of concurrent first start of both modules there is a high probability of conflict between instances
3. Install node dependencies by `yarn` for js projected based in `frontend` directory

## Deploying on production

1. Build images using Dockerfiles from root of this project (`Dockerfile.nginx`, `Dockerfile.python`, `Dockerfile.python-admin`) and put in magic way (there is need to change it) secrets into images. *Remember to not put **private** key into `dict-python` image*
2. Move images on production environment. [helpful stackoverflow comment](https://stackoverflow.com/a/23938978)
3. Start using `docker-compose.yml` from root (don't mismatch with this from `backend` project). Remember to set env variables for DB directory and port

## Roadmap
Here are things that are needed to be improved.
1. Tests - there is no comments.
2. Frontend - it's look terrible, there is need to add some styles.
3. Develop better way to distribute secrets. Inserting secrets in magic way into images is very bad idea because we will want to put our images in some internal docker registry, but there will be great time to change it during migration to ci/cd in place of manual deployment.
4. Some setting system better than raw parsing of yml.
5. Typing in crucial places (it will help us, help IDE to suggest types).
6. Some TODOs and comments left in code.