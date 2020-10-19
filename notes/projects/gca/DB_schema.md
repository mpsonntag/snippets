# The DB schema of the GCA-Web application

# Version 1.3

## List of relations

 Schema |          Name          | Type  | Owner 
--------+------------------------+-------+-------
 public | abstract               | table | play
 public | abstract_abstractgroup | table | play
 public | abstract_favusers      | table | play
 public | abstract_owners        | table | play
 public | abstractgroup          | table | play
 public | account                | table | play
 public | affiliation            | table | play
 public | author                 | table | play
 public | author_affiliations    | table | play
 public | banner                 | table | play
 public | conference             | table | play
 public | conference_owners      | table | play
 public | conftext               | table | play
 public | credentialslogin       | table | play
 public | figure                 | table | play
 public | play_evolutions        | table | play
 public | reference              | table | play
 public | statelogentry          | table | play
 public | topic                  | table | play

## Tables

### Table abstract

       Column       |            Type             | Collation | Nullable | Default 
--------------------+-----------------------------+-----------+----------+---------
 uuid               | character varying(255)      |           | not null | 
 acknowledgements   | character varying(300)      |           |          | 
 conflictofinterest | character varying(255)      |           |          | 
 doi                | character varying(255)      |           |          | 
 istalk             | boolean                     |           |          | 
 mtime              | timestamp without time zone |           |          | 
 reasonfortalk      | character varying(255)      |           |          | 
 sortid             | integer                     |           |          | 
 state              | character varying(255)      |           |          | 
 text               | character varying(2500)     |           |          | 
 title              | character varying(255)      |           |          | 
 topic              | character varying(255)      |           |          | 
 conference_uuid    | character varying(255)      |           |          | 
 ctime              | timestamp without time zone |           |          | 

### Table abstract_abstractgroup

     Column      |          Type          | Collation | Nullable | Default 
-----------------+------------------------+-----------+----------+---------
 abstract_uuid   | character varying(255) |           | not null |              FK abstract 
 abstrtypes_uuid | character varying(255) |           | not null |              FK abstractgroup 

### Table abstract_favusers
      Column       |          Type          | Collation | Nullable | Default 
-------------------+------------------------+-----------+----------+---------
 favabstracts_uuid | character varying(255) |           | not null |            FK abstract
 favusers_uuid     | character varying(255) |           | not null |            FK account

### Table abstract_owners
     Column     |          Type          | Collation | Nullable | Default 
----------------+------------------------+-----------+----------+---------
 owners_uuid    | character varying(255) |           | not null |               FK account
 abstracts_uuid | character varying(255) |           | not null |               FK abstract

### Table abstractgroup
     Column      |          Type          | Collation | Nullable | Default 
-----------------+------------------------+-----------+----------+---------
 uuid            | character varying(255) |           | not null | 
 name            | character varying(255) |           |          | 
 prefix          | integer                |           |          | 
 short           | character varying(255) |           |          | 
 conference_uuid | character varying(255) |           |          |              FK conference

### Table account
  Column   |            Type             | Collation | Nullable | Default 
-----------+-----------------------------+-----------+----------+---------
 uuid      | character varying(255)      |           | not null | 
 avatar    | character varying(255)      |           |          | 
 firstname | character varying(255)      |           |          | 
 fullname  | character varying(255)      |           |          | 
 lastname  | character varying(255)      |           |          | 
 mail      | character varying(255)      |           |          | 
 ctime     | timestamp without time zone |           |          | 
 mtime     | timestamp without time zone |           |          | 

### Table affiliation
   Column   |          Type          | Collation | Nullable | Default 
------------+------------------------+-----------+----------+---------
 uuid       | character varying(255) |           | not null | 
 address    | character varying(255) |           |          | 
 country    | character varying(255) |           |          | 
 department | character varying(255) |           |          | 
 position   | integer                |           |          | 
 section    | character varying(255) |           |          | 
 abstr_uuid | character varying(255) |           |          |                   FK abstract

### Table author
   Column   |          Type          | Collation | Nullable | Default 
------------+------------------------+-----------+----------+---------
 uuid       | character varying(255) |           | not null | 
 firstname  | character varying(255) |           |          | 
 lastname   | character varying(255) |           |          | 
 mail       | character varying(255) |           |          | 
 middlename | character varying(255) |           |          | 
 position   | integer                |           |          | 
 abstr_uuid | character varying(255) |           |          |                   FK abstract

### Table author_affiliations
      Column       |          Type          | Collation | Nullable | Default 
-------------------+------------------------+-----------+----------+---------
 affiliations_uuid | character varying(255) |           | not null |            FK affiliation
 authors_uuid      | character varying(255) |           | not null |            FK author

### Table banner
     Column      |          Type          | Collation | Nullable | Default 
-----------------+------------------------+-----------+----------+---------
 uuid            | character varying(255) |           | not null | 
 btype           | character varying(300) |           |          | 
 conference_uuid | character varying(255) |           |          |              FK conference

### Table conference
        Column        |            Type             | Collation | Nullable | Default 
----------------------+-----------------------------+-----------+----------+---------
 uuid                 | character varying(255)      |           | not null | 
 cite                 | character varying(255)      |           |          | 
 deadline             | timestamp without time zone |           |          | 
 description          | character varying(512)      |           |          | 
 enddate              | timestamp without time zone |           |          | 
 isopen               | boolean                     |           |          | 
 ispublished          | boolean                     |           |          | 
 link                 | character varying(255)      |           |          | 
 logo                 | character varying(255)      |           |          | 
 name                 | character varying(255)      |           |          | 
 short                | character varying(255)      |           |          | 
 startdate            | timestamp without time zone |           |          | 
 thumbnail            | character varying(255)      |           |          | 
 ctime                | timestamp without time zone |           |          | 
 geo                  | character varying(10000)    |           |          | 
 conferencegroup      | character varying(255)      |           |          | 
 haspresentationprefs | boolean                     |           |          | 
 iosapp               | character varying(255)      |           |          | 
 info                 | character varying(10000)    |           |          | 
 isactive             | boolean                     |           |          | 
 mtime                | timestamp without time zone |           |          | 
 schedule             | character varying(100000)   |           |          | 
 abstractmaxfigures   | integer                     |           |          | 
 abstractmaxlength    | integer                     |           |          | 

### Table conference_owners
      Column      |          Type          | Collation | Nullable | Default 
------------------+------------------------+-----------+----------+---------
 owners_uuid      | character varying(255) |           | not null |             FK account
 conferences_uuid | character varying(255) |           | not null |             FK conference

### Table conftext
     Column      |          Type          | Collation | Nullable | Default 
-----------------+------------------------+-----------+----------+---------
 uuid            | character varying(255) |           | not null | 
 cttype          | character varying(255) |           |          | 
 text            | character varying(512) |           |          | 
 conference_uuid | character varying(255) |           |          |              FK conference

### Table credentialslogin
    Column    |          Type          | Collation | Nullable | Default 
--------------+------------------------+-----------+----------+---------
 uuid         | character varying(255) |           | not null | 
 date         | bytea                  |           |          | 
 hasher       | character varying(255) |           |          | 
 isactive     | boolean                |           |          | 
 password     | character varying(255) |           |          | 
 salt         | character varying(255) |           |          | 
 token        | character varying(255) |           |          | 
 account_uuid | character varying(255) |           |          |                 FK account

### Table figure
   Column   |          Type          | Collation | Nullable | Default 
------------+------------------------+-----------+----------+---------
 uuid       | character varying(255) |           | not null | 
 caption    | character varying(300) |           |          | 
 position   | integer                |           |          | 
 abstr_uuid | character varying(255) |           |          |                   FK abstract

### Table reference
   Column   |          Type          | Collation | Nullable | Default 
------------+------------------------+-----------+----------+---------
 uuid       | character varying(255) |           | not null | 
 doi        | character varying(255) |           |          | 
 link       | character varying(255) |           |          | 
 position   | integer                |           |          | 
 text       | character varying(300) |           |          | 
 abstr_uuid | character varying(255) |           |          |                   FK abstract

### Table statelogentry
   Column   |            Type             | Collation | Nullable | Default 
------------+-----------------------------+-----------+----------+---------
 uuid       | character varying(255)      |           | not null | 
 editor     | character varying(255)      |           |          | 
 note       | character varying(255)      |           |          | 
 state      | character varying(255)      |           |          | 
 timestamp  | timestamp without time zone |           |          | 
 abstr_uuid | character varying(255)      |           |          |              FK abstract

### Table topic
     Column      |          Type          | Collation | Nullable | Default 
-----------------+------------------------+-----------+----------+---------
 uuid            | character varying(255) |           | not null | 
 position        | integer                |           |          | 
 topic           | character varying(255) |           |          | 
 conference_uuid | character varying(255) |           |          |              FK conference

### Table play_evolutions
    Column     |            Type             | Collation | Nullable | Default 
---------------+-----------------------------+-----------+----------+---------
 id            | integer                     |           | not null | 
 hash          | character varying(255)      |           | not null | 
 applied_at    | timestamp without time zone |           | not null | 
 apply_script  | text                        |           |          | 
 revert_script | text                        |           |          | 
 state         | character varying(255)      |           |          | 
 last_problem  | text                        |           |          | 
