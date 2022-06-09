## notes on how to setup gin-valid

TODO
- simplify folder structure
- update docker-compose to newer version

- create folder structure

    ```bash
    VALID_ROOT=/data/web/valid
    mkdir -vp $VALID_ROOT/config
    mkdir -vp $VALID_ROOT/docker
    mkdir -vp $VALID_ROOT/results
    ```

- create compose env

    ```bash
    sudo sh -c "echo 'COMPOSE_PROJECT_NAME=ginvalid' > ${VALID_ROOT}/docker/.env"
    ```

- provide `docker-compose.yml` in $VALID_ROOT/docker and `cfg.json` in $VALID_ROOT/config

- change ownership to `gnode` user and `deploy` group

    ```bash
    sudo chown -R gnode:deploy $VALID_ROOT
    ```

- the service requires a user named "gin-valid" on the running gin instance it is supposed to work with.

## cfg.json file

```json
{
    "settings": {
        "rooturl": "https://valid.gin.g-node.org",
        "ginuser": "gin-valid",
        "ginpassword": "[add password here]",
        "hooksecret": "[add secret here]"
    },
    "ginaddresses": {
        "weburl": "https://gin.g-node.org:443",
        "giturl": "git@gin.g-node.org:22"
    }
}
```

## docker-compose file

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
        ipv4_address: 172.19.0.10
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
        - subnet: 172.19.0.0/16
```
