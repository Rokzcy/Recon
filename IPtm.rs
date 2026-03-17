use std::net::{UdpSocket, SocketAddr};
use std::env;
use std::str::FromStr;
use std::thread;
use std::time::Duration;

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() != 4 {
        eprintln!("Usage: {} <target_ip> <target_port> <local_port>", args[0]);
        eprintln!("Example: {} 192.168.1.100 12345 4444", args[0]);
        std::process::exit(1);
    }

    let target_ip = &args[1];
    let target_port: u16 = args[2].parse().expect("Invalid target port");
    let local_port: u16 = args[3].parse().expect("Invalid local port");

    let target_addr: SocketAddr = format!("{}:{}", target_ip, target_port).parse().expect("Invalid target address");
    
    // Create UDP socket bound to local port
    let socket = UdpSocket::bind(format!("0.0.0.0:{}", local_port))
        .expect("Failed to bind to local port");

    println!("IP Transmitter started on UDP {} -> {}", local_port, target_addr);
    println!("Waiting for incoming packets...");

    loop {
        let mut buf = [0u8; 65535];
        
        match socket.recv_from(&mut buf) {
            Ok((len, src_addr)) => {
                println!("Received {} bytes from {} - forwarding to {}", 
                         len, src_addr, target_addr);
                
                // Forward the exact packet data
                if let Err(e) = socket.send_to(&buf[..len], target_addr) {
                    eprintln!("Failed to forward packet: {}", e);
                }
            }
            Err(e) => {
                eprintln!("Recv error: {}", e);
                thread::sleep(Duration::from_millis(100));
            }
        }
    }
}
