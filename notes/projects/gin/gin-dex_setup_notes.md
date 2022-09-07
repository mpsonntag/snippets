# setting up gin-dex / elasticsearch alongside a gin webservice

## GIN-Dex

[GIN Indexing service](https://github.com/G-Node/gin-dex).  Feeds data into the [Elasticsearch](#elasticsearch) service.


### Docker compose GIN-Dex section

```yaml
  dex:
    image: gnode/gin-dex:latest
    env_file: ../config/gindex/config.env
    entrypoint: ./gindex
    restart: always
    networks:
      net:
        aliases:
          - gindex
    depends_on:
      - "elasticsearch1"
    volumes:
      - ../gindata/gin-repositories:/repos:ro
      - esstore1:/usr/share/elasticsearch/data:rw
```

#### GIN-Dex configuration

The indexing service is configured in the same manner as the DOI service: An `env_file` can be provided to the container to configure a number of options.  Unlike the DOI service, however, we mostly just use the default values for these, so no configuration is really necessary.

Required options:
- `elastic_url`: The address of the [Elasticsearch](#elasticsearch) service.  The GIN-Dex service should always run on the same machine as the Elasticsearch service, so this can just be the alias of the ES Docker container with the default port (`elastic_url=http://elasticsearch1:9200`).
- `repository_store`: The full path to the GIN repositories that the service will be indexing.  From the *compose* section above, this would be `/repos`.  Note that the volume is mounted in `read-only` mode, since the indexing service only needs to be able to read repository data (`repository_store=/repos`).
- `port`: The port that the indexing service will be listening on.
- `key`: The encryption key, shared with GIN Web for verification.


#### GIN-Dex volumes

- `../gindata/gin-repositories:/repos:ro`: The storage location of the GIN repositories, mounted `read-only`, so that the indexing service can scan and index the repository data.
- `esstore1:/usr/share/elasticsearch/data:rw`: This is not necessary and was probably added as a mistake.  *Needs Review.*


#### GIN-Dex ports

The indexing service requires one port that should be accessible to the web service and included in the GIN-Web configuration, along with the address of GIN-Dex.  The web service sends requests to the indexing service to invoke indexing tasks and to perform searches.


### Changes to the GIN-Dex service configuration

Older version of the GIN-Dex service would accept command line arguments for configuration during startup (much like the GIN-DOI service).


## Elasticsearch

The Elasticsearch service provides indexing and search functionality to GIN-Web through GIN-Dex.


### Docker compose Elasticsearch section

```yaml
  elasticsearch1:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.2.0
    container_name: elasticsearch1
    environment:
      - node.name=elasticsearch1
      - discovery.seed_hosts=elasticsearch2
      - cluster.name=docker-cluster
      - cluster.initial_master_nodes=elasticsearch1,elasticsearch2
      - xpack.license.self_generated.type=basic
      - path.repo=/usr/share/elasticsearch
      - bootstrap.memory_lock=true
      - "ES_JAVA_OPTS=-Xms2g -Xmx2g -Des.enforce.bootstrap.checks=true"
    env_file: ../config/elasticsearch/elasticsecrets.env
    restart: always
    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile:
        soft: 65536
        hard: 65536
    mem_limit: 8g
    networks:
      net:
        aliases:
          - elasticsearch1
    volumes:
      - esstore1:/usr/share/elasticsearch/data:rw

  elasticsearch2:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.2.0
    container_name: elasticsearch2
    environment:
      - node.name=elasticsearch2
      - discovery.seed_hosts=elasticsearch1
      - cluster.name=docker-cluster
      - cluster.initial_master_nodes=elasticsearch1,elasticsearch2
      - xpack.license.self_generated.type=basic
      - path.repo=/usr/share/elasticsearch
      - bootstrap.memory_lock=true
      - "ES_JAVA_OPTS=-Xms2g -Xmx2g -Des.enforce.bootstrap.checks=true"
    env_file: ../config/elasticsearch/elasticsecrets.env
    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile:
        soft: 65536
        hard: 65536
    mem_limit: 8g
    restart: always
    networks:
      net:
        aliases:
          - elasticsearch2
    volumes:
      - esstore2:/usr/share/elasticsearch/data:rw
```


#### Elasticsearch configuration

The Elasticsearch service is configured through environment variables that are provided in the docker-compose file (see section above).  These could be moved to a single `env_file` for consistency with the DOI and indexing services.

- `cluster.name=docker-cluster`: The cluster under which this node will be run.  By default (or perhaps convention?), when running Elasticsearch in a docker container, the cluster name `docker-cluster` is used.
- `xpack.license.self_generated.type=basic`: This enables the free basic license for Elasticsearch.  This disables all X-Pack features that are not included in the free version.
- `path.repo=/usr/share/elasticsearch`: The path to the storage location for the indexing.
- `bootstrap.memory_lock=true`: Prevents the Elasticsearch memory form being swapped out of RAM.
- `"ES_JAVA_OPTS=-Xms1024m -Xmx1024m"`: JVM options for memory allocation and limits.

The `env_file` (`env_file: ../config/elasticsearch/elasticsecrets.env`) contains the password for the service, defined as `ELASTIC_PASSWORD`.

#### HOST MACHINE CONFIGURATION

Whether running in a container or not, the `vm.max_map_count` on the **host** machine needs to be increased, otherwise Elasticsearch fails with out of memory errors.
See [this page of the ES docs](https://www.elastic.co/guide/en/elasticsearch/reference/current/vm-max-map-count.html).

To increase the system limit permanently, create a file `/etc/sysctl.d/80-elasticsearch.conf` and add the following:
```
vm.max_map_count=262144
```

To set the new limit, you need to reboot the system or run:
```
sysctl --system
```
to reload all configuration files or:
```
sysctl -w vm.max_map_count=262144
```
to set the new limit directly.

#### Elasticsearch volumes

The `esstore` volume is the location where the indexes are stored for the Elasticsearch service.  This location doesn't need to be exposed, but it is named in order to persist across restarts of the service.  If need be, the data can be bound to a directory on the host machine, or copied out, at a later date.  The indexes aren't critical however, since a reindex can be performed at any time, although it can be a bit I/O and perhaps processor intensive.


#### Elasticsearch ports

No ports should be exposed from the Elasticsearch service.  The only other service that communicates with Elasticsearch is the GIN-Dex (indexing) service, which should always run on the same machine.  The internal Docker network should be used to connect the two services and they can address one another using the specified aliases.


## Config files and file updates

### gogs config entry

**GIN DEX** related settings:
- `INDEX_URL`: Address for the gin-dex service's `/index` route (depends on local Docker configuration and container names).
- `SEARCH_URL`: Address for the gin-dex service's `/search` route.
- `SEARCH_KEY`: Shared encryption key for encrypting requests and decrypting responses.

$GIN_ROOT/config/gogs/conf/app.ini

    ```
    [search]
    INDEX_URL = http://gindex:[define port]/index
    SEARCH_URL = http://gindex:[define port]/search
    SEARCH_KEY = [some key]
    ```

### gin-dex config file

$GIN_ROOT/config/gin-dex/config.env

    ```
    elastic_url=http://elasticsearch1:[defined elastic search port e.g. default 9200]
    repository_store=[docker gin container repository directory e.g. /repos]
    port=[defined port for index and search from app.ini]
    key=[defined gin-dex key; compare to config/gogs/conf/app.ini]
    ```

### elasticsearch config file

$GIN_ROOT/config/elasticsearch/elasticsecrets.env

    ```
    ELASTIC_PASSWORD=[some password]
    ```

