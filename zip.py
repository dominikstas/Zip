import tkinter as tk
from tkinter import filedialog
import zipfile
import os

class ZipManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zip Manager")

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)

        self.label = tk.Label(self.frame, text="Zip Manager", font=("Helvetica", 16))
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        self.zip_button = tk.Button(self.frame, text="Zip files", command=self.zip_files)
        self.zip_button.grid(row=1, column=0, padx=5, pady=5)

        self.unzip_button = tk.Button(self.frame, text="Unzip files", command=self.unzip_files)
        self.unzip_button.grid(row=1, column=1, padx=5, pady=5)

    def zip_files(self):
        files = filedialog.askopenfilenames(title="Select files to zip", filetypes=(("All files", "*.*"),))
        if files:
            zip_file_path = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=(("ZIP files", "*.zip"),))
            if zip_file_path:
                with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                    for file in files:
                        zipf.write(file, os.path.basename(file))
                tk.messagebox.showinfo("Success", "Files zipped successfully!")

    def unzip_files(self):
        zip_file = filedialog.askopenfilename(title="Select zip file", filetypes=(("ZIP files", "*.zip"),))
        if zip_file:
            unzip_folder = filedialog.askdirectory(title="Select folder to unzip files")
            if unzip_folder:
                with zipfile.ZipFile(zip_file, 'r') as zipf:
                    zipf.extractall(unzip_folder)
                tk.messagebox.showinfo("Success", "Files unzipped successfully!")


if __name__ == "__main__":
    root = tk.Tk()
    app = ZipManagerApp(root)
    root.mainloop()
