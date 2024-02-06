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
