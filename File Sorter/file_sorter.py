#* Tkinter Imports
from tkinterdnd2 import TkinterDnD, DND_FILES
import tkinter as tk

#* Imports for Files
from os.path import basename
from pathlib import Path
import zipfile
import tarfile
import rarfile

#* Clear the console after exit
def cc():
    from os import system, name

    system("cls" if name == 'nt' else 'clear')

class Main:
    def __init__(self):
        self.dropped_files = []
        self.basename_files = []
        self.selected_option = None
        self.dropdown_menu = None
        self.file_path_selected = None
        self.path_display = None

    #* Handle file drops
    def on_drop(self, event):
        paths = self.root.tk.splitlist(event.data)
        new_files = [Path(p) for p in paths]
        new_basenames = [basename(p) for p in paths]

        self.dropped_files.extend(new_files)
        self.basename_files.extend(new_basenames)

        self.update_dropdown()

    #* Handle folder drop for target path
    def on_folder_drop(self, event):
        paths = self.root.tk.splitlist(event.data)
        folder = Path(paths[0])
        if folder.is_dir():
            self.file_path_selected = folder
            self.path_display.config(text=f"{folder}")
            self.sort_button.config(state='normal')

    #* Update dropdown with file names
    def update_dropdown(self):
        menu = self.dropdown_menu["menu"]
        menu.delete(0, "end")

        for name in self.basename_files:
            menu.add_command(label=name, command=lambda value=name: self.selected_option.set(value))

        if self.basename_files:
            self.selected_option.set(self.basename_files[-1])
            self.dropdown_menu.config(state='normal')

    #* Check for extension
    def check_extension(self, fp: Path):
        return fp.suffix

    #* Creating new folders for extensions
    def create_new_folder(self, base_folder: Path, extension: str) -> Path:
        """
        Creates a subfolder inside base_folder named after the file extension (no dot).
        Returns the path to the new subfolder.
        """
        if not base_folder.is_dir():
            return 'Directory'

        ext_name = extension.lower().lstrip('.')
        ext_folder = base_folder / ext_name

        ext_folder.mkdir(parents=True, exist_ok=True)
        return ext_folder

    def create_ext_folder(self, base_folder: Path):
        """
        Creates a subfolder inside base_folder for extracted folders
        """
        ext_name = "Folders and Extracted Folders"
        ext_folder = base_folder / ext_name

        ext_folder.mkdir(parents=True, exist_ok=True)
        return ext_folder

    #* Extract Methods
    def extract_zip(self, zip_path: Path, extract_path: Path):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

    def extract_tar(self, tar_path: Path, extract_path: Path):
        with tarfile.open(tar_path, 'r:*') as tar_ref:
            tar_ref.extractall(extract_path)

    def extract_rar(self, rar_path: Path, extract_path: Path):
        with rarfile.RarFile(rar_path, 'r') as rar_ref:
            rar_ref.extractall(extract_path)

    #* Extract Zip, Tar, Tar-Gz, Tgz, and Rar Files
    def extract_archive(self, archive_path: Path, extract_to: Path):
        if archive_path.suffix == ".zip":
            self.extract_zip(archive_path, extract_to)
            return None
        elif archive_path.suffix in [".tar", ".gz", ".tgz", ".bz2"]:
            self.extract_tar(archive_path, extract_to)
            return None
        elif archive_path.suffix == ".rar":
            self.extract_rar(archive_path, extract_to)
            return None
        else:
            return 'Not Extractable File'

    #* Sort the files
    def sort_files(self):
        if not self.dropped_files or not self.file_path_selected:
            return

        for file in self.dropped_files:
            ext = self.check_extension(file)

            if file.is_dir():
                # Move normal folders
                folder_target = self.create_ext_folder(self.file_path_selected)
                dest = folder_target / file.name
                try:
                    file.rename(dest)
                    print(f"Moved folder: {file.name} → {dest}")
                except Exception as e:
                    print(f"Failed to move folder {file}: {e}")
                continue

            if ext in ['.zip', '.tar', '.gz', '.tgz', '.bz2', '.rar']:
                # Extract archive into a named subfolder
                folder_target = self.create_ext_folder(self.file_path_selected)
                extract_folder = folder_target / file.stem
                extract_folder.mkdir(parents=True, exist_ok=True)

                try:
                    self.extract_archive(file, extract_folder)
                    file.unlink()  # Delete original archive
                    print(f"Extracted {file.name} to {extract_folder}")
                except Exception as e:
                    print(f"Failed to extract {file}: {e}")
                continue

            # Normal file – sort by extension
            target_folder = self.create_new_folder(self.file_path_selected, ext)
            try:
                destination = target_folder / file.name
                file.rename(destination)
                print(f"Moved {file.name} → {destination}")
            except Exception as e:
                print(f"Failed to move file {file}: {e}")

    #* Main window setup
    def run_window(self):
        self.root = TkinterDnD.Tk()
        self.root.geometry('500x500')
        self.root.resizable(False, False)
        self.root.title("File Sorter")

        #* File drop zone
        drop_zone = tk.Label(self.root, text="Drop Files Here", width=40, height=10, bg="lightblue", relief='groove')
        drop_zone.pack(padx=20, pady=10)
        drop_zone.drop_target_register(DND_FILES)
        drop_zone.dnd_bind("<<Drop>>", self.on_drop)

        #* Dropdown menu
        self.selected_option = tk.StringVar(self.root)
        self.selected_option.set('No Files Dropped Yet')
        self.dropdown_menu = tk.OptionMenu(self.root, self.selected_option, ())
        self.dropdown_menu.pack()
        self.dropdown_menu.config(state='disabled')

        #* Folder drop zone (next to label)
        path_frame = tk.Frame(self.root)
        path_frame.pack(pady=10)

        label = tk.Label(path_frame, text="File Path:", anchor='w', relief='groove', bg='lightblue')
        label.pack(side="left", padx=(0, 10))

        self.path_display = tk.Label(path_frame, text="(Drop folder here)", width=30, height=1, bg="lightblue", relief='groove', anchor='w', justify='left')
        self.path_display.pack(side="left")

        self.path_display.drop_target_register(DND_FILES)
        self.path_display.dnd_bind("<<Drop>>", self.on_folder_drop)

        #* Sort Button
        self.sort_button = tk.Button(self.root, text="Sort Files", state='disabled', command=self.sort_files)
        self.sort_button.pack(pady=20)

        self.root.mainloop()

Main().run_window()
cc()