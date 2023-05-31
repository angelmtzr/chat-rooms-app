import socket
import customtkinter as ctk
from PIL import Image
from functools import partial

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

KEY = 13

current_user = ""
flag_login = False


def server_connection(host: str, port: int) -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    sock.connect_ex((host, port))
    check_server_str = caesar_cipher("check_server", KEY)
    sock.send(check_server_str.encode())
    reply = sock.recv(1024).decode()

    if reply == "":
        return False
    else:
        return True


def reachable_server():
    servers = [("127.0.0.1", 5004),
               ("127.0.0.1", 5001)]
    no_Server = ("0.0.0.0", 0)
    for i in range(len(servers)):
        r = server_connection(servers[i][0], servers[i][1])
        if r:
            return servers[i]
    return no_Server


class ChatRoomsApp(ctk.CTk):

    def __init__(self):
        ctk.CTk.__init__(self)

        self.s = ""
        self.geometry("650x600")
        self.title("PimenTalk - Login")
        self.iconbitmap("bitmap.ico")
        self.toplevel_window = None

        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure((0, 10), weight=1)
        container.grid_columnconfigure((0, 10), weight=1)

        self.frames = {}
        for F in (SignupPage, LoginPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

        self.show_frame("SignupPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def open_toplevel_login(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindowLogin()  # create window if its None or destroyed
            self.toplevel_window.focus()
        else:
            self.toplevel_window.focus()

    def open_toplevel_signup(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindowSignup()  # create window if its None or destroyed
            self.toplevel_window.focus()
        else:
            self.toplevel_window.focus()

    def open_toplevel_success(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindowSuccess()  # create window if its None or destroyed
            self.toplevel_window.focus()
        else:
            self.toplevel_window.focus()

    def login(self, username, password):
        server_available = reachable_server()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((server_available[0], server_available[1]))
        print(f"[+] Connected to server on {server_available[0]}:{server_available[1]}")
        req = f"auth {username} {password}"
        print(f"[+] Client request (decrypted): {req}")
        req = caesar_cipher(req, KEY)
        self.s.send(req.encode())
        print(f"[+] Request sent to server (encrypted): {req}")
        res = self.s.recv(1024).decode()
        print(f"[+] Response from server (encrypted): {res}")
        res = caesar_decipher(res, KEY)
        print(f"[+] Server response (decrypted): {res}")
        auth_code = res.split(" ")[0]
        if auth_code == "SUCCESS":
            global flag_login
            flag_login = True
            global current_user
            current_user = f"{username}"
            self.destroy()
        elif auth_code == "ERROR":
            self.open_toplevel_login()

    def signup(self, page_name, username, password):
        server_available = reachable_server()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((server_available[0], server_available[1]))
        print(f"[+] Connected to server on {server_available[0]}:{server_available[1]}")
        if len(username) > 7 and len(password) > 7:
            req = f"new_user {username} {password}"
            print(f"[+] Client request (decrypted): {req}")
            req = caesar_cipher(req, KEY)
            self.s.send(req.encode())
            print(f"[+] Request sent to server (encrypted): {req}")
            res = self.s.recv(1024).decode()
            print(f"[+] Response from server (encrypted): {res}")
            res = caesar_decipher(res, KEY)
            print(f"[+] Server response (decrypted): {res}")
            auth_code = res.split(" ")[0]
            if auth_code == "SUCCESS":
                self.open_toplevel_success()
                self.show_frame(page_name)
            elif auth_code == "ERROR":
                self.open_toplevel_signup()
        else:
            self.open_toplevel_signup()


class SignupPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        self.grid(row=4, column=5, rowspan=4, sticky="nsew")
        ctk.CTkLabel(self, text="CREATE ACCOUNT", font=("Montserrat", 28, "bold")).pack(pady=40)

        ctk.CTkLabel(self, text="Username", font=("Montserrat", 18)).pack(anchor="w", padx=40)

        signup_username_entry = ctk.CTkEntry(self, width=380, height=50, placeholder_text="Username",
                                             placeholder_text_color=("Grey", "Grey"))
        signup_username_entry.pack(pady=10, padx=40)

        ctk.CTkLabel(self, text="Password", font=("Montserrat", 18)).pack(anchor="w", padx=40)

        signup_password_entry = ctk.CTkEntry(self, width=380, height=50, placeholder_text="Password",
                                             show="*",
                                             placeholder_text_color=("Grey", "Grey"))
        signup_password_entry.pack(pady=10, padx=40)

        signup_button_s = ctk.CTkButton(self, width=380, height=50, text="Create Account",
                                        font=("Montserrat", 18, "bold"), text_color="black",
                                        fg_color="#fca521", hover_color="#e38c09",
                                        command=lambda: controller.signup("LoginPage",
                                                                          signup_username_entry.get(),
                                                                          signup_password_entry.get()))
        signup_button_s.pack(pady=10)

        login_button_s = ctk.CTkButton(self, width=380, height=50, text="Login",
                                       font=("Montserrat", 18, "bold"), text_color="White",
                                       fg_color="#4a4743", hover_color="#595550",
                                       command=lambda: controller.show_frame("LoginPage"))
        login_button_s.pack(pady=10)


class LoginPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.grid(row=4, column=5, rowspan=4, sticky="nsew")

        ctk.CTkLabel(self, text="LOGIN", font=("Montserrat", 28, "bold")).pack(pady=40)

        ctk.CTkLabel(self, text="Username", font=("Montserrat", 18)).pack(anchor="w", padx=40)

        login_username_entry = ctk.CTkEntry(self, width=380, height=50, placeholder_text="Username",
                                            placeholder_text_color=("Grey", "Grey"))
        login_username_entry.pack(pady=10, padx=40)

        ctk.CTkLabel(self, text="Password", font=("Montserrat", 18)).pack(anchor="w", padx=40)

        login_password_entry = ctk.CTkEntry(self, width=380, height=50, placeholder_text="Password",
                                            show="*",
                                            placeholder_text_color=("Grey", "Grey"))
        login_password_entry.pack(pady=10, padx=40)

        login_button_l = ctk.CTkButton(self, width=380, height=50, text="Login",
                                       font=("Montserrat", 18, "bold"), text_color="Black",
                                       fg_color="#fca521", hover_color="#e38c09",
                                       command=lambda: controller.login(login_username_entry.get(),
                                                                        login_password_entry.get()))
        login_button_l.pack(pady=10, padx=40)

        signup_button_l = ctk.CTkButton(self, width=380, height=50, text="Create Account",
                                        font=("Montserrat", 18, "bold"), text_color="White",
                                        fg_color="#4a4743",
                                        hover_color="#595550", command=lambda: controller.show_frame("SignupPage"))
        signup_button_l.pack(pady=10, padx=40)
        ctk.CTkLabel(self, text=" ", font=("Montserrat", 18)).pack(pady=5)


class LobbyPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        self.grid(row=4, column=5, rowspan=4, sticky="nsew")
        ctk.CTkLabel(self, text="LOBBY", font=("Montserrat", 28, "bold")).pack(pady=40)


class ToplevelWindowLogin(ctk.CTkToplevel):
    def __init__(self):
        ctk.CTkToplevel.__init__(self)
        self.geometry("350x150")
        self.title("Notification")
        self.after(250, lambda: self.iconbitmap("error_bitmap.ico"))
        self.grid_rowconfigure((0, 2), weight=1)
        self.grid_columnconfigure((0, 3), weight=1)

        error_image = ctk.CTkImage(light_image=Image.open("error_icon.png"),
                                   dark_image=Image.open("error_icon.png"),
                                   size=(30, 30))
        ctk.CTkLabel(self, image=error_image, text="").grid(column=0, row=0, pady=10, padx=5)
        ctk.CTkLabel(self, text="Wrong username or password.", font=("Montserrat", 15, "bold")).grid(column=1, row=0,
                                                                                                     columnspan=2,
                                                                                                     pady=10)
        ctk.CTkButton(self, width=150, height=40, text="Accept",
                      font=("Montserrat", 18, "bold"), text_color="White",
                      fg_color="#4a4743",
                      hover_color="#595550", command=self.destroy).grid(column=1, row=1)


class ToplevelWindowSignup(ctk.CTkToplevel):
    def __init__(self):
        ctk.CTkToplevel.__init__(self)
        self.geometry("450x200")
        self.title("Notification")
        self.after(250, lambda: self.iconbitmap("error_bitmap.ico"))
        self.grid_rowconfigure(0, weight=3)
        self.grid_rowconfigure((1, 5), weight=1)
        self.grid_columnconfigure((0, 3), weight=1)

        error_image = ctk.CTkImage(light_image=Image.open("error_icon.png"),
                                   dark_image=Image.open("error_icon.png"),
                                   size=(50, 50))
        ctk.CTkLabel(self, image=error_image, text="").grid(column=0, row=0, rowspan=2, padx=10)
        ctk.CTkLabel(self, text="Error creating account:\n", font=("Montserrat", 22, "bold")).grid(column=1, row=0,
                                                                                                   columnspan=2,
                                                                                                   rowspan=2)

        ctk.CTkLabel(self, text="-Minimum length of 8 characters",
                     font=("Montserrat", 15)).grid(column=1, row=1, columnspan=2, sticky=ctk.W, padx=30)
        ctk.CTkLabel(self, text="-Do not leave blank spaces",
                     font=("Montserrat", 15)).grid(column=1, row=2, columnspan=2, sticky=ctk.W, padx=30)
        ctk.CTkButton(self, width=155, height=40, text="Accept",
                      font=("Montserrat", 18, "bold"), text_color="White",
                      fg_color="#4a4743",
                      hover_color="#595550", command=self.destroy).grid(column=1, row=5, pady=15)


class ToplevelWindowSuccess(ctk.CTkToplevel):
    def __init__(self):
        ctk.CTkToplevel.__init__(self)
        self.geometry("350x150")
        self.title("Notification")
        self.after(250, lambda: self.iconbitmap("success_icon.ico"))
        self.grid_rowconfigure((0, 2), weight=1)
        self.grid_columnconfigure((0, 3), weight=1)

        error_image = ctk.CTkImage(light_image=Image.open("success_icon.png"),
                                   dark_image=Image.open("success_icon.png"),
                                   size=(30, 30))
        ctk.CTkLabel(self, image=error_image, text="").grid(column=0, row=0, pady=10, padx=5)
        ctk.CTkLabel(self, text="Created successfully!", font=("Montserrat", 15, "bold")).grid(column=1, row=0,
                                                                                               columnspan=2,
                                                                                               pady=10)
        ctk.CTkButton(self, width=150, height=40, text="Accept",
                      font=("Montserrat", 18, "bold"), text_color="White",
                      fg_color="#4a4743",
                      hover_color="#595550", command=self.destroy).grid(column=1, row=1)


def open_toplevel_chat(group_name):
    print(group_name)
    ToplevelWindowChat(group_name).focus()  # create window if its None or destroyed


class Lobby(ctk.CTk):
    def __init__(self, username):
        ctk.CTk.__init__(self)

        self.s = ""
        self.geometry("750x600")
        self.title("PimenTalk - Lobby")
        self.iconbitmap("bitmap.ico")
        self.toplevel_window = None
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)
        self.scrollable_frame1_buttons = []
        self.scrollable_frame2_buttons = []

        user_greeting = f"Hello {username}, welcome to PimenTalk!"
        self.greeting = ctk.CTkLabel(self, text=user_greeting, font=("Montserrat", 18, "bold")).grid(row=0,
                                                                                                     column=0,
                                                                                                     columnspan=5,
                                                                                                     pady=15)
        self.group_name_entry = ctk.CTkEntry(self, width=100, height=40, placeholder_text="Group name",
                                             placeholder_text_color=("Grey", "Grey"))
        self.group_name_entry.grid(row=0, column=6, pady=15)
        self.create_group_button = ctk.CTkButton(self, width=120, height=40, text="Create Group",
                                                 font=("Montserrat", 15, "bold"), text_color="black",
                                                 fg_color="#fca521", hover_color="#e38c09",
                                                 command=lambda: self.create_group(username, self.group_name_entry.get()
                                                                                   ))
        self.create_group_button.grid(row=0, column=7, columnspan=2)
        self.refresh_button = ctk.CTkButton(self, width=70, height=40, text="Refresh",
                                            font=("Montserrat", 15, "bold"), text_color="black",
                                            fg_color="#fca521", hover_color="#e38c09",
                                            command=lambda: self.refresh(username))
        self.refresh_button.grid(row=0, column=9, pady=15)
        self.frame = ctk.CTkFrame(self, width=100, corner_radius=0)
        self.frame.grid(row=1, column=0, rowspan=10, columnspan=11, sticky="nsew")
        self.frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.frame.grid_rowconfigure((0, 1, 2), weight=1)

        self.scrollable_frame1 = ctk.CTkScrollableFrame(self.frame, label_text="My Groups",
                                                        label_font=("Montserrat", 16, "bold"), height=425, width=200)
        self.scrollable_frame1.grid(row=0, column=0, rowspan=3)
        self.scrollable_frame1.grid_columnconfigure(0, weight=1)

        self.scrollable_frame2 = ctk.CTkScrollableFrame(self.frame, label_text="Other Groups",
                                                        label_font=("Montserrat", 16, "bold"), height=425, width=200)

        self.scrollable_frame2.grid(row=0, column=1, rowspan=3)
        self.scrollable_frame2.grid_columnconfigure(0, weight=1)
        self.scrollable_frame3 = ctk.CTkScrollableFrame(self.frame, label_text="Requests",
                                                        label_font=("Montserrat", 16, "bold"), height=425, width=200)
        self.scrollable_frame3.grid(row=0, column=2, rowspan=3)
        self.scrollable_frame3.grid_columnconfigure(0, weight=1)
        self.get_groups(username)
        self.get_other_groups(username)

    def create_group(self, username, group_name):
        server_available = reachable_server()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((server_available[0], server_available[1]))
        print(f"[+] Connected to server on {server_available[0]}:{server_available[1]}")
        req = f"new_group {group_name} {username}"
        print(f"[+] Client request (decrypted): {req}")
        req = caesar_cipher(req, KEY)
        self.s.send(req.encode())
        print(f"[+] Request sent to server (encrypted): {req}")
        res = self.s.recv(1024).decode()
        print(f"[+] Response from server (encrypted): {res}")
        res = caesar_decipher(res, KEY)
        print(f"[+] Server response (decrypted): {res}")
        auth_code = res.split(" ")[0]
        if auth_code == "SUCCESS":
            self.open_toplevel_success()
            self.refresh(username)

        elif auth_code == "ERROR":
            self.open_toplevel_group()

    def get_groups(self, username):
        server_available = reachable_server()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((server_available[0], server_available[1]))
        print(f"[+] Connected to server on {server_available[0]}:{server_available[1]}")
        req = f"get_user_groups {username}"
        print(f"[+] Client request (decrypted): {req}")
        req = caesar_cipher(req, KEY)
        self.s.send(req.encode())
        print(f"[+] Request sent to server (encrypted): {req}")
        res = self.s.recv(1024).decode()
        print(f"[+] Response from server (encrypted): {res}")
        res = caesar_decipher(res, KEY)
        print(f"[+] Server response (decrypted): {res}")
        user_groups = res.split(":")
        for group in user_groups:
            if group:
                self.scrollable_frame1_buttons.append(group.split(" ")[0])
        for i, button in enumerate(self.scrollable_frame1_buttons):
            new_button = ctk.CTkButton(self.scrollable_frame1, text=f"{button}", fg_color="#4a4747",
                                       hover_color="#595454", command=partial(open_toplevel_chat, button))
            new_button.grid(row=i, column=0, padx=10, pady=(0, 20))

    def get_other_groups(self, username):
        server_available = reachable_server()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((server_available[0], server_available[1]))
        print(f"[+] Connected to server on {server_available[0]}:{server_available[1]}")
        req = f"get_other_groups {username}"
        print(f"[+] Client request (decrypted): {req}")
        req = caesar_cipher(req, KEY)
        self.s.send(req.encode())
        print(f"[+] Request sent to server (encrypted): {req}")
        res = self.s.recv(1024).decode()
        print(f"[+] Response from server (encrypted): {res}")
        res = caesar_decipher(res, KEY)
        print(f"[+] Server response (decrypted): {res}")
        user_groups = res.split(":")
        for group in user_groups:
            if group:
                self.scrollable_frame2_buttons.append(group.split(" ")[0])
        for i, button in enumerate(self.scrollable_frame2_buttons):
            new_button = ctk.CTkButton(self.scrollable_frame2, text=f"{button}", fg_color="#4a4747",
                                       hover_color="#595454")
            new_button.grid(row=i, column=0, padx=10, pady=(0, 20))

    def open_toplevel_group(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindowGroup()  # create window if its None or destroyed
            self.toplevel_window.focus()
        else:
            self.toplevel_window.focus()

    def open_toplevel_success(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindowSuccess()  # create window if its None or destroyed
            self.toplevel_window.focus()
        else:
            self.toplevel_window.focus()

    def refresh(self, username):
        self.scrollable_frame1_buttons = []
        self.scrollable_frame2_buttons = []

        self.get_groups(username)
        self.get_other_groups(username)


class ToplevelWindowGroup(ctk.CTkToplevel):
    def __init__(self):
        ctk.CTkToplevel.__init__(self)
        self.geometry("350x150")
        self.title("Notification")
        self.after(250, lambda: self.iconbitmap("error_bitmap.ico"))
        self.grid_rowconfigure((0, 2), weight=1)
        self.grid_columnconfigure((0, 3), weight=1)

        error_image = ctk.CTkImage(light_image=Image.open("error_icon.png"),
                                   dark_image=Image.open("error_icon.png"),
                                   size=(30, 30))
        ctk.CTkLabel(self, image=error_image, text="").grid(column=0, row=0, pady=10, padx=5)
        ctk.CTkLabel(self, text="Could not create group.", font=("Montserrat", 15, "bold")).grid(column=1, row=0,
                                                                                                 columnspan=2,
                                                                                                 pady=10)
        ctk.CTkButton(self, width=150, height=40, text="Accept",
                      font=("Montserrat", 18, "bold"), text_color="White",
                      fg_color="#4a4743",
                      hover_color="#595550", command=self.destroy).grid(column=1, row=1)


class ToplevelWindowChat(ctk.CTkToplevel):
    def __init__(self, group_name):
        ctk.CTkToplevel.__init__(self)
        chat_name = f"Chat - {group_name}"
        self.geometry("321x500")
        self.title(chat_name)
        self.after(250, lambda: self.iconbitmap("bitmap.ico"))
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)

        self.chat_frame = ctk.CTkFrame(self, width=100, corner_radius=0)
        self.chat_frame.grid(row=0, column=0, rowspan=9, columnspan=3, sticky="nsew")
        self.chat_entry = ctk.CTkEntry(self, width=200, height=35, placeholder_text="Write your message...",
                                       placeholder_text_color=("Grey", "Grey"))
        self.chat_entry.grid(row=9, column=0, columnspan=2)
        self.send_button = ctk.CTkButton(self, width=70, height=35, text="Send",
                                         font=("Montserrat", 15, "bold"), text_color="black",
                                         fg_color="#fca521", hover_color="#e38c09",
                                         )
        self.send_button.grid(row=9, column=2, sticky="w")


def caesar_cipher(plaintext, shift):
    ciphertext = ""
    for char in plaintext:
        if char.isupper():
            ciphertext += chr((ord(char) + shift - 65) % 26 + 65)
        elif char.islower():
            ciphertext += chr((ord(char) + shift - 97) % 26 + 97)
        else:
            ciphertext += char
    return ciphertext


def caesar_decipher(ciphertext, shift):
    plaintext = ""
    for char in ciphertext:
        if char.isupper():
            plaintext += chr((ord(char) - shift - 65) % 26 + 65)
        elif char.islower():
            plaintext += chr((ord(char) - shift - 97) % 26 + 97)
        else:
            plaintext += char
    return plaintext


def main():
    CRA = ChatRoomsApp()
    CRA.mainloop()
    if flag_login:
        CRL = Lobby(current_user)
        CRL.mainloop()


if __name__ == '__main__':
    main()
