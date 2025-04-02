import tkinter as tk

class ThermometerDisplay:
    def __init__(self, root):
        self.root = root
        self.root.title("🌡️ Indoor Thermometer Display")
        self.root.configure(bg="#e9f0f4")
        self.temp = 20

        tk.Label(root, text="Indoor Temperature Thermometer",
                 font=("Segoe UI", 18, "bold"), bg="#e9f0f4", fg="#2c3e50").pack(pady=15)

        entry_frame = tk.Frame(root, bg="#e9f0f4")
        entry_frame.pack()

        self.entry = tk.Entry(entry_frame, font=("Segoe UI", 13), width=8, justify="center")
        self.entry.insert(0, str(self.temp))
        self.entry.pack(side="left", padx=5)
        self.entry.bind("<Return>", lambda event: self.update_display())  # Press Enter to update

        self.button = tk.Button(entry_frame, text="Update", font=("Segoe UI", 12, "bold"),
                                bg="#27ae60", fg="white", activebackground="#2ecc71",
                                relief="flat", padx=10, pady=2, command=self.update_display)
        self.button.pack(side="left", padx=5)

        tk.Label(root,
                 text="Unit: °C     |     Low: 0°C     |     Normal Range: 20–25°C     |     High: 40°C",
                 font=("Segoe UI", 10, "italic"), bg="#e9f0f4", fg="#34495e").pack(pady=10)

        self.canvas = tk.Canvas(root, width=220, height=400, bg="#ffffff",
                                bd=0, highlightthickness=1, highlightbackground="#ccc")
        self.canvas.pack(pady=10)

        self.temp_label = tk.Label(root, text=f"{self.temp:.1f}°C", font=("Segoe UI", 16, "bold"),
                                   bg="#e9f0f4", fg="#2c3e50")
        self.temp_label.pack()

        self.status_label = tk.Label(root, text="", font=("Segoe UI", 12, "bold"),
                                     bg="#e9f0f4")
        self.status_label.pack(pady=5)

        self.draw_thermometer()
        self.update_status()

    def draw_thermometer(self):
        self.canvas.delete("all")
        max_temp = 40

        self.canvas.create_oval(80, 340, 140, 400, fill="#bdc3c7", outline="#bdc3c7")
        self.canvas.create_rectangle(100, 50, 120, 350, fill="#ecf0f1", outline="#bdc3c7", width=2)

        filled_height = (self.temp / max_temp) * 300 if self.temp > 0 else 0
        top = 350 - filled_height
        color = self.get_color(self.temp)

        if self.temp > 0:
            self.canvas.create_rectangle(100, top, 120, 350, fill=color, outline=color)

        self.canvas.create_oval(80, 340, 140, 400, fill=color, outline=color)

        for i in range(0, 41, 5):
            y = 350 - (i / 40) * 300
            self.canvas.create_line(125, y, 135, y, fill="#7f8c8d")
            self.canvas.create_text(140, y, text=f"{i}°", font=("Segoe UI", 8), anchor="w", fill="#2c3e50")

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
            self.status_label.config(text="Status: LOW", fg="#3498db")
        elif 20 <= self.temp <= 25:
            self.status_label.config(text="Status: NORMAL", fg="#27ae60")
        else:
            self.status_label.config(text="Status: HIGH", fg="#e74c3c")

    def update_display(self):
        try:
            value = float(self.entry.get())

            if value < 0:
                target_temp = 0
                message = "Clamped to 0°C (minimum)"
                color = "#3498db"
            elif value > 40:
                target_temp = 40
                message = "Clamped to 40°C (maximum)"
                color = "#e74c3c"
            else:
                target_temp = round(value, 1)
                message = ""
                color = ""

            step = 0.2 if self.temp < target_temp else -0.2

            def animate():
                nonlocal step
                if (step > 0 and self.temp < target_temp) or (step < 0 and self.temp > target_temp):
                    self.temp += step
                    self.temp_label.config(text=f"{self.temp:.1f}°C")
                    self.draw_thermometer()
                    self.update_status()
                    self.root.after(10, animate)
                else:
                    self.temp = target_temp
                    self.temp_label.config(text=f"{self.temp:.1f}°C")
                    self.draw_thermometer()
                    self.update_status()
                    if message:
                        self.status_label.config(text=message, fg=color)

            animate()

            # Reset entry
            self.entry.delete(0, tk.END)
            self.entry.insert(0, str(target_temp))

        except ValueError:
            self.status_label.config(text="Enter a valid number", fg="red")


if __name__ == "__main__":
    root = tk.Tk()
    app = ThermometerDisplay(root)
    root.geometry("300x600")
    root.mainloop()
