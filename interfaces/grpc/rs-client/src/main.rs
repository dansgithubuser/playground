pub mod zoo {
    tonic::include_proto!("zoo");
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("client connecting");
    let mut client = zoo::monkey_client::MonkeyClient::connect("http://[::1]:8000").await?;
    println!("client requesting");
    println!(
        "client {:?}",
        client
            .hello(tonic::Request::new(zoo::Name {
                first: "Clarence".into(),
                last: "Clearwater".into(),
            }))
            .await?,
    );
    Ok(())
}
