use getaddrs::InterfaceAddrs;

fn main() {
    let addrs = InterfaceAddrs::query_system()
        .expect("System has no network interfaces.");

    for addr in addrs {
        println!("{}: {:#?}", addr.name, addr);
    }
}
