import socket
import customtkinter as ctk
from PIL import Image

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

USER = "edgarvlz"
PASSWORD = "12345"
HOST = "localhost"
PORT = 5004
KEY = 14


class ChatRoomsApp(ctk.CTk):

    def __init__(self, s):
        ctk.CTk.__init__(self)

        self.geometry("1100x600")
        self.title("PimenTalk")
        self.iconbitmap("bitmap.ico")
        self.toplevel_window = None
        self.s = s

        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure((0, 10), weight=1)
        container.grid_columnconfigure((0, 10), weight=1)

        self.frames = {}
        for F in (SignupPage, LoginPage, LobbyPage):
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

    def login(self, page_name, username, password):
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
            frame = self.frames[page_name]
            frame.tkraise()
        elif auth_code == "ERROR":
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((HOST, PORT))
            self.open_toplevel_login()

    def signup(self, page_name, username, password):
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
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.connect((HOST, PORT))
                self.open_toplevel_success()
                frame = self.frames[page_name]
                frame.tkraise()
            elif auth_code == "ERROR":
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.connect((HOST, PORT))
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
                                       command=lambda: controller.login("LobbyPage",
                                                                        login_username_entry.get(),
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
        ctk.CTkLabel(self, text="Wrong password or username.", font=("Montserrat", 15, "bold")).grid(column=1, row=0,
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
        ctk.CTkLabel(self, text="User created successfully!", font=("Montserrat", 15, "bold")).grid(column=1, row=0,
                                                                                                    columnspan=2,
                                                                                                    pady=10)
        ctk.CTkButton(self, width=150, height=40, text="Accept",
                      font=("Montserrat", 18, "bold"), text_color="White",
                      fg_color="#4a4743",
                      hover_color="#595550", command=self.destroy).grid(column=1, row=1)


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
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"[+] Connected to server on {HOST}:{PORT}")
        CRA = ChatRoomsApp(s)
        CRA.mainloop()


if __name__ == '__main__':
    main()
