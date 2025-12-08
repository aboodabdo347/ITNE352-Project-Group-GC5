import socket, threading, json

HOST = "127.0.0.1"
PORT = 5000

def handle_client(conn, addr):
    username = conn.recv(1024).decode().strip()
    print("Client:", username, "from", addr)
    conn.sendall(b"Welcome! Type keyword or 'quit'\n")

    while True:
        data = conn.recv(1024)
        if not data:
            break
        keyword = data.decode().strip()
        if keyword.lower() == "quit":
            break

        # fake news just to test the connetion
        headlines = [
            {"title": f"{keyword} news 1"},
            {"title": f"{keyword} news 2"},
            {"title": f"{keyword} news 3"},
        ]

        # save it as json and send it to the client
        with open(f"{username}_demo.json", "w", encoding="utf-8") as f:
            json.dump(headlines, f, indent=2)

        conn.sendall((json.dumps(headlines) + "\n").encode())

    conn.close()
    print("Disconnected:", username)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Server listening on", HOST, PORT)
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
