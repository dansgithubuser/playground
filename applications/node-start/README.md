This readme will get more love as needed. For now here're some gotchas.

On getting deployed:
- use `--db-dry-sql` to get db creation commands to run in a `psql` session in db droplet
- make an `env` file in `env` folder, change the `DB_HOST` to `db`
