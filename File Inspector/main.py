import os
import time
import shutil
from datetime import datetime

from VividText import VividText as vt

# ---------- Functions ----------
def cc():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_folder_to_inspect():
    tp = vt(bold=True, sleep=.02)
    while True:
        folder_to_inspect = tp.inputTypewriter("Type a folder name or file path to inspect")
        if os.path.exists(folder_to_inspect) and os.path.isdir(folder_to_inspect):
            break
        else:
            tp.typewriter("Not a valid folder.")
    return folder_to_inspect

def get_file_size(file):
    size = os.path.getsize(file)
    units = ['Bytes', 'KB', 'MB', 'GB', 'TB']
    unit_index = 0
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    return f"{size:.2f} {units[unit_index]}"

def get_file_mod(file):
    try:
        mod_time = os.path.getmtime(file)
        return time.strftime("%a, %b %d, %Y. %H:%M:%S", time.localtime(mod_time))
    except Exception:
        return "Unknown"

# ---------- Main Class ----------
class Main:
    def __init__(self, root='file_inspector'):
        self.tp = vt(bold=True, sleep=.02)
        self.folder = None
        self.folder_history = []
        self.return_to_main = False
        self.kill_all = False
        self.root = root
        self.templates = {
            'txt': '', "py": "#", "js": "//", "java": "//", "cpp": "//",
            "c": "//", "html": "<!-- {text} -->", "xml": "<!-- {text} -->",
            "css": "/* {text} */", "sql": "--", "ini": ";", "sh": "#",
            "yaml": "#", "yml": "#"
        }

    def scan_file_for_malware(self, file_path):
        suspicious_keywords = [
            'eval', 'exec', 'subprocess', 'os.system', 'base64', 'import socket',
            'powershell', 'cmd.exe', 'wget', 'curl', 'CreateObject("WScript.Shell")'
        ]
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                contents = f.read().lower()
                for keyword in suspicious_keywords:
                    if keyword in contents:
                        return True, keyword
        except Exception as e:
            return False, f"Scan error: {e}"
        return False, None

    def check_to_return_to_menu(self):
        while True:
            choice = self.tp.inputTypewriter("\nGo back to menu, quit, or stay in the file? (menu/quit/folder)").lower()
            if choice in ['menu', 'm']:
                self.return_to_main = True
                return
            elif choice in ['quit', 'q']:
                self.kill_all = True
                return
            elif choice in ['folder', 'f']:
                return
            else:
                self.tp.typewriter("Invalid option.")
                cc()

    def get_len_of_insides(self, path):
        files, dirs = 0, 0
        try:
            for obj in os.listdir(path):
                full = os.path.join(path, obj)
                if os.path.isdir(full): dirs += 1
                else: files += 1
        except Exception:
            pass
        return files + dirs, files, dirs

    def add_folder(self, current_path=None):
        def add(name):
            try:
                os.mkdir(name)
            except FileExistsError:
                self.tp.typewriter("File already exists, cannot overwrite.")

        if current_path is None:
            current_path = self.folder

        while True:
            cc()
            name = self.tp.inputTypewriter("Select a name of your folder or type quit to quit").replace(' ', '_')
            if name.lower() in ['q', 'quit']:
                self.check_to_return_to_menu()
                break
            if not os.path.exists(os.path.join(current_path, name)):
                add(os.path.join(current_path, name))
                break
            else:
                self.tp.typewriter("Not a valid option.")

    def add_file(self, current_path=None):
        def add(file, type='txt'):
            with open(file, 'w') as obj:
                time_created = datetime.now()
                text = f"New File created at: {time_created}"
                template = self.templates.get(type, "#")
                comment = template.format(text=text) if "{text}" in template else f"{template} {text}"
                obj.write(f"{comment}\n")

        if current_path is None:
            current_path = self.folder

        while True:
            cc()
            name = self.tp.inputTypewriter("Type in the name of your file or type quit to quit").replace(' ', '_')
            if name.lower() in ['q', 'quit']:
                self.check_to_return_to_menu()
                break
            if not os.path.exists(os.path.join(current_path, name)):
                while True:
                    self.tp.typewriter("----------- File Types -----------")
                    for temp in self.templates:
                        self.tp.typewriter(f"   - {temp}")
                    temps = self.tp.inputTypewriter("Select a type of file")
                    if temps in self.templates:
                        break
                fp = os.path.join(current_path, f"{name}.{temps}")
                add(fp, temps)
                break
            else:
                self.tp.typewriter("That file already exists.")

    def choose_addition(self, current_path=None):
        if current_path is None:
            current_path = self.folder
        while True:
            cc()
            choice = self.tp.inputTypewriter("Would you like to add a file or a folder, or type 'quit' to quit. (fl/fd/q)").lower()
            if choice in ['fl', 'file']:
                self.add_file(current_path)
                continue
            elif choice in ['fd', 'folder']:
                self.add_folder(current_path)
                continue
            elif choice in ['q', 'quit']:
                self.check_to_return_to_menu()
                break
            else:
                self.tp.typewriter("Not a valid option.")

    def remove_file(self, current_path=None):
        def remove(file):
            try:
                os.remove(file)
            except PermissionError:
                self.tp.typewriter(f"Unable to remove {os.path.basename(file).replace('_', ' ')}")
            except FileNotFoundError:
                self.tp.typewriter(f"Unable to find {os.path.basename(file).replace('_', ' ')}")

        if current_path is None:
            current_path = self.folder

        files = [obj for obj in os.listdir(current_path) if os.path.isfile(os.path.join(current_path, obj))]
        if not files:
            self.tp.typewriter("No files.")
            time.sleep(0.2)
            return

        while True:
            cc()
            self.tp.typewriter("---------- Files able to delete. ----------")
            self.tp.typewriter()
            for file in files:
                self.tp.typewriter(f"File: {file.replace('_', ' ')}")
            self.tp.typewriter()
            choice = self.tp.inputTypewriter("Select a file to delete, or type 'quit' to exit")
            if choice.lower() in ['q', 'quit']:
                self.check_to_return_to_menu()
                break
            fp = os.path.join(current_path, choice.replace(' ', '_'))
            if os.path.exists(fp):
                rep = self.tp.inputTypewriter(f"Are you sure you want to delete {self.get_breadcrumb_path(fp)}? (y/n)").strip().lower()
                if rep in ['y', 'yes']:
                    remove(fp)
                    files = [obj for obj in os.listdir(current_path) if os.path.isfile(os.path.join(current_path, obj))]
                    if not files:
                        self.tp.typewriter("No more files.")
                        time.sleep(0.2)
                        return
                else:
                    self.tp.typewriter("Okay, canceling...")
                self.tp.inputTypewriter("Press enter to continue.",end='')
            else:
                self.tp.typewriter("Not a valid file.")

    def remove_folder(self, current_path=None):
        if current_path is None:
            current_path = self.folder
        def remove(name):
            try:
                shutil.rmtree(os.path.join(current_path, name))
            except PermissionError:
                self.tp.typewriter(f"{self.get_breadcrumb_path(name)} is not allowed to be removed.")
            except FileNotFoundError:
                self.tp.typewriter(f"{self.get_breadcrumb_path(name)} is not found.")

        folders = [obj for obj in os.listdir(current_path) if os.path.isdir(os.path.join(current_path, obj))]
        if not folders:
            self.tp.typewriter("No folders were found.")

        while True:
            cc()
            self.tp.typewriter("---------- Folders able to delete ----------")
            for fold in folders:
                self.tp.typewriter(f"Folder: {fold}")
            self.tp.typewriter()
            choice = self.tp.inputTypewriter("Select a folder to remove or type 'quit' to quit.").replace(' ', '_')
            if choice.lower() in ['q', 'quit']:
                self.check_to_return_to_menu()
                break
            elif os.path.isdir(os.path.join(current_path, choice)):
                confirm = self.tp.inputTypewriter(f"Are you sure you want to remove {choice}? (y/n)").lower()
                if confirm in ['y', 'yes']:
                    remove(choice)
                    folders = [obj for obj in os.listdir(current_path) if os.path.isdir(os.path.join(current_path, obj))]
                    if not folders:
                        return
                elif confirm in ['n', 'no']:
                    self.tp.typewriter("Okay.")
                else:
                    self.tp.typewriter("Not an option.")
            else:
                self.tp.typewriter('Not a valid folder.')

    def choose_removal(self, current_path=None):
        if current_path is None:
            current_path = self.folder
        while True:
            cc()
            choice = self.tp.inputTypewriter("Would you like to remove a file or a folder, or type 'quit' to quit. (fl/fd/q)").lower()
            if choice in ['fl', 'file']:
                self.remove_file(current_path)
                continue
            elif choice in ['fd', 'folder']:
                self.remove_folder(current_path)
                continue
            elif choice in ['q', 'quit']:
                self.check_to_return_to_menu()
                break
            else:
                self.tp.typewriter("Not a valid option.")

    def get_breadcrumb_path(self, current_path=None):
        if current_path is None:
            current_path = self.folder
        try:
            root_abs = os.path.abspath(self.root)
            current_abs = os.path.abspath(current_path)
            if not current_abs.startswith(root_abs):
                return current_abs
            relative_path = os.path.relpath(current_abs, root_abs)
            parts = relative_path.split(os.sep)
            if len(parts) <= 3:
                return f"{os.path.basename(root_abs)} / {' / '.join(parts)}"
            else:
                return f"{os.path.basename(root_abs)} / ... / {' / '.join(parts[-2:])}"
        except Exception:
            return current_path

    def show_file_details(self):
        cc()
        size = get_file_size(self.folder)
        mod = get_file_mod(self.folder)
        self.tp.typewriter(
            f"\n📄 {os.path.basename(self.folder).replace('_', ' ')}\n"
            f"   - Size: {size}\n"
            f"   - Modified: {mod}"
        )
        flagged, reason = self.scan_file_for_malware(self.folder)
        if flagged:
            self.tp.typewriter(f"   ⚠️  Potential malware detected (matched: {reason})")
        elif reason and reason.startswith("Scan error"):
            self.tp.typewriter(f"   ⚠️  Could not scan file: {reason}")

        self.check_to_return_to_menu()

        if self.return_to_main or self.kill_all:
            return

        # === HERE IS THE CHANGE ===
        # If user chose to stay in folder, show the folder containing this file
        self.folder = os.path.dirname(self.folder)
        self.display_folder_contents()

    def display_folder_contents(self):
        while not self.kill_all:
            cc()
            if not os.path.isdir(self.folder):
                self.show_file_details()
                return

            try:
                entries = os.listdir(self.folder)
            except Exception:
                self.tp.typewriter("Cannot access folder contents.")
                time.sleep(1)
                if self.folder_history:
                    self.folder = self.folder_history.pop()
                else:
                    self.return_to_main = True
                return

            if not entries:
                self.tp.typewriter(f"📁 '{os.path.basename(self.folder)}' is empty.")
                while True:
                    c = self.tp.inputTypewriter("Would you like to add a file? (yes/no)").strip().lower()
                    if c in ('y', 'yes'):
                        self.add_file()
                    elif c in ('n', 'no'):
                        self.tp.inputTypewriter("Press enter to go back.")
                        break
                    else:
                        self.tp.typewriter("Not an option.")
                        time.sleep(0.2)
                if self.folder_history:
                    self.folder = self.folder_history.pop()
                else:
                    self.return_to_main = True
                return

            paths = []
            for name in entries:
                path = os.path.join(self.folder, name)
                paths.append((path, get_file_size(path), get_file_mod(path)))

            for path, file_size, file_mod in paths:
                base = os.path.basename(path).replace('_', ' ')
                if os.path.isdir(path):
                    total, file_count, dir_count = self.get_len_of_insides(path)
                    self.tp.typewriter(
                        f"📁 Folder: {base}\n"
                        f"   - Location: {self.get_breadcrumb_path(path)}\n"
                        f"   - Items: {total} (Files: {file_count}, Folders: {dir_count})"
                    )
                else:
                    self.tp.typewriter(
                        f"📄 File: {base}\n"
                        f"   - Location: {self.get_breadcrumb_path(path)}\n"
                        f"   - Size: {file_size}\n"
                        f"   - Modified: {file_mod}"
                    )
                self.tp.typewriter("\n")

            self.tp.typewriter(
                "Select a file to inspect."
                "\nType 'add' to add a file or folder."
                "\nType 'del' to delete a file or folder."
                "\nType 'back' to go up a folder."
                "\nType 'quit' to exit."
            )
            choice = self.tp.inputTypewriter("Your option ").strip().lower()

            if choice in ['quit', 'q']:
                self.check_to_return_to_menu()
                self.return_to_main = True
                return
            elif choice in ['back', 'b']:
                if self.folder_history:
                    self.folder = self.folder_history.pop()
                else:
                    self.tp.typewriter("Already at the top-level folder.")
                    time.sleep(1)
                continue
            elif choice in ['d', 'del']:
                self.choose_removal()
                continue
            elif choice in ['a', 'add']:
                self.choose_addition()
                continue

            choice_normalized = choice.lower()
            match = [
                (p, s, m) for (p, s, m) in paths
                if os.path.basename(p).lower() == choice_normalized
            ]

            if match:
                target, _, _ = match[0]
                self.folder_history.append(self.folder)
                if os.path.isdir(target):
                    self.folder = target
                else:
                    self.folder = target
                    self.show_file_details()
                    if self.return_to_main:
                        return
                    if self.folder_history:
                        self.folder = self.folder_history.pop()
            else:
                self.tp.typewriter("Invalid selection.")
                time.sleep(1)

    def select_folder(self):
        directory = self.root
        while not self.kill_all:
            cc()
            self.return_to_main = False
            try:
                entries = os.listdir(directory)
            except Exception:
                self.tp.typewriter(f"Cannot access root folder '{directory}'. Exiting.")
                time.sleep(2)
                return

            files = [f for f in entries if os.path.isfile(os.path.join(directory, f))]
            folders = [f for f in entries if os.path.isdir(os.path.join(directory, f))]

            self.tp.typewriter("----------- Files -----------")
            for f in files:
                full_path = os.path.join(directory, f)
                breadcrumb = self.get_breadcrumb_path(full_path)
                self.tp.typewriter(f"File: {f}\n    - Location: {breadcrumb}")

            self.tp.typewriter("\n---------- Folders ----------")
            for folder in folders:
                path = os.path.join(directory, folder)
                total, file_count, dir_count = self.get_len_of_insides(path)
                self.tp.typewriter(
                    f"Folder: {folder.replace('_', ' ')}\n"
                    f"   - Location: {self.get_breadcrumb_path(path)}\n"
                    f"   - Items: {total} (Files: {file_count}, Folders: {dir_count})"
                )
            
            print()

            self.tp.typewriter(
                "Choose a file or folder to inspect."
                "\nType 'add' to add a file or folder."
                "\nType 'del' to delete a file or folder."
                "\nType 'quit' to exit."
            )
            choice = self.tp.inputTypewriter("Your option ").strip().lower()

            if choice in ['quit', 'q']:
                self.kill_all = True
                break

            elif choice in ['a', 'add']:
                self.choose_addition(directory)
                continue

            elif choice in ['d', 'del']:
                self.choose_removal(directory)
                continue

            target = os.path.join(directory, choice)
            if os.path.exists(target):
                self.folder = target
                self.folder_history.clear()
                self.display_folder_contents()
                if self.return_to_main:
                    continue
            else:
                self.tp.typewriter("Invalid selection.")
                time.sleep(1)

        cc()

if __name__ == '__main__':
    folder = get_folder_to_inspect()
    main = Main(root=folder)
    main.select_folder()
