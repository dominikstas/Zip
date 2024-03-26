import tkinter as tk
from tkinter import filedialog, messagebox
import zipfile
import os

class ZipManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zip!")
        self.root.geometry("400x200")  
        self.root.configure(bg="#333333")  

       
        window_width = self.root.winfo_reqwidth()
        window_height = self.root.winfo_reqheight()
        position_right = int(self.root.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(self.root.winfo_screenheight() / 2 - window_height / 2)
        self.root.geometry("+{}+{}".format(position_right, position_down))

        self.frame = tk.Frame(self.root, bg="#333333")  
        self.frame.pack(padx=20, pady=20)

        self.label = tk.Label(self.frame, text="Zip!", font=("Helvetica", 20), fg="white", bg="#333333")  # Zmiana rozmiaru i koloru tekstu etykiety
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        self.zip_button = tk.Button(self.frame, text="Zip", command=self.zip_files, bg="#555555", fg="white")  # Zmiana koloru tła i tekstu przycisku Zip
        self.zip_button.grid(row=1, column=0, padx=5, pady=5)

        self.unzip_button = tk.Button(self.frame, text="Unzip", command=self.unzip_files, bg="#555555", fg="white")  # Zmiana koloru tła i tekstu przycisku Unzip
        self.unzip_button.grid(row=1, column=1, padx=5, pady=5)

    def zip_files(self):
        source_folder = filedialog.askdirectory(title="Select folder to zip")
        if source_folder:
            zip_file_path = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=(("ZIP files", "*.zip"),))
            if zip_file_path:
                with zipfile.ZipFile(zip_file_path, 'w') as zipf:
                    for root, dirs, files in os.walk(source_folder):
                        for file in files:
                            file_path = os.path.join(root, file)
                            zipf.write(file_path, os.path.relpath(file_path, source_folder))
                messagebox.showinfo("Success", "Zipped successfully!")

    def unzip_files(self):
        zip_file = filedialog.askopenfilename(title="Select zip file", filetypes=(("ZIP files", "*.zip"),))
        if zip_file:
            unzip_folder = filedialog.askdirectory(title="Select folder to unzip files")
            if unzip_folder:
                create_new_folder = messagebox.askyesno("Create New Folder", "Do you want to create a new folder for extraction?")
                if create_new_folder:
                    unzip_folder = os.path.join(unzip_folder, os.path.basename(zip_file).split('.')[0])
                    os.makedirs(unzip_folder, exist_ok=True)
                with zipfile.ZipFile(zip_file, 'r') as zipf:
                    zipf.extractall(unzip_folder)
                messagebox.showinfo("Success", "Files unzipped successfully!")


if __name__ == "__main__":
    root = tk.Tk()
    app = ZipManagerApp(root)
    root.mainloop()
