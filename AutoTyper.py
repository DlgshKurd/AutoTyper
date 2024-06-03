import tkinter as tk
from tkinter import ttk, messagebox
import time
import pyperclip
import keyboard
import threading

class AutoTyperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoTyper")
        self.root.geometry("200x240")
        self.root.resizable(False, False)

        self.typing_speed = tk.DoubleVar(value=0.05)
        self.timer_value = tk.IntVar(value=3)
        self.stop_typing = threading.Event()
        self.pause_typing = threading.Event()
        self.transparency = 1.0

        # Style
        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 10))
        style.configure('TLabel', font=('Helvetica', 10))
        style.configure('TScale', length=200)

        # Main frame
        frame = ttk.Frame(root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Write button
        self.write_button = ttk.Button(frame, text="Write", command=self.write_clipboard_content)
        self.write_button.grid(row=0, column=0, columnspan=2, pady=5)

        # Stay on top toggle button
        self.stay_on_top = tk.BooleanVar(value=True)
        self.stay_on_top_button = ttk.Checkbutton(frame, text="Stay on Top", variable=self.stay_on_top, command=self.toggle_stay_on_top)
        self.stay_on_top_button.grid(row=1, column=0, columnspan=2, pady=5)

        # Write from text field button
        self.write_text_field_button = ttk.Button(frame, text="Write Text Field Content", command=self.show_text_field_window)
        self.write_text_field_button.grid(row=2, column=0, columnspan=2, pady=5)

        # Typing speed slider
        self.speed_label = ttk.Label(frame, text="Typing Speed")
        self.speed_label.grid(row=3, column=0, pady=5, sticky=tk.E)
        self.speed_slider = ttk.Scale(frame, from_=0.01, to=0.5, orient=tk.HORIZONTAL, variable=self.typing_speed)
        self.speed_slider.grid(row=3, column=1, pady=5, sticky=tk.W)

        # Timer entry
        self.timer_label = ttk.Label(frame, text="Timer (seconds)")
        self.timer_label.grid(row=4, column=0, pady=5, sticky=tk.E)
        self.timer_entry = ttk.Entry(frame, textvariable=self.timer_value, width=5)
        self.timer_entry.grid(row=4, column=1, pady=5, sticky=tk.W)

        # Instruction button
        self.instruction_button = ttk.Button(frame, text="Show Keybinds", command=self.show_keybinds_info)
        self.instruction_button.grid(row=5, column=0, columnspan=2, pady=10)

        self.toggle_stay_on_top()
        
        # Updated hotkeys
        keyboard.add_hotkey('F10', self.force_stop)
        keyboard.add_hotkey('F9', self.toggle_pause)
        keyboard.add_hotkey('F8', self.increase_speed)
        keyboard.add_hotkey('F7', self.decrease_speed)
        keyboard.add_hotkey('F11', self.decrease_transparency)
        keyboard.add_hotkey('F12', self.increase_transparency)
        keyboard.add_hotkey('F6', self.toggle_stay_on_top)

    def write_clipboard_content(self):
        try:
            clipboard_content = pyperclip.paste()
            self.type_text_with_countdown(clipboard_content)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def toggle_stay_on_top(self):
        self.root.attributes("-topmost", self.stay_on_top.get())

    def show_text_field_window(self):
        text_window = tk.Toplevel(self.root)
        text_window.title("Enter Text")
        text_window.geometry("300x200")
        text_window.resizable(False, False)

        # Position text window next to the main window
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        text_window.geometry(f"+{x + 360}+{y}")

        text_label = ttk.Label(text_window, text="Enter your text:")
        text_label.pack(pady=10)

        text_field = tk.Text(text_window, wrap=tk.WORD, width=30, height=5)
        text_field.pack(pady=10)

        write_text_button = ttk.Button(text_window, text="Write", command=lambda: self.write_text_field_content(text_field))
        write_text_button.pack(pady=10)

    def write_text_field_content(self, text_field):
        try:
            text_content = text_field.get("1.0", tk.END)
            self.type_text_with_countdown(text_content)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def type_text_with_countdown(self, text):
        self.stop_typing.clear()
        self.pause_typing.clear()
        countdown = self.timer_value.get()
        for i in range(countdown, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        threading.Thread(target=self.type_text, args=(text,)).start()

    def type_text(self, text):
        for char in text:
            if self.stop_typing.is_set():
                break
            while self.pause_typing.is_set():
                time.sleep(0.1)
            keyboard.write(char, delay=self.typing_speed.get())
        print("Typing completed or stopped.")

    def force_stop(self):
        self.stop_typing.set()

    def toggle_pause(self):
        if self.pause_typing.is_set():
            self.pause_typing.clear()
        else:
            self.pause_typing.set()

    def increase_speed(self):
        if self.typing_speed.get() > 0.01:
            self.typing_speed.set(max(0.01, self.typing_speed.get() - 0.01))

    def decrease_speed(self):
        self.typing_speed.set(min(0.5, self.typing_speed.get() + 0.01))

    def increase_transparency(self):
        if self.transparency < 1.0:
            self.transparency += 0.1
            self.root.attributes('-alpha', self.transparency)

    def decrease_transparency(self):
        if self.transparency > 0.1:
            self.transparency -= 0.1
            self.root.attributes('-alpha', self.transparency)

    def show_keybinds_info(self):
        keybinds_info = (
            "Keybinds Information:\n"
            "F10: Stop\n"
            "F9: Pause/Resume\n"
            "F8: Speed Up\n"
            "F7: Slow Down\n"
            "F11: Decrease Transparency\n"
            "F12: Increase Transparency\n"
            "F6: Toggle Stay on Top\n"
        )
        messagebox.showinfo("Keybinds", keybinds_info)

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoTyperApp(root)
    root.mainloop()
