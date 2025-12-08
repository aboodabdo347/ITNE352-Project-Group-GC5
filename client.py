import socket, json

HOST = "127.0.0.1"
PORT = 5000

def main():
    username = input("Enter your name: ")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall((username + "\n").encode())

        print(s.recv(1024).decode())  # welcome

        while True:
            keyword = input("Keyword (or 'quit'): ")
            s.sendall((keyword + "\n").encode())
            if keyword.lower() == "quit":
                break

            data = s.recv(4096).decode().strip()
            if not data:
                break

            try:
                headlines = json.loads(data)
            except json.JSONDecodeError:
                print("Bad response:", data)
                continue

            print("\nHeadlines:")
            for i, h in enumerate(headlines, start=1):
                print(f"{i}. {h['title']}")
            print()

if __name__ == "__main__":
    main()
