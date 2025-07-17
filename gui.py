from tkinter.ttk import *

import tkinter as tk
from tkinter import filedialog, messagebox, Listbox 
import os
from config_manager import load_config
from obs import ObsClient
from config_manager import load_config  # 👈 This will get settings from settings.json
from tkinter import filedialog
from settings_window import SettingsWindow
from helper.helper import get_selected_bucket



class OBSUploaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Huawei OBS Desktop Uploader")
        self.root.geometry("600x600")
        self.root.configure(bg="#f0f4f8")  # light background
                
        self.config = load_config()        

        # Top-right settings button
        top_frame = tk.Frame(root,  bg="#f0f4f8")
        top_frame.grid(row=0, column=2, sticky="e", padx=10, pady=5)
        tk.Button(top_frame, text="⚙️ Settings", command=self.open_settings).pack()
       
        # Combobox to show buckets (grid-based layout, consistent style)
        Label(root, text="Select Bucket:", background="#f0f4f8", font=("Segoe UI", 10)).grid(row=6, column=0, padx=10, pady=(20, 5), sticky="w")
        self.bucket_combo = Combobox(root, width=50, font=("Segoe UI", 10))
        self.bucket_combo.grid(row=6, column=1, padx=10, pady=(20, 5), columnspan=2, sticky="w")
        Button(root, text="List Buckets", command=self.list_buckets).grid(row=7, column=1, pady=10, sticky="w")

        # Folder selection
        tk.Label(root, text="Upload Folder:").grid(row=1, column=0, padx=5, pady=5)
        self.folder_var = tk.StringVar(value=self.config["upload_folder"])
        self.folder_entry = tk.Entry(root, textvariable=self.folder_var, width=60)
        self.folder_entry.grid(row=1, column=1, padx=5)
        tk.Button(root, text="Browse", command=self.browse_folder).grid(row=1, column=2, padx=5)

        # Buttons
        tk.Button(root, text="Upload File", bg="#0052cc",
            fg="white",
            font=("Arial", 12),
            relief="raised",
            bd=3, command=self.upload_file).grid(row=2, column=0, pady=10)
        
        # File List
        self.file_listbox = Listbox(root, width=60, height=10)
        self.file_listbox.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        self.obs_file_listbox = Listbox(root, width=60, height=10)
        self.obs_file_listbox.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
        
        button_frame = tk.Frame(root)
        button_frame.grid(row=5, column=0, columnspan=3, pady=10)

        
        tk.Button(button_frame, text="Refresh Bucket Files", command=self.list_obs_files).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Delete File", command=self.delete_file).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Download File", command=self.download_file).pack(side=tk.LEFT, padx=10)
                
        self.refresh_file_list()

    def browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.folder_var.set(path)
            self.refresh_file_list()

    def open_settings(self):
        SettingsWindow(self.root)


    def refresh_file_list(self):
        folder = self.folder_var.get()
        if not os.path.exists(folder):
            os.makedirs(folder)
        self.file_listbox.delete(0, tk.END)
        for file in os.listdir(folder):
            self.file_listbox.insert(tk.END, file)

    def upload_file(self):
        try:
            folder = self.folder_var.get()
            selected_index = self.file_listbox.curselection()

            if not selected_index:
                messagebox.showwarning("No file selected", "Please select a file to upload.")
                return

            file_name = self.file_listbox.get(selected_index)
            file_path = os.path.join(folder, file_name)

            # ✅ Load config from settings.json
            config = load_config()
            access_key = config.get("access_key")
            secret_key = config.get("secret_key")
            server = config.get("endpoint")
            # bucket_name = config.get("bucket")
            # bucket_name = self.bucket_combo.get()
            bucket_name = get_selected_bucket(self.bucket_combo)
            if not bucket_name:
                return  # Don't proceed if no bucket selected

            # === Initialize OBS Client using loaded config ===
            obs_client = ObsClient(
                access_key_id=access_key,
                secret_access_key=secret_key,
                server=server
            )

            # === Upload the file ===
            resp = obs_client.putFile(bucket_name, file_name, file_path)          

            if resp.status < 300:
                messagebox.showinfo("Success", f"File '{file_name}' uploaded successfully.")
            else:
                messagebox.showerror("Upload Failed", f"Error Code: {resp.errorCode}\nMessage: {resp.errorMessage}")

            obs_client.close()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def list_obs_files(self):
        try:
            config = load_config()
            access_key = config.get("access_key")
            secret_key = config.get("secret_key")
            server = config.get("endpoint")
            # bucket_name = config.get("bucket")
            # bucket_name = self.bucket_combo.get()
            bucket_name = get_selected_bucket(self.bucket_combo)
            if not bucket_name:
                return 

            obs_client = ObsClient(
                access_key_id=access_key,
                secret_access_key=secret_key,
                server=server
            )

            self.obs_file_listbox.delete(0, tk.END)  # Clear previous list

            response = obs_client.listObjects(bucket_name)

            if response.status < 300:
                for obj in response.body.contents:
                    self.obs_file_listbox.insert(tk.END, obj.key)
            else:
                self.obs_file_listbox.insert(tk.END, "Failed to fetch file list.")

            obs_client.close()

        except Exception as e:
            self.obs_file_listbox.insert(tk.END, f"Error: {str(e)}")


    def delete_file(self):
        selected = self.obs_file_listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a file to delete.")
            return

        file_name = self.obs_file_listbox.get(selected[0])

        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete '{file_name}' from OBS?")
        if not confirm:
            return

        try:
            config = load_config()
            obs_client = ObsClient(
                access_key_id=config["access_key"],
                secret_access_key=config["secret_key"],
                server=config["endpoint"]
            )

            response = obs_client.deleteObject(config["bucket"], file_name)

            if response.status < 300:
                messagebox.showinfo("Success", f"'{file_name}' deleted from OBS.")
                self.list_obs_files()  # Refresh
            else:
                messagebox.showerror("Error", f"Failed to delete file: {response.errorMessage}")

            obs_client.close()

        except Exception as e:
            messagebox.showerror("Error", str(e))
    

    def download_file(self):
        selected = self.obs_file_listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a file to download.")
            return

        file_name = self.obs_file_listbox.get(selected[0])

        save_path = filedialog.asksaveasfilename(initialfile=file_name, title="Save File As")
        if not save_path:
            return

        try:
            config = load_config()
            obs_client = ObsClient(
                access_key_id=config["access_key"],
                secret_access_key=config["secret_key"],
                server=config["endpoint"]
            )

            response = obs_client.getObject(config["bucket"], file_name, downloadPath=save_path)

            if response.status < 300:
                messagebox.showinfo("Success", f"'{file_name}' downloaded to:\n{save_path}")
            else:
                messagebox.showerror("Error", f"Download failed: {response.errorMessage}")

            obs_client.close()

        except Exception as e:
            messagebox.showerror("Error", str(e))
    

    def list_buckets(self):
        try:
            # Load from config (assuming your config keys are named like this)
            ak = self.config.get("access_key")
            sk = self.config.get("secret_key")
            endpoint = self.config.get("endpoint")

            # Initialize OBS client
            obs_client = ObsClient(
                access_key_id=ak,
                secret_access_key=sk,
                server=endpoint
            )

            # List buckets
            resp = obs_client.listBuckets()

            if resp.status < 300:
                buckets = [bucket.name for bucket in resp.body.buckets]
                self.bucket_combo['values'] = buckets
                if buckets:
                    self.bucket_combo.current(0)
            else:
                messagebox.showerror("Error", f"Failed to list buckets: {resp.errorCode} - {resp.errorMessage}")

            obs_client.close()

        except Exception as e:
            messagebox.showerror("Exception", str(e))


