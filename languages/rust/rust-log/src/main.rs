mod inner;

fn main() {
    env_logger::init();
    log::info!("main");
    inner::f();
    inner::center::f();
}
