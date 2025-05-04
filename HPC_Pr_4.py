import socket
import threading

TERMINATE = "exit"
MAX_LEN = 1000
finished = threading.Event()

def listen(sock, name):
    while not finished.is_set():
        try:
            msg, _ = sock.recvfrom(MAX_LEN)
            msg = msg.decode()
            if not msg.startswith(name):
                print(msg)
        except OSError:
            break  # Socket closed
        except Exception as e:
            print(f"Listener error: {e}")
            break

def main():
    group = input("Multicast IP (e.g., 230.0.0.0): ")
    port = int(input("Port (e.g., 4446): "))
    name = input("Your name: ")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', port))

    mreq = socket.inet_aton(group) + socket.inet_aton('0.0.0.0')
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    listener_thread = threading.Thread(target=listen, args=(sock, name), daemon=True)
    listener_thread.start()

    print("Type messages (type 'exit' to quit):")
    try:
        while True:
            msg = input()
            if msg.lower() == TERMINATE:
                finished.set()
                sock.sendto(f"{name} has left the chat.".encode(), (group, port))
                break
            sock.sendto(f"{name}: {msg}".encode(), (group, port))
    finally:
        sock.close()

if _name_ == "_main_":
    main()