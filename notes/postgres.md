Get long-running queries:
[ref](https://www.postgresql.org/docs/current/monitoring-stats.html#MONITORING-PG-STAT-ACTIVITY-VIEW)

```
SELECT pid, now() - query_start AS age, usename, query
FROM pg_stat_activity
WHERE age(clock_timestamp(), query_start) > interval '10 second'
	AND state != 'idle'
ORDER BY age DESC;
```

Fast table count estimate:
- [ref](https://wiki.postgresql.org/wiki/Count_estimate)

```
SELECT reltuples FROM pg_class WHERE relname = '<table>';
```

Query on random sampling of table:
- works best when table size is much greater than physical page size
- [ref](https://wiki.postgresql.org/wiki/Count_estimate)

```
SELECT <selection> FROM <table> TABLESAMPLE SYSTEM(<percentage 0.0 to 100.0>) WHERE <condition>;
```

# performance
## Why isn't Postgres using my index?
### When the index is new
Postgres decides on an execution plan based on internal state it keeps. It offers no insights into how it came up with an execution plan. In general, internal state is created over time, and there's no guarantee it is accurate after an index is created. Simply, postgres doesn't fully know what an index does after it's created. Autovacuuming seems to be the normal method for internal state to be updated. There's two manual queries we can do to spur internal state updates:

This one sounds right and works in some cases:
```
ANALYZE <table>
```

This one doesn't sound useful, but it's what postgres will do over time, now:
```
VACUUM <table>
```
In particular, this seems to be necessary for an index-only scan. I'm unclear if `ANALYZE` handles any cases that `VACUUM` does not.

# psql
## peer authentication failed for user
Peer is an authentication method that's a default in a bunch of cases. It requires that your OS user matches your db user, which is probably not the case. That's why `postgres` user often works without asking - during install, both OS user and db user are created.

The obvious method to switch to is password, and we must guarantee a secure connection to not leak the password. We shouldn't care about the password in the first place, there should be no possibility of a connection to the db that we don't already know is OK. So we could just use trust. In either case we need to actually change the auth method.

`pg_hba.conf` is the file we're looking for. Find it with `sudo su postgres -c 'psql -c "SHOW hba_file"'`.

Insert an entry to `pg_hba.conf`:
`local database_name database_user_name trust`
If there's a line like
`local all all peer`
then make sure the new line is above it so it takes effect first.

Update live config:
`sudo su postgres -c 'psql -c "SELECT pg_reload_conf()"'`.

Check on it:
`sudo su postgres -c 'psql -c "select * from pg_hba_file_rules"'`

Other example `pg_hba.conf` lines:
```
host database user 1.2.3.4/32 md5  # allow users with specific IP to log in via password
```
