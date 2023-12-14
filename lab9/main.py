import customtkinter as ctk
from src.smtp import send_email


app = ctk.CTk()


def send():
    recipient = recipient_field.get()
    subject = subject_field.get()
    body = body_field.get("1.0", "end")
    send_email(recipient, subject, body)


recipient_field = ctk.CTkEntry(
    app,
    placeholder_text="Recipient",
    font=("Arial", 20),
    width=400
)
subject_field = ctk.CTkEntry(
    app,
    placeholder_text="Subject",
    font=("Arial", 20),
    width=400
)
body_field = ctk.CTkTextbox(
    app,
    width=400,
    height=400
)
send_button = ctk.CTkButton(
    app,
    text="Send",
    font=("Arial", 20),
    command=send
)


def app_exit():
    app.quit()
    app.after(100, app.destroy)


def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app.title("SMTP Mailer")
    app.protocol("WM_DELETE_WINDOW", app_exit)
    app.resizable(False, False)
    app.geometry("400x600")

    recipient_field.pack(padx=10, pady=10)

    subject_field.pack(padx=10, pady=10)

    body_field.pack(padx=10, pady=10)

    send_button.pack(padx=10, pady=10)

    app.mainloop()


if __name__ == "__main__":
    main()
