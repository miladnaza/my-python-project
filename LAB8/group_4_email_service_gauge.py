import tkinter as tk
import math
import smtplib
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ---------------- SMTP CONFIG (SendGrid) ----------------
SENDGRID_SMTP_SERVER = "smtp.sendgrid.net"
SMTP_PORT = 587
SMTP_USERNAME = "apikey"  # This must be the literal string "apikey"
SENDGRID_API_KEY =""
SENDER_EMAIL = "networkinggroupl3@gmail.com"
# ✅ List of recipients
RECEIVER_EMAILS = [
  #"mnovapac@my.centennialcollege.ca",
  "mnazari9@my.centennialcollege.ca",
  "ddiazpar@my.centennialcollege.ca"
 # "eemiowei@my.centennialcollege.ca"
]


def send_email_alert(value):
    subject = "🚨 Critical Temperature Alert"

    if value == "Invalid Input":
        body = "The temperature entered is invalid input. Please check the system."
    else:
        body = f"The user entered a temperature of {value}°C, which is dangerous outside the safe range is (0–40°C)."

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = ", ".join(RECEIVER_EMAILS)
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SENDGRID_SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SENDGRID_API_KEY)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAILS, msg.as_string())
        print("✅ Email sent successfully!")
    except Exception as e:
        print("❌ Failed to send email:", str(e))


# ---------------- GUI APP ----------------

class ModernGaugeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Indoor Temperature Gauge")
        self.root.configure(bg="#f2f6fc")
        self.temp = 20

        tk.Label(root, text="🌡️ Indoor Temperature Gauge",
                 font=("Segoe UI", 20, "bold"), bg="#f2f6fc", fg="#1f2d3d").pack(pady=15)

        entry_frame = tk.Frame(root, bg="#f2f6fc")
        entry_frame.pack()

        self.entry = tk.Entry(entry_frame, font=("Segoe UI", 14), width=8, justify="center",
                              bd=1, relief="solid")
        self.entry.insert(0, str(self.temp))
        self.entry.pack(side="left", padx=8, ipady=3)
        self.entry.bind("<Return>", lambda event: self.update_display())

        self.button = tk.Button(entry_frame, text="Update", font=("Segoe UI", 12, "bold"),
                                bg="#2ecc71", fg="white", activebackground="#27ae60",
                                relief="flat", padx=14, pady=6, command=self.update_display)
        self.button.pack(side="left", padx=8)

        tk.Label(root, text="Unit: °C     |     Low: 0°C     |     Normal: 20–25°C     |     High: 40°C",
                 font=("Calibri", 11, "italic"), bg="#f2f6fc", fg="#7f8c8d").pack(pady=5)

        self.canvas = tk.Canvas(root, width=360, height=360, bg="#ffffff",
                                bd=0, highlightthickness=0)
        self.canvas.pack(pady=15)

        self.status_label = tk.Label(root, text="", font=("Segoe UI", 13, "bold"), bg="#f2f6fc")
        self.status_label.pack(pady=8)

        self.draw_gauge()

    def draw_gauge(self):
        self.canvas.delete("all")
        cx, cy, radius = 180, 180, 130

        # Colored arc segments
        for i in range(0, 41):
            angle = 135 - (i / 40) * 270
            extent = 270 / 40
            color = self.get_color(i)
            self.canvas.create_arc(cx - radius, cy - radius, cx + radius, cy + radius,
                                   start=angle, extent=extent, style="arc",
                                   width=22, outline=color)

        # Inner hub
        self.canvas.create_oval(cx - 65, cy - 65, cx + 65, cy + 65,
                                fill="#f9fbfd", outline="#dfe6ec")

        # Needle
        angle = 135 - (self.temp / 40) * 270
        needle_len = 80
        x_end = cx + needle_len * math.cos(math.radians(angle))
        y_end = cy - needle_len * math.sin(math.radians(angle))
        self.canvas.create_line(cx, cy, x_end, y_end, width=4, fill=self.get_color(self.temp))
        self.canvas.create_oval(cx - 8, cy - 8, cx + 8, cy + 8,
                                fill=self.get_color(self.temp), outline="#2c3e50")

        # Value label
        self.canvas.create_text(cx, cy + 90, text=f"{self.temp:.1f}°C",
                                font=("Segoe UI", 18, "bold"), fill="#2c3e50")

        # Tick labels
        for i in range(0, 41, 10):
            tick_angle = 135 - (i / 40) * 270
            x = cx + 100 * math.cos(math.radians(tick_angle))
            y = cy - 100 * math.sin(math.radians(tick_angle))
            self.canvas.create_text(x, y, text=str(i), font=("Segoe UI", 9), fill="#34495e")

        self.update_status()

    def get_color(self, temp):
        if temp >= 35:
            return "#e74c3c"
        elif temp >= 25:
            return "#f39c12"
        elif temp >= 15:
            return "#2ecc71"
        else:
            return "#3498db"

    def update_status(self):
        if self.temp < 20:
            self.status_label.config(text="🧊 Status: LOW", fg="#3498db")
        elif 20 <= self.temp <= 25:
            self.status_label.config(text="✅ Status: NORMAL", fg="#2ecc71")
        else:
            self.status_label.config(text="🔥 Status: HIGH", fg="#e74c3c")

    def update_display(self):
        try:
            value = float(self.entry.get())
            clamped = False

            if value < 0 or value > 40:
                threading.Thread(target=send_email_alert, args=(value,)).start()

            if value < 0:
                target_temp = 0
                clamped = True
            elif value > 40:
                target_temp = 40
                clamped = True
            else:
                target_temp = round(value, 1)

            step = 0.2 if self.temp < target_temp else -0.2

            def animate():
                if abs(self.temp - target_temp) > 0.1:
                    self.temp += step
                    self.draw_gauge()
                    self.root.after(10, animate)
                else:
                    self.temp = target_temp
                    self.draw_gauge()
                    if clamped:
                        msg = f"Input too {'low' if self.temp == 0 else 'high'}. Adjusted to safe limit: {self.temp:.1f}°C"
                        self.status_label.config(text=msg, fg="#e67e22")
                    else:
                        self.update_status()

            animate()

        except ValueError:
            self.status_label.config(text="❌ Enter a valid number", fg="#c0392b")
            threading.Thread(target=send_email_alert, args=("Invalid Input",)).start()


# ---------------- RUN APP ------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ModernGaugeApp(root)
    root.geometry("420x580")
    root.mainloop()
