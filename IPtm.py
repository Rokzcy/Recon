#!/usr/bin/env python3
import socket
import sys
import argparse
import threading
import time

def ip_transmitter(target_host, target_port, local_port):
    """UDP IP packet forwarder/transmitter"""
    
    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        sock.bind(('0.0.0.0', local_port))
        print(f"[+] IP Transmitter started: UDP *:{local_port} -> {target_host}:{target_port}")
        print("[+] Waiting for incoming packets...")
        
        while True:
            try:
                data, addr = sock.recvfrom(65535)
                print(f"[+] Fwd {len(data)} bytes from {addr} -> {target_host}:{target_port}")
                
                # Forward exact packet data
                sock.sendto(data, (target_host, target_port))
                
            except KeyboardInterrupt:
                print("\n[!] Interrupted by user")
                break
            except Exception as e:
                print(f"[!] Recv error: {e}")
                time.sleep(0.1)
                
    except Exception as e:
        print(f"[!] Bind failed on port {local_port}: {e}")
        sys.exit(1)
    finally:
        sock.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UDP IP Packet Forwarder/Transmitter")
    parser.add_argument("target", help="Target IP:PORT (e.g. 192.168.1.100:12345)")
    parser.add_argument("local_port", type=int, help="Local UDP port to listen on")
    
    args = parser.parse_args()
    
    try:
        target_host, target_port = args.target.split(':')
        target_port = int(target_port)
    except:
        print("Error: target must be IP:PORT format")
        sys.exit(1)
    
    ip_transmitter(target_host, target_port, args.local_port)
