use tonic::{transport::Server, Request, Response, Status};

pub mod zoo {
    tonic::include_proto!("zoo");
}

#[derive(Debug, Default)]
pub struct Monkey {}

#[tonic::async_trait]
impl zoo::monkey_server::Monkey for Monkey {
    async fn hello(&self, req: Request<zoo::Name>) -> Result<Response<zoo::Msg>, Status> {
        println!("server {:?}", req);
        let name = req.into_inner();
        Ok(Response::new(zoo::Msg {
            msg: format!("Ooh ooh ah {} ah!", name.first),
        }))
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("server starting");
    Server::builder()
        .add_service(zoo::monkey_server::MonkeyServer::new(Monkey::default()))
        .serve("[::1]:8000".parse()?)
        .await?;
    Ok(())
}
