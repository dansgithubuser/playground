use std::thread;
use std::time::{Instant, Duration};

fn get_conn() -> Result<rusqlite::Connection, rusqlite::Error> {
    use rusqlite::OpenFlags;
    let conn = rusqlite::Connection::open_with_flags(
        "lol.sqlite",
        OpenFlags::SQLITE_OPEN_READ_WRITE
            | OpenFlags::SQLITE_OPEN_CREATE
            | OpenFlags::SQLITE_OPEN_FULL_MUTEX,
    )?;
    conn.busy_timeout(Duration::from_secs_f32(0.1)).unwrap();
    conn.execute_batch(
        "CREATE TABLE IF NOT EXISTS vars (
            name TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            metadata TEXT
        )",
    )?;
    Ok(conn)
}

fn main() {
    let args: Vec<_> = std::env::args().collect();
    let name = &args[1];
    println!("{}: started", name);
    for i in 0..100 {
        let start = Instant::now();
        let conn = match get_conn() {
            Ok(conn) => conn,
            Err(e) => {
                println!("error when getting conn: {}, t = {} s", e, (Instant::now() - start).as_secs_f32());
                thread::sleep(Duration::from_secs_f32(0.01));
                continue;
            }
        };
        if let Err(e) = (|| -> Result<(), rusqlite::Error> {
            match i % 3 {
                0 => conn.execute_batch(&format!("INSERT OR IGNORE INTO vars VALUES ('{}', '0', NULL)", i))?,
                1 => {
                    conn.execute_batch(&format!(
                        "
                        UPDATE vars
                        SET value = CAST(CAST(value AS INTEGER) + 1 AS TEXT)
                        WHERE name = '{}'
                        ",
                        i - 1
                    ))?;
                    thread::sleep(Duration::from_secs_f32(0.01));
                }
                2 => {
                    conn.query_row::<String, _, _>(
                        &format!("SELECT * FROM vars WHERE name = '{}'", i),
                        [],
                        |row| row.get(0),
                    )?;
                    thread::sleep(Duration::from_secs_f32(0.01));
                }
                _ => panic!("bad math"),
            }
            Ok(())
        })() {
            println!("error when querying: {}, t = {} s", e, (Instant::now() - start).as_secs_f32());
        };
        conn.close().unwrap();
        println!("{}: i = {}, t = {}", name, i, (Instant::now() - start).as_secs_f32());
    }
}
