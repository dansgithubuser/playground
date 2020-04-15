use tonic::{transport::Server, Request, Response, Status};

use hello::world_server::{World, WorldServer};
use hello::{HelloRep, HelloReq};

pub mod hello {
    tonic::include_proto!("hello");
}

#[derive(Debug, Default)]
pub struct WorldConcrete {}

#[tonic::async_trait]
impl World for WorldConcrete {
    async fn hello(&self, request: Request<HelloReq>) -> Result<Response<HelloRep>, Status> {
        println!("WorldConcrete {:?}", request);
        let request = request.into_inner();
        Ok(Response::new(HelloRep {
            message: format!("Hello {}!", request.name),
        }))
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    Server::builder()
        .add_service(WorldServer::new(WorldConcrete::default()))
        .serve("[::1]:8000".parse()?)
        .await?;
    Ok(())
}
