use tokio::sync::mpsc::{channel, Receiver};
use tonic::{transport::Server, Request, Response, Status};

pub mod zoo {
    tonic::include_proto!("zoo");
}

#[derive(Debug, Default)]
pub struct Monkey {}

#[tonic::async_trait]
impl zoo::monkey_server::Monkey for Monkey {
    async fn hello(&self, req: Request<zoo::Name>) -> Result<Response<zoo::Msg>, Status> {
        println!("server monkey {:?}", req);
        let name = req.into_inner();
        Ok(Response::new(zoo::Msg {
            msg: format!("Ooh ooh ah {} ah!", name.first),
        }))
    }
}

#[derive(Debug, Default)]
pub struct Bird {}

#[tonic::async_trait]
impl zoo::bird_server::Bird for Bird {
    type ListenStream = Receiver<Result<zoo::Msg, Status>>;//this is necessary

    async fn listen(&self, req: Request<zoo::None>) -> Result<Response<Self::ListenStream>, Status> {
        println!("server bird {:?}", req);
        let (mut tx, rx) = channel(1);
        tokio::spawn(async move {
            let mut bird_brain = 0x1834;
            loop {
                println!("server bird sleeping");
                tokio::time::delay_for(std::time::Duration::from_secs(2)).await;
                println!("server bird awake");
                tx.send(Ok(zoo::Msg {
                    msg: match bird_brain % 4 {
                        0 => "IT IS RAINING",
                        1 => "THIS IS MY TREE",
                        2 => "WHERE THE PRETTY BIRDS AT",
                        3 => "THERE IS A BAD BIRD OR LAND LOVER",
                        _ => "SQUAWK",
                    }.into(),
                })).await.unwrap();
                bird_brain = (bird_brain >> 1) | if (bird_brain & 0x1) ^ (bird_brain & 0x40) != 0 {
                    0x8000
                } else {
                    0
                };
            }
        });
        Ok(Response::new(rx))
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("server starting");
    Server::builder()
        .add_service(zoo::monkey_server::MonkeyServer::new(Monkey::default()))
        .add_service(zoo::bird_server::BirdServer::new(Bird::default()))
        .serve("[::1]:8000".parse()?)
        .await?;
    Ok(())
}
