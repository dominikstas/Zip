import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import zipfile
import os

class ZipManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zip!")
        self.root.geometry("400x200")
        self.root.configure(bg="#333333")

        # Centering the window
        self.center_window()

        # Main frame
        self.frame = tk.Frame(self.root, bg="#333333")
        self.frame.pack(padx=20, pady=20)

        # Label
        self.label = tk.Label(self.frame, text="Zip!", font=("Helvetica", 20), fg="white", bg="#333333")
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        # Buttons
        self.zip_button = tk.Button(self.frame, text="Zip", command=self.zip_files, bg="#555555", fg="white")
        self.zip_button.grid(row=1, column=0, padx=5, pady=5)

        self.unzip_button = tk.Button(self.frame, text="Unzip", command=self.unzip_files, bg="#555555", fg="white")
        self.unzip_button.grid(row=1, column=1, padx=5, pady=5)

        # Progress bar
        self.progress = ttk.Progressbar(self.frame, orient='horizontal', mode='determinate', length=300)
        self.progress.grid(row=2, column=0, columnspan=2, pady=10)

    def center_window(self):
        self.root.update_idletasks()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        position_right = int(self.root.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(self.root.winfo_screenheight() / 2 - window_height / 2)
        self.root.geometry(f"+{position_right}+{position_down}")

    def zip_files(self):
        source_folder = filedialog.askdirectory(title="Select folder to zip")
        if source_folder:
            zip_file_path = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=(("ZIP files", "*.zip"),))
            if zip_file_path:
                try:
                    self.progress['value'] = 0
                    files_to_zip = []
                    for root, dirs, files in os.walk(source_folder):
                        for file in files:
                            files_to_zip.append(os.path.join(root, file))
                    
                    total_files = len(files_to_zip)
                    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                        for i, file in enumerate(files_to_zip):
                            zipf.write(file, os.path.relpath(file, source_folder))
                            self.update_progress(i + 1, total_files)
                    messagebox.showinfo("Success", "Zipped successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred while zipping: {e}")

    def unzip_files(self):
        zip_file = filedialog.askopenfilename(title="Select zip file", filetypes=(("ZIP files", "*.zip"),))
        if zip_file:
            unzip_folder = filedialog.askdirectory(title="Select folder to unzip files")
            if unzip_folder:
                create_new_folder = messagebox.askyesno("Create New Folder", "Do you want to create a new folder for extraction?")
                if create_new_folder:
                    unzip_folder = os.path.join(unzip_folder, os.path.basename(zip_file).split('.')[0])
                    os.makedirs(unzip_folder, exist_ok=True)
                try:
                    self.progress['value'] = 0
                    with zipfile.ZipFile(zip_file, 'r') as zipf:
                        total_files = len(zipf.infolist())
                        for i, file in enumerate(zipf.infolist()):
                            zipf.extract(file, unzip_folder)
                            self.update_progress(i + 1, total_files)
                    messagebox.showinfo("Success", "Files unzipped successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred while unzipping: {e}")

    def update_progress(self, current, total):
        self.progress['value'] = (current / total) * 100
        self.root.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = ZipManagerApp(root)
    root.mainloop()
