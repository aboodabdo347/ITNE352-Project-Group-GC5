import socket, json

HOST = "127.0.0.1" # Localhost Server IP
PORT = 12345 # Server Port
BUFFER_SIZE = 4096 # Buffer size for receiving data

# Send a request to the server
def send_request(sock, action, params=None):
    if params is None:
        params = {}
    message = json.dumps({"action": action, "params": params}) + "\n"
    sock.sendall(message.encode())

# Receive a response from the server
def receive_response(sock):
    data = b""
    while b"\n" not in data:
        chunk = sock.recv(BUFFER_SIZE)
        if not chunk:
            return None
        data += chunk
    message, _ = data.split(b"\n", 1)
    return json.loads(message.decode())

# Display the main menu and get user choice
def show_main_menu():
    print("\n=== Main Menu ===")
    print("1. Search Headlines")
    print("2. List Sources")
    print("3. Quit")
    return input("Choose an option: ")

# Display the headlines menu and get user choice
def show_headlines_menu():
    print("\n--- Headlines Menu ---")
    print("1. Search by keyword")
    print("2. Search by category")
    print("3. Search by country")
    print("4. List all headlines")
    print("5. Back")
    return input("Choose an option: ")

# Display the sources menu and get user choice
def show_sources_menu():
    print("\n--- Sources Menu ---")
    print("1. Search by category")
    print("2. Search by country")
    print("3. Search by language")
    print("4. List all sources")
    print("5. Back")
    return input("Choose an option: ")

# Display a list of items
def display_list(items):
    for item in items:
        text = item.get("title") or item.get("name", "N/A")
        print(f"{item['index']}. {text}")

# Show detailed information for a selected item
def show_detail(sock, action):
    idx = input("Select index for details (Enter to skip): ").strip()
    if idx:
        send_request(sock, action, {"index": idx})
        detail = receive_response(sock)

        if detail and detail.get("status") == "ok":
            print(json.dumps(detail["detail"], indent=4))
        else:
            print("Error:", detail.get("message", "Unknown error"))

# Main function logic
def main():
    username = input("Enter your name: ")
    # Create tcp socket and connect to server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall((username + "\n").encode()) # Send username to server

        while True:
            choice = show_main_menu()
            # HEADLINES MENU
            if choice == "1":
                while True:
                    h_choice = show_headlines_menu()

                    if h_choice == "1":
                        q = input("Keyword: ")
                        send_request(sock, "headlines_keyword", {"q": q})

                    elif h_choice == "2":
                        cat = input("Category: {business, general, health, science, sports, technology}\n")
                        send_request(sock, "headlines_category", {"category": cat})

                    elif h_choice == "3":
                        c = input("Country code: {au, ca, jp, ae, sa, kr, us, ma}\n")
                        send_request(sock, "headlines_country", {"country": c})

                    elif h_choice == "4":
                        send_request(sock, "headlines_all")

                    elif h_choice == "5":
                        break

                    else:
                        print("Invalid option")
                        continue

                    response = receive_response(sock)
                    if response["status"] != "ok":
                        print("Error:", response["message"])
                        continue

                    display_list(response["items"])
                    show_detail(sock, "headlines_detail")
            # SOURCES MENU
            elif choice == "2":
                while True:
                    s_choice = show_sources_menu()

                    if s_choice == "1":
                        cat = input("Category: {business, general, health, science, sports, technology}\n")
                        send_request(sock, "sources_category", {"category": cat})

                    elif s_choice == "2":
                        c = input("Country code: {au, ca, jp, ae, sa, kr, us, ma}\n")
                        send_request(sock, "sources_country", {"country": c})

                    elif s_choice == "3":
                        lang = input("Language: {ar, en} \n")
                        send_request(sock, "sources_language", {"language": lang})

                    elif s_choice == "4":
                        send_request(sock, "sources_all")

                    elif s_choice == "5":
                        break

                    else:
                        print("Invalid option")
                        continue

                    response = receive_response(sock)
                    if response["status"] != "ok":
                        print("Error:", response["message"])
                        continue

                    display_list(response["items"])
                    show_detail(sock, "sources_detail")

            elif choice == "3":
                send_request(sock, "quit")
                print("Disconnected.")
                break

            else:
                print("Invalid option")


if __name__ == "__main__":
    main()
