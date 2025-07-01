import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from customtkinter import CTkImage
import threading
import speedtest

# Global variables
is_dark_mode = True
history = []

def toggle_dark_mode():
    global is_dark_mode
    is_dark_mode = not is_dark_mode
    mode = "dark" if is_dark_mode else "light"
    ctk.set_appearance_mode(mode)
    dark_mode_btn.configure(text="☀ Light Mode" if is_dark_mode else "🌙 Dark Mode")

def test_speed():
    def run_speed_test():
        try:
            result_textbox.configure(state="normal")
            result_textbox.delete("1.0", "end")
            result_textbox.insert("end", "🚀 Testing... Please wait.\n", "testing_tag")
            result_textbox.tag_config("testing_tag", foreground="#FFA500")  # Orange color
            result_textbox.configure(state="disabled")

            app.update_idletasks()

            st = speedtest.Speedtest()
            st.get_best_server()

            isp = st.results.client["isp"]
            server = st.get_best_server()
            server_location = f"{server['name']}, {server['country']}"
            download_speed = st.download() / 1_000_000
            upload_speed = st.upload() / 1_000_000
            ping = st.results.ping

            result_text = (
                f"🌐 ISP:              {isp}\n"
                f"📍 Server:         {server_location}\n"
                f"⬇  Download:  {download_speed:.2f} Mbps\n"
                f"⬆  Upload:       {upload_speed:.2f} Mbps\n"
                f"⚡ Ping:           {ping:.2f} ms"
            )

            result_textbox.configure(state="normal")
            result_textbox.delete("1.0", "end")
            result_textbox.insert("end", result_text)
            result_textbox.configure(state="disabled")

            history.append(result_text)
            if len(history) > 10:
                history.pop(0)

            history_textbox.configure(state="normal")
            history_textbox.delete("1.0", "end")
            history_textbox.insert("end", "\n\n".join(history))
            history_textbox.configure(state="disabled")

        except speedtest.ConfigRetrievalError:
            messagebox.showerror("Error", "Failed to retrieve Speedtest configuration. Check your internet connection.")
        except speedtest.NoMatchedServers:
            messagebox.showerror("Error", "No Speedtest servers available. Try again later.")
        except Exception as e:
            messagebox.showerror("Error", f"Speed test failed: {e}")

    threading.Thread(target=run_speed_test, daemon=True).start()


# Initialize customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Main Window
app = ctk.CTk()
app.title("Network Speed Test")
app.geometry("1200x780")
app.resizable(False, False)

# Glass Frame
glass_frame = ctk.CTkFrame(app, width=1000, height=700, corner_radius=15)
glass_frame.place(relx=0.5, rely=0.5, anchor="center")

# Speedometer Image
image = Image.open("image.png")
icon_image = CTkImage(dark_image=image, size=(150, 150))
icon_label = ctk.CTkLabel(glass_frame, image=icon_image, text="")
icon_label.pack(pady=10)

# Title
title_label = ctk.CTkLabel(glass_frame, text="🌐 Internet Speed Test", font=("Berlin Sans FB", 26, "bold"))
title_label.pack(pady=10)

# Test Button
start_btn = ctk.CTkButton(glass_frame, text="🚀 Start Test", font=("Berlin Sans FB", 20), command=test_speed)
start_btn.pack(pady=10)

# Dark Mode Toggle
dark_mode_btn = ctk.CTkButton(glass_frame, text="☀ Light Mode", font=("Berlin Sans FB", 20), command=toggle_dark_mode)
dark_mode_btn.pack(pady=10)

# Result Box
result_textbox = ctk.CTkTextbox(glass_frame, font=("Berlin Sans FB", 16), width=850, height=150)
result_textbox.insert("end", "Click the button to test")
result_textbox.configure(state="disabled")
result_textbox.pack(pady=10)

# History Label
history_label = ctk.CTkLabel(glass_frame, text="📜 Test History", font=("Berlin Sans FB", 20, "bold"))
history_label.pack(pady=5)

# History Frame with Scrollbar
history_frame = ctk.CTkFrame(glass_frame, width=900, height=200)
history_frame.pack_propagate(False)
history_frame.pack(pady=5)

history_textbox = ctk.CTkTextbox(history_frame, font=("Berlin Sans FB", 14), wrap="word")
history_textbox.insert("end", "History will appear here.")
history_textbox.configure(state="disabled")
history_textbox.pack(side="left", fill="both", expand=True)

# Run App
app.mainloop()
