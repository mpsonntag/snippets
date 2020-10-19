Postgres
========


## Install postgres (Linux)

    apt-get install postgresql

- Postgres will be installed to `/etc/postgresql/[version]/`
- It sets up a superuser "postgres"
- It already sets up a couple of demons that are listening to requests
- Check where the demons are listening:
       `netstat -l`    ... shows all listening demons by their name
    or
       `netstat -lt`   ... shows all listening demons by their Local address

- Postgres listens by default on port 5432 e.g. 127.0.0.1:5432
- To check how one can connect to the database, open `/etc/postgresql/[version]/main/pg_hba.conf`


## Create user and database

- First open the postgres terminal using the superuser "postgres"

        sudo -u postgres psql

- Now we are connected to the postgres terminal. To look up which commands are available:

       \?

- Check which databases are currently available:

        \l ... should print the main "postgres" db and two templates

- Check which roles (~users) are currently available:

       \d  ... should return no relations

- List all schemas

        \dn

- List all users

        \du

- List all tables in a database

        \d

- List columns of a table

        \d table_name

- First we need to connect to the main database "postgres" ... This database contains all information about installed roles and databases. Here we also add new users and databases

        \c postgres

- Now we are connected to database "postgres" with superuser "postgres"
- Now we create a normal user for our first database

        CREATE ROLE play WITH LOGIN PASSWORD 'play'; ... This creates user "play" and this user can login to databases using password "play".

- If we check the available roles:

       \du   ... we will see the users "postgres" and "play" with their attributes.

- Now we create our first database:

       CREATE database playground OWNER play;    ... this does exactly what it looks like.

- If we check our available databases with `\l` we will see, that "playground" has been added with owner "play"
- We can log out of the postgres terminal by using `\q`

- We can log into our new database with our new user:

       psql -U play -h localhost playground

- Here we can create a couple of tables e.g. "swingset" with columns "plank" and "tire".
- Now we can list, which tables are available using `\d`
- We can also display the table setup using `\d swingset`


## Connecting to database

- Connect to an existing database:

        psql -h [hostname] -d [database] -U [user]

        // Example:
        psql -h localhost -d testDB -U testUser


## Export table data

To dump data from a table to an sql file:

    pg_dump -U database_user -h localhost -t column_name --data-only --column-inserts database_name > outputfile.sql

The `-t` option can be chosen multiple times. 

## Run sql script

at the psql prompt do this:

    \i <sqlfile>

## Run sql script from the shell

    psql -d[database] -U[user] -a -f [sql script]
    e.g.
    psql -UtestUser -dtestDB -a -f /tmp/lastBackup.sql 


## Useful commands

Display column details and relations of a specific table

    \d+ <table name>

# Resources

- [The Internals of PostgreSQL](http://www.interdb.jp/pg/index.html)
