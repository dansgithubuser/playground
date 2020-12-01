fn main() {
    let args: Vec<_> = std::env::args().collect();
    let name = &args[1];
    println!("{}: started", name);
    let conn = rusqlite::Connection::open_with_flags(
        "lol.sql",
        rusqlite::OpenFlags::SQLITE_OPEN_READ_WRITE | rusqlite::OpenFlags::SQLITE_OPEN_CREATE,
    )
    .unwrap();
    conn.busy_timeout(std::time::Duration::from_secs_f32(3.0)).unwrap();
    conn.execute_batch(
        "CREATE TABLE IF NOT EXISTS vars (
            name TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            metadata TEXT
        )",
    )
    .expect("common DB schema execution failed");
    println!("{}: opened connection", name);
    for i in 0..1000 {
        conn.execute_batch(&format!("INSERT OR IGNORE INTO vars VALUES ('{}', '{}', NULL)", i, i))
            .unwrap();
        conn.query_row::<String, _, _>(
            &format!("SELECT * FROM vars WHERE name = '{}'", i),
            rusqlite::NO_PARAMS,
            |row| row.get(0),
        )
        .unwrap();
        conn.execute_batch(&format!(
            "INSERT OR REPLACE INTO vars VALUES ('{}', '{}', NULL)",
            i,
            i * 2
        ))
        .unwrap();
        if i % 100 == 0 {
            println!("{}: i = {}", name, i);
        }
    }
}
