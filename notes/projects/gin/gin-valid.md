## notes on how to setup gin-valid

- create folder structure

    ```bash
    mkdir -vp /data/web/valid/config
    mkdir -vp /data/web/valid/docker
    mkdir -vp /data/web/valid/results
    ```

- create compose env

    ```bash
    sudo sh -c "echo 'COMPOSE_PROJECT_NAME=ginvalid' > /data/web/valid/config/.env"
    ```

- provide `docker-compose.yml` in /data/web/valid/docker and `cfg.json` in /data/web/valid/config

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
