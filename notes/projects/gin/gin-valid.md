## Notes on how to set up the gin-valid service

- create folder structure

    ```bash
    VALID_ROOT=/data/web/valid
    mkdir -vp $VALID_ROOT/config
    mkdir -vp $VALID_ROOT/valid-dockerfile
    mkdir -vp $VALID_ROOT/results
    ```

- create compose env file

    ```bash
    sudo sh -c "echo 'COMPOSE_PROJECT_NAME=ginvalid' > ${VALID_ROOT}/valid-dockerfile/.env"
    ```

- provide `docker-compose.yml` in $VALID_ROOT/valid-dockerfile and `cfg.json` in $VALID_ROOT/config

- change ownership to `gnode` user and `deploy` group

    ```bash
    sudo chown -R gnode:deploy $VALID_ROOT
    ```

- the service requires a user named "gin-valid" on the running gin instance it is supposed to work with.

## gin-valid config file (cfg.json)

```json
{
    "settings": {
        "rooturl": "https://valid.dev.g-node.org",
        "ginuser": "gin-valid",
        "ginpassword": "[add password here]",
        "hooksecret": "[add secret here]"
    },
    "ginaddresses": {
        "weburl": "https://gin.dev.g-node.org:443",
        "giturl": "git@gin.dev.g-node.org:22"
    }
}
```

## gin-valid docker-compose file

Do not expose ports in live setup; handle port mapping via the apache config

```yaml
version: '3.8'
services:
  valid:
    image: gnode/gin-valid:latest
    volumes:
      - ../config:/gin-valid/config
      - ../results:/gin-valid/results
      - tokens:/gin-valid/tokens
    restart: unless-stopped
    networks:
      net:
        ipv4_address: 172.12.0.10
       aliases:
         - ginvalid
    logging:
      driver: "json-file"
      options:
        max-size: "1m"
        max-file: "10"

volumes:
  tokens:

networks:
  net:
    ipam:
      driver: default
      config:
        - subnet: 172.12.0.0/16
          gateway: 172.12.0.254
```

Note that you can find a previous version of the live docker-compose file in the addendum.

## apache config

```
VirtualHost valid.dev.g-node.org:80>
    ServerName valid.dev.g-node.org
    ServerAdmin dev@g-node.org

    RewriteEngine on
    RewriteCond %{SERVER_NAME} =valid.dev.g-node.org
    RewriteRule ^ https://%{SERVER_NAME}%{REQUEST_URI} [END,NE,R=permanent]
</VirtualHost>

<VirtualHost valid.dev.g-node.org:443>
    ServerName valid.dev.g-node.org

    SSLEngine On
    SSLCertificateFile /etc/letsencrypt/live/valid.dev.g-node.org/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/valid.dev.g-node.org/privkey.pem
    Include /etc/letsencrypt/options-ssl-apache.conf

    ProxyPreserveHost  On
    ProxyRequests Off
    ProxyPass / http://172.12.0.10:4044/
    ProxyPassReverse / http://172.12.0.10:4044/
</VirtualHost>
```

## Add a GIN "gin-valid" user

On the connected gin instance, add a user named "gin-valid" with the password used in the `cfg.json` file (or use a different password and change it in the config file; your cup of tea).

The gin-valid service should now be ready to go.

# Local development setup

A setup for local development needs a different approach. All containers will live within the same docker network and communicate mostly via the internal network. For the setup of the local gin and the gin-client to work with a local gin server, please consult the gin in-house setup guide.

## Set up a local gin server

Set up a local gin server along the lines of the in-house gin project. The resulting directory structure should look like the following:

```
$GIN_ROOT_FOLDER
├── config
|   ├── postgres
|   |   └── pgressecrets.env
|   └── gogs
|       ├── notice
|       |   └── banner.md   # GIN page notice banner
|       ├── public          # custom frontend style
|       └── templates       # custom frontend files
├── volumes
|   └── ginweb
├── gindata
|   ├── gin-postgresdb
|   └── gin-repositories
└── gin-dockerfile
    ├── .env
    └── docker-compose.yml
```

## Add gin-valid directories

Add the following directories to accommodate the additional gin-valid requirements:

```
mkdir -vp $GIN_ROOT_FOLDER/valid/config
mkdir -vp $GIN_ROOT_FOLDER/valid/results
```

## Add a gin-valid config file

Add a `cfg.json` config file at `$GIN_ROOT_FOLDER/valid/config`. The directory structure should now look like this:

```
$GIN_ROOT_FOLDER
├── config
|   ├── postgres
|   |   └── pgressecrets.env
|   └── gogs
|       ├── notice
|       |   └── banner.md   # GIN page notice banner
|       ├── public          # custom frontend style
|       └── templates       # custom frontend files
├── valid
|   ├── config
|   |   └── cfg.json
|   └── results
├── volumes
|   └── ginweb
├── gindata
|   ├── gin-postgresdb
|   └── gin-repositories
└── gin-dockerfile
    ├── .env
    └── docker-compose.yml
```

## Update the docker-compose file

Update the existing gin docker-compose file to accommodate gin-valid in the same local network:

```yaml
version: '3.8'
services:

  web:
    image: gnode/gin-web:dev
    volumes:
      - ../gindata/gin-repositories:/data/repos:rw
      - ../volumes/ginweb:/data:rw
      - ../config/gogs:/custom:rw
      - gintmp:/data/tmp:rw
    restart: always
    environment:
      - PUID=1000      # 'ginuser' user id
      - PGID=2000      # 'ginservice' group id
      - GOGS_CUSTOM=/custom
    ports:
      - "2121:22"
      - "3000:3000"
    networks:
      net:
        ipv4_address: 172.13.0.10
        aliases:
          - ginweb
    depends_on:
      - db
    logging:
      driver: "json-file"
      options:
        max-size: "1m"
        max-file: "10"

  db:
    image: postgres:11
    env_file: ../config/postgres/pgressecrets.env
    restart: always
    networks:
      net:
        aliases:
          - ginpgres
    volumes:
      - ../gindata/gin-postgresdb:/var/lib/postgresql/data:rw
    logging:
      driver: "json-file"
      options:
        max-size: "1m"
        max-file: "10"

  valid:
    image: gnode/gin-valid:dev
    volumes:
      - ../valid/config:/gin-valid/config
      - ../valid/results:/gin-valid/results
      - tokens:/gin-valid/tokens
    ports:
      - "4044:4044"
    networks:
      net:
       aliases:
         - ginvalid
    depends_on:
      - web
    logging:
      driver: "json-file"
      options:
        max-size: "1m"
        max-file: "10"

volumes:
  gintmp:
  tokens:

networks:
  net:
    ipam:
      driver: default
      config:
        - subnet: 172.13.0.0/16
          gateway: 172.13.0.254
```

## Update the config file

Update the config file to contain the following information:

```json
{
    "settings": {
        "rooturl": "http://localhost:4044",
        "ginuser": "gin-valid",
        "ginpassword": "ginvalid",
        "hooksecret": "localhook"
    },
    "ginaddresses": {
        "weburl": "http://ginweb:3000",
        "giturl": "git@ginweb:22"
    }
}
```

## Add a GIN "gin-valid" user

On the local gin instance, add a user named "gin-valid" with the password used in the `cfg.json` file (or use a different password and change it in the config file; your cup of tea).

The service should now be available.


## Activate webhooks on a local setup

Webhooks do not work out of the box in a local setup. The following procedure is required to enable them:

- log into the local gin-valid instance
- enable the webhook for a specific repository
- the webhook now has been created on the local gin repository
- access the 'webhook' menu option in the repository setting on the locally running gin instance
- change the Payload URL from e.g. "http://localhost:4044/validate/odml/gin-valid/odmlFiles" to the docker alias set for gin-valid. In our docker-compose.yml example this would be "ginvalid"; so the payload URL should be changed to "http://ginvalid:4044/validate/odml/gin-valid/odmlFiles".
- test the webhook via the "Test delivery" option on the gin webhook setting page


# Addendum

## previous docker-compose version


```yaml
version: '2.4'
services:
  valid:
    image: gnode/gin-valid:latest
    volumes:
      - cfg:/gin-valid/config
      - tokens:/gin-valid/tokens
      - results:/gin-valid/results
    restart: unless-stopped
    networks:
      net:
        ipv4_address: 172.12.0.10
        aliases:
          - ginvalid

volumes:
  webdata:
  repos:
  webtmp:
  cfg:
    driver: "local"
    driver_opts:
      type: "none"
      o: "bind"
      device: "/data/web/valid/config"
  tokens:
  results:
    driver: "local"
    driver_opts:
      type: "none"
      o: "bind"
      device: "/data/web/valid/results"

networks:
  net:
    ipam:
      driver: default
      config:
        - subnet: 172.12.0.0/16
```
