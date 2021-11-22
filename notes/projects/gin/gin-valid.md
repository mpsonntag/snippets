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
