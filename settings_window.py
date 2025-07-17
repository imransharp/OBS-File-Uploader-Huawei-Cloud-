# obs_uploader/settings_window.py

import tkinter as tk
from tkinter import ttk, messagebox
from config_manager import load_config, save_config

class SettingsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Settings")
        self.geometry("400x300")
        self.resizable(False, False)

        self.config = load_config()

        # Form fields
        self.entries = {}
        fields = ["access_key", "secret_key", "endpoint", "bucket", "upload_folder"]

        for idx, field in enumerate(fields):
            tk.Label(self, text=field.replace("_", " ").title() + ":").grid(row=idx, column=0, sticky="w", padx=10, pady=5)
            entry = ttk.Entry(self, width=40)
            entry.insert(0, self.config.get(field, ""))
            entry.grid(row=idx, column=1, padx=10, pady=5)
            self.entries[field] = entry

        # Save button
        save_btn = ttk.Button(self, text="Save", command=self.save_settings)
        save_btn.grid(row=len(fields), columnspan=2, pady=15)

    def save_settings(self):
        new_config = {field: entry.get().strip() for field, entry in self.entries.items()}
        save_config(new_config)
        messagebox.showinfo("Saved", "Settings updated successfully.")
        self.destroy()
