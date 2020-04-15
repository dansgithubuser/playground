use hello::{world_client::WorldClient, HelloReq};

pub mod hello {
    tonic::include_proto!("hello");
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut client = WorldClient::connect("http://[::1]:8000").await?;
    println!(
        "WorldClient {:?}",
        client
            .hello(tonic::Request::new(HelloReq {
                name: "Clarence".into(),
            }))
            .await?,
    );
    Ok(())
}
