async fn f() -> Result<(), ()> {
    println!("hello, ");
    Ok(())
}

async fn g() -> Result<i32, ()> {
    println!("world!");
    Ok(0)
}

async fn h() -> Result<(), i32> {
    Err(13)
}

#[tokio::main]
pub async fn main() {
    tokio::try_join!(f(), g());
    //tokio::try_join!(f(), h()); // doesn't compile
}
