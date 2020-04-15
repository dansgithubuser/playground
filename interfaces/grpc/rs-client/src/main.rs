pub mod zoo {
    tonic::include_proto!("zoo");
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("client monkey connecting");
    let mut client = zoo::monkey_client::MonkeyClient::connect("http://[::1]:8000").await?;
    println!("client monkey hello");
    println!(
        "client monkey {:?}",
        client
            .hello(tonic::Request::new(zoo::Name {
                first: "Clarence".into(),
                last: "Clearwater".into(),
            }))
            .await?,
    );
    println!("client bird connecting");
    let mut client = zoo::bird_client::BirdClient::connect("http://[::1]:8000").await?;
    println!("client bird listen");
    let mut stream = client
        .listen(tonic::Request::new(zoo::None {}))
        .await?
        .into_inner();
    println!("client bird streaming");
    for _ in 0..5 {
        println!("client bird {:?}", stream.message().await?);
    }
    Ok(())
}
