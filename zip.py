import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
import zipfile
import os
from typing import List

class ZipManagerApp:
    def __init__(self, root: tk.Tk) -> None:
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
        self.create_tooltip(self.zip_button, "Select a folder to zip")

        self.unzip_button = tk.Button(self.frame, text="Unzip", command=self.unzip_files, bg="#555555", fg="white")
        self.unzip_button.grid(row=1, column=1, padx=5, pady=5)
        self.create_tooltip(self.unzip_button, "Select a zip file to unzip")

        # Progress bar
        self.progress = ttk.Progressbar(self.frame, orient='horizontal', mode='determinate', length=300)
        self.progress.grid(row=2, column=0, columnspan=2, pady=10)

    def center_window(self) -> None:
        self.root.update_idletasks()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        position_right = int(self.root.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(self.root.winfo_screenheight() / 2 - window_height / 2)
        self.root.geometry(f"+{position_right}+{position_down}")

    def zip_files(self) -> None:
        source_folder = filedialog.askdirectory(title="Select folder to zip")
        if source_folder:
            zip_file_path = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=(("ZIP files", "*.zip"),))
            if zip_file_path:
                try:
                    self.progress['value'] = 0
                    files_to_zip = self.get_files_to_zip(source_folder)
                    if not files_to_zip:
                        messagebox.showinfo("No Files", "The selected folder is empty.")
                        return
                    
                    # Get the maximum size limit from the user
                    max_size_mb = simpledialog.askinteger("Max Size", "Enter the maximum size of each zip file in MB:", minvalue=1)
                    if max_size_mb:
                        max_size_bytes = max_size_mb * 1024 * 1024  # Convert MB to bytes
                        self.create_multiple_zip_files(zip_file_path, source_folder, files_to_zip, max_size_bytes)
                        messagebox.showinfo("Success", "Zipped successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred while zipping: {e}")

    def unzip_files(self) -> None:
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
                    self.extract_zip_file(zip_file, unzip_folder)
                    messagebox.showinfo("Success", "Files unzipped successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred while unzipping: {e}")

    def get_files_to_zip(self, source_folder: str) -> List[str]:
        files_to_zip = []
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                files_to_zip.append(os.path.join(root, file))
        return files_to_zip

    def create_multiple_zip_files(self, zip_file_path: str, source_folder: str, files_to_zip: List[str], max_size_bytes: int) -> None:
        total_files = len(files_to_zip)
        current_zip_index = 1
        current_zip_size = 0
        current_zip_files = []

        def save_current_zip():
            nonlocal current_zip_files, current_zip_index, current_zip_size
            if current_zip_files:
                zip_path = f"{os.path.splitext(zip_file_path)[0]}_{current_zip_index}.zip"
                self.create_zip_file(zip_path, source_folder, current_zip_files)
                current_zip_files = []
                current_zip_index += 1
                current_zip_size = 0

        for i, file in enumerate(files_to_zip):
            file_size = os.path.getsize(file)
            if current_zip_size + file_size > max_size_bytes:
                save_current_zip()
            current_zip_files.append(file)
            current_zip_size += file_size
            self.update_progress(i + 1, total_files)

        save_current_zip()
        self.reset_progress_bar()

    def create_zip_file(self, zip_file_path: str, source_folder: str, files_to_zip: List[str]) -> None:
        with zipfile.ZipFile(zip_file_path, 'w') as zipf:
            for file in files_to_zip:
                zipf.write(file, os.path.relpath(file, source_folder))

    def extract_zip_file(self, zip_file: str, unzip_folder: str) -> None:
        with zipfile.ZipFile(zip_file, 'r') as zipf:
            total_files = len(zipf.infolist())
            for i, file in enumerate(zipf.infolist()):
                zipf.extract(file, unzip_folder)
                self.update_progress(i + 1, total_files)
        self.reset_progress_bar()

    def update_progress(self, current: int, total: int) -> None:
        self.progress['value'] = (current / total) * 100
        self.root.update_idletasks()

    def reset_progress_bar(self) -> None:
        self.progress['value'] = 0

    def create_tooltip(self, widget: tk.Widget, text: str) -> None:
        tooltip = tk.Label(widget, text=text, bg="#555555", fg="white", relief='solid', borderwidth=1, wraplength=150)
        tooltip.place(x=widget.winfo_x(), y=widget.winfo_y() - 30)
        tooltip.after(1500, tooltip.destroy)

if __name__ == "__main__":
    root = tk.Tk()
    app = ZipManagerApp(root)
    root.mainloop()
