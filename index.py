from math import frexp
import os
from select import select
import shutil
from xml.etree.ElementInclude import include
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter.simpledialog import askstring
import ctypes

myappid = 'codes.lucasjoel.BOTW Save Changer and Exporter for Cemu.1.0.0'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

path = open('./config.save', 'r').readline()

root = Tk()
root.title("BOTW Save Changer and Exporter for Cemu")
root.iconbitmap('./assets/logo.ico')
root.geometry("686x500")
root.resizable(False, True)

def error_message(message):
    messagebox.showerror("Error", message)

def success_message(message):
    messagebox.showinfo("Success", message)

def CREATE_SAVE(save_name):
    if os.path.exists('./saves/' + save_name):
        error_message("Save already exists")
        return
    os.mkdir('./saves/' + save_name)
    f = open('./saves/' + save_name + '/save.save', 'w')
    f.write(save_name)
    f.close()
    success_message("Save " + save_name + " created")

def LOAD_SAVE():
    save = filedialog.askdirectory(initialdir='./saves')
    print(save + '/save.save')
    if not save + '/save.save':
        error_message("Invalid save, no save.save file found")
        return
    f = open(save + '/save.save', 'r')
    save_name = f.readline()
    f.close()
    currentSaveFile = open(path + "\\mlc01\\usr\\save\\00050000\\101c9400\\user\\80000001\\save.save", 'r')
    currentSave = currentSaveFile.readline()
    for file in os.listdir(path + "\\mlc01\\usr\\save\\00050000\\101c9400\\user\\80000001"):
        if file != 'save.save':
            shutil.move(path + "\\mlc01\\usr\\save\\00050000\\101c9400\\user\\80000001\\" + file, './saves/' + currentSave)
    for file in os.listdir('./saves/' + save_name):
        if file != 'save.save':
            shutil.move('./saves/' + save_name + '/' + file, path + "\\mlc01\\usr\\save\\00050000\\101c9400\\user\\80000001")
    f = open(path + "\\mlc01\\usr\\save\\00050000\\101c9400\\user\\80000001\\save.save", 'w')
    f.write(save_name)
    f.close()
    success_message("Save " + save_name + " loaded")

def DUPLICATE_SAVE(duplicate_name):
    save = filedialog.askdirectory(initialdir='./saves')
    if not save + '/save.save':
        error_message("Invalid save, no save.save file found")
        return
    shutil.copytree(save, './saves/' + duplicate_name)
    f = open('./saves/' + duplicate_name + '/save.save', 'w')
    f.write(duplicate_name)
    f.close()
    success_message("Save " + duplicate_name + " created")

def DELETE_SAVE():
    save = filedialog.askdirectory(initialdir='./saves')
    if not save + '/save.save':
        error_message("Invalid save, no save.save file found")
        return
    # confirm delete
    save_name = open(save + '/save.save', 'r').readline()
    if messagebox.askokcancel("Delete Save", "Are you sure you want to delete " + save_name + "?"):
        shutil.rmtree(save)
        success_message("Save deleted")
        return
    success_message("Save not deleted")

def CHANGE_SAVE_NAME(save_name):
    save = filedialog.askdirectory(initialdir='./saves')
    if not save + '/save.save':
        error_message("Invalid save, no save.save file found")
        return
    f = open(save + '/save.save', 'r')
    old_name = f.readline()
    f.close()
    f = open(save + '/save.save', 'w')
    f.write(save_name)
    f.close()
    shutil.move(save, './saves/' + save_name)
    success_message("Save name changed from " + old_name + " to " + save_name)

def BACKUP_SAVE(backup_name):
    save = filedialog.askdirectory(initialdir='./saves')
    if not save + '/save.save':
        error_message("Invalid save, no save.save file found")
        return
    if backup_name == "":
        backup_name = open(save + '/save.save', 'r').readline()
    shutil.copytree(save, './backups/' + backup_name)
    i = 0
    for file in os.listdir('./backups'):
        if save in file:
            i += 1
    shutil.make_archive('./backups/' + backup_name, 'zip', './backups/' + backup_name)
    shutil.rmtree('./backups/' + backup_name)
    success_message("Save backed up")

def RESTORE_SAVE():
    save = filedialog.askopenfilename(initialdir='./backups', filetypes=[('Zip Files', '*.zip')])
    if not save:
        error_message("No backup selected")
        return
    backup_save_name = save.split('/')[-1].split('.')[0]
    shutil.unpack_archive(save, './backups/' + backup_save_name)
    if not os.path.exists('./backups/' + backup_save_name + '/save.save'):
        error_message("Invalid backup, no save.save file found")
        return
    f = open('./backups/' + backup_save_name + '/save.save', 'r')
    save_name = f.readline()
    f.close()
    shutil.rmtree('./saves/' + save_name)
    shutil.move('./backups/' + backup_save_name, './saves/')
    success_message("Save restored")

def EXPORT_SAVE():
    save = filedialog.askdirectory(initialdir='./saves', title="Select save to export")
    if not save + '/save.save':
        error_message("Invalid save, no save.save file found")
        return
    save_name = open(save + '/save.save', 'r').readline()
    export_location = filedialog.asksaveasfilename(initialdir='./saves', title="Select export location", initialfile=save_name)
    if messagebox.askokcancel("Export Save", "Are you sure you want to export " + save_name + "?"):
        shutil.make_archive(export_location, 'zip', save)
        success_message("Save exported")
        return
    success_message("Save not exported")

def IMPORT_SAVE():
    save = filedialog.askopenfilename(initialdir='./saves', filetypes=[('Zip Files', '*.zip')])
    if not save:
        error_message("No save selected")
        return
    save_name = save.split('/')[-1].split('.')[0]
    if messagebox.askokcancel("Import Save", "Are you sure you want to import " + save_name + "?"):
        shutil.unpack_archive(save, './saves/' + save_name)
        success_message("Save imported")
        return
    success_message("Save not imported")

if path == "" or not os.path.isdir(path):
    success_message("No cemu path found in config.save, please enter your cemu path")
    path = filedialog.askdirectory(initialdir='./saves')
    if path == "":
        error_message("No save path selected")
        exit()
    f = open('./config.save', 'w')
    f.write(path)
    f.close()
    
tabControl = ttk.Notebook(root)
tab_creat_save = ttk.Frame(tabControl)
tab_load_save = ttk.Frame(tabControl)
tab_duplicate_save = ttk.Frame(tabControl)
tab_delete_save = ttk.Frame(tabControl)
tab_change_save_name = ttk.Frame(tabControl)
tab_backup_save = ttk.Frame(tabControl)
tab_restore_save = ttk.Frame(tabControl)
tab_export_save = ttk.Frame(tabControl)
tab_import_save = ttk.Frame(tabControl)
tabControl.add(tab_creat_save, text="Create Save")
tabControl.add(tab_load_save, text="Load Save")
tabControl.add(tab_duplicate_save, text="Duplicate Save")
tabControl.add(tab_delete_save, text="Delete Save")
tabControl.add(tab_change_save_name, text="Change Save Name")
tabControl.add(tab_backup_save, text="Backup Save")
tabControl.add(tab_restore_save, text="Restore Save")
tabControl.add(tab_export_save, text="Export Save")
tabControl.add(tab_import_save, text="Import Save")
tabControl.pack(expand=1, fill="both")

# Create Save Tab
tab_label_creat_save = ttk.Label(tab_creat_save, text="Create Save", font=("Arial", 16))
tab_label_creat_save.pack(pady=10)
save_name_entry = ttk.Entry(tab_creat_save, width=50)
save_name_entry.insert(0, "Save Name")
save_name_entry.pack(pady=10)
ttk.Button(tab_creat_save, text="Create Save", command=lambda: CREATE_SAVE(str(save_name_entry.get()))).pack(pady=10)

# Load Save Tab
tab_label_load_save = ttk.Label(tab_load_save, text="Load Save", font=("Arial", 16))
tab_label_load_save.pack(pady=10)
ttk.Button(tab_load_save, text="Load Save", command=lambda: LOAD_SAVE()).pack(pady=10)

# Duplicate Save Tab
tab_label_duplicate_save = ttk.Label(tab_duplicate_save, text="Duplicate Save", font=("Arial", 16))
tab_label_duplicate_save.pack(pady=10)
duplicate_name_entry = ttk.Entry(tab_duplicate_save, width=50)
duplicate_name_entry.insert(0, "Duplicate Save Name")
duplicate_name_entry.pack(pady=10)
ttk.Button(tab_duplicate_save, text="Duplicate Save", command=lambda: DUPLICATE_SAVE(str(duplicate_name_entry.get()))).pack(pady=10)

# Delete Save Tab
tab_label_delete_save = ttk.Label(tab_delete_save, text="Delete Save", font=("Arial", 16))
tab_label_delete_save.pack(pady=10)
ttk.Button(tab_delete_save, text="Delete Save", command=lambda: DELETE_SAVE()).pack(pady=10)

# Change Save Name Tab
tab_label_change_save_name = ttk.Label(tab_change_save_name, text="Change Save Name", font=("Arial", 16))
tab_label_change_save_name.pack(pady=10)
save_name_entry = ttk.Entry(tab_change_save_name, width=50)
save_name_entry.insert(0, "Save Name")
save_name_entry.pack(pady=10)
ttk.Button(tab_change_save_name, text="Change Save Name", command=lambda: CHANGE_SAVE_NAME(str(save_name_entry.get()))).pack(pady=10)

# Backup Save Tab
tab_label_backup_save = ttk.Label(tab_backup_save, text="Backup Save", font=("Arial", 16))
tab_label_backup_save.pack(pady=10)
backup_name_entry = ttk.Entry(tab_backup_save, width=50)
backup_name_entry.insert(0, "Backup Save Name")
backup_name_entry.pack(pady=10)
ttk.Button(tab_backup_save, text="Backup Save", command=lambda: BACKUP_SAVE(str(backup_name_entry.get()))).pack(pady=10)

# Restore Save Tab
tab_label_restore_save = ttk.Label(tab_restore_save, text="Restore Save", font=("Arial", 16))
tab_label_restore_save.pack(pady=10)
ttk.Button(tab_restore_save, text="Restore Save", command=lambda: RESTORE_SAVE()).pack(pady=10)

# Export Save Tab
tab_label_export_save = ttk.Label(tab_export_save, text="Export Save", font=("Arial", 16))
tab_label_export_save.pack(pady=10)
ttk.Button(tab_export_save, text="Export Save", command=lambda: EXPORT_SAVE()).pack(pady=10)

# Import Save Tab
tab_label_import_save = ttk.Label(tab_import_save, text="Import Save", font=("Arial", 16))
tab_label_import_save.pack(pady=10)
ttk.Button(tab_import_save, text="Import Save", command=lambda: IMPORT_SAVE()).pack(pady=10)

root.mainloop()