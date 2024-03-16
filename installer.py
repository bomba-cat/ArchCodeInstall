#Imports
import tkinter as ntk
from tkinter import ttk as tk
from ttkthemes import ThemedTk
import os as linux

#GET FREE SPACE FOR INSTALLATION
linux.system("mount -o remount,size=8G /run/archiso/cowspace")

#Create window class
installer = ThemedTk(theme="breeze")

#Variables
user = ""
passw = ""
sudo = False
hostname = ""

kernel = ""

drivevar = ntk.StringVar(installer, "")
drive = ""

timezone = ""

#Commands
packages = [
    "parted"
]

commands = (
    "timedatectl",

    #Print drive for debugging
    "echo chosen drive: DRIVE",
    "read test"

    "mkdir /mnt/boot",
    #Setup partitions for arch linux: EFI, SWAP and ROOT using ext4 fs
    "parted /dev/DRIVE mklabel gpt",
    "parted /dev/DRIVE mkpart primary fat32 1MiB 300MiB",
    "parted /dev/DRIVE set 1 boot on",
    "parted /dev/DRIVE mkpart primary linux-swap 300MiB 4GiB",
    "parted /dev/DRIVE mkpart primary ext4 4GiB 100%",

    "read test"

    #Format partitions
    "mkfs.fat -F32 /dev/DRIVE1",
    "mkswap /dev/DRIVE2",
    "swapon /dev/DRIVE2",
    "mkfs.ext4 /dev/DRIVE3,"
    "mount /dev/DRIVE3 /mnt",
    "mkdir /mnt/boot",
    "mount /dev/DRIVE1 /mnt/boot",

    #Pacstrap
    "pacstrap -K /mnt base linux linux-firmware",
    "genfstab -U /mnt >> /mnt/etc/fstab",

    #Chroot
    "arch-chroot /mnt",

    #Set timezone
    "ln -sf /usr/share/zoneinfo/TIMEZONE /etc/localtime",
    "hwclock --systohc",

    #Set locales

    "echo 'LANG=en_US.UTF-8' > /etc/locale.conf",
    "echo 'en_US.UTF-8 UTF-8' > /etc/locale.gen",
    "locale-gen",

    #Set hostname
    "echo 'HOST' > /etc/hostname",

    #Set passwd for root
    "echo 'root:PASSWORD' | chpasswd",

    #Set user
    "useradd -m USER",
    "echo 'USER:PASSWORD' | chpasswd",
    "usermod -aG wheel USER",
    "echo 'USER ALL=(ALL:ALL) ALL' >> /etc/sudoers",

    #Install grub and efibootmgr
    "pacman -Sy grub efibootmgr --noconfirm",

    #Bootloader
    "grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB",
    "grub-mkconfig -o /boot/grub/grub.cfg"
)

postpackages = [
    #Environment stuff
    "plasma-meta",
    "plasma-desktop",
    "dolphin",

    #Editor stuff
    "vim",
    "neovim",
    "nano",
    "code",

    #Coding stuff
    "nasm",
    "gcc",
    "make",
    "cmake",
    "openjdk",
    "python",
    "python-pip",
    "python-numpy",
    "python3",
    "python3-pip",
    "python3-numpy",
    "nodejs",
    "nodejs-npm",
    "cargo",
    "mariadb",
    "mysql",
    "curl",
    "git",

    #Internet stuff
    "firefox",

    #Terminal stuff
    "kitty",
    "zsh"
]

basepackages = []

#open file
with open("packages.x86_64", "r") as f:
    basepack = f.readlines()
    for i in basepack:
        basepackages.append(i.strip())

postcommands = [
    "sudo pacman -Syu",
    "sudo pacman -S --needed base-devel git",
    "git clone https://aur.archlinux.org/yay.git",
    "cd yay",
    "makepkg -si",
    "cd ..",
    "rm -rf yay"
]

def sudoCheck():
    global sudo
    if sudo == True:
        sudo = False
    else:
        sudo = True

#Get user and password
def GetUserPass():
    global user, passw, sudo, hostname
    for widget in installer.winfo_children():               #Clear all widgets
        widget.destroy()
    user = ntk.StringVar()
    passw = ntk.StringVar()
    tk.Label(installer, text="Set Hostname", font=("Courier New", 40)).place(relx=0.5, rely=0.1, anchor="center")
    tk.Entry(installer, textvariable=hostname, font=("Courier New", 20)).place(relx=0.5, rely=0.2, anchor="center")

    tk.Label(installer, text="Create user", font=("Courier New", 40)).place(relx=0.5, rely=0.3, anchor="center")
    tk.Label(installer, text="Enter username:", font=("Courier New", 20)).place(relx=0.5, rely=0.4, anchor="center")
    tk.Entry(installer, textvariable=user, font=("Courier New", 20)).place(relx=0.5, rely=0.5, anchor="center")
    tk.Label(installer, text="Enter password:", font=("Courier New", 20)).place(relx=0.5, rely=0.6, anchor="center")
    tk.Entry(installer, textvariable=passw, show="*", font=("Courier New", 20)).place(relx=0.5, rely=0.7, anchor="center")
    tk.Checkbutton(installer, text="Root", command=sudoCheck).place(relx=0.5, rely=0.8, anchor="center")
    tk.Button(installer, text="Next", command=GetKernel).place(relx=0.5, rely=0.9, anchor="center")

def GetKernel():
    global kernel
    for widget in installer.winfo_children():               #Clear all widgets
        widget.destroy()
    tk.Label(installer, text="Select kernel", font=("Courier New", 40)).place(relx=0.5, rely=0.1, anchor="center")
    tk.Button(installer, text="Linux (Recommended)", command=lambda: GetDrives("linux")).place(relx=0.5, rely=0.2, anchor="center")
    tk.Button(installer, text="Linux-LTS", command=lambda: GetDrives("linux-lts")).place(relx=0.5, rely=0.3, anchor="center")
    tk.Button(installer, text="Linux-Zen", command=lambda: GetDrives("linux-zen")).place(relx=0.5, rely=0.4, anchor="center")
    tk.Label(installer, text="Not sure what to pick?", font=("Courier New", 20)).place(relx=0.5, rely=0.5, anchor="center")
    tk.Label(installer, text="Linux - Latest linux kernel", font=("Courier New", 10)).place(relx=0.5, rely=0.6, anchor="center")
    tk.Label(installer, text="Linux LTS - Long Term Support kernel", font=("Courier New", 10)).place(relx=0.5, rely=0.7, anchor="center")
    tk.Label(installer, text="Linux Zen - Hacker tested kernel", font=("Courier New", 10)).place(relx=0.5, rely=0.8, anchor="center")

def GetDrives(chosenKernel):
    global kernel, drive, drivevar
    kernel = chosenKernel
    drives = linux.popen("lsblk --nodeps --output NAME | grep -v 'NAME'").read()
    for widget in installer.winfo_children():               #Clear all widgets
        widget.destroy()
    drives = drives.split("\n")

    tk.Label(installer, text="Select drive, WARNING: ALL DATA ON DRIVE WILL BE LOST", font=("Courier New", 20)).place(relx=0.5, rely=0.1, anchor="center")
    tk.Label(installer, text="Drives:", font=("Courier New", 20)).place(relx=0.5, rely=0.2, anchor="center")

    for d in drives:
        if d != "":
            tk.Radiobutton(installer, text=d, value=d, variable=drivevar).place(relx=0.5, rely=0.3+(drives.index(d)*0.1), anchor="center")

    tk.Button(installer, text="Next", command=setdrive).place(relx=0.5, rely=0.7, anchor="center")

def GetLocales():
    global timezone
    for widget in installer.winfo_children():               #Clear all widgets
        widget.destroy()
    tk.Label(installer, text="Locales", font=("Courier New", 40)).place(relx=0.5, rely=0.1, anchor="center")
    tk.Entry(installer, textvariable=timezone, font=("Courier New", 20)).place(relx=0.5, rely=0.3, anchor="center")
    tk.Button(installer, text="Next", command=Installing).place(relx=0.5, rely=0.7, anchor="center")

def setdrive():
    global drivevar, drive
    drive = drivevar.get()
    if "nvme" in drive:
        drive = f"{drive}p"
        print(drive)
    else:
        print(drive)
    GetLocales()

def Installing():
    global commands, packages, postcommands, postpackages, user, passw, sudo, hostname, drive, timezone, kernel
    #Label saying installing
    tk.Label(installer, text="Installing", font=("Courier New", 20)).place(relx=0.5, rely=0.5, anchor="center")

    #Label saying installing packages
    for widget in installer.winfo_children():               #Clear all widgets
        widget.destroy()
    tk.Label(installer, text="Installing packages", font=("Courier New", 20)).place(relx=0.5, rely=0.6, anchor="center")
    for i in packages:
        linux.system(f"pacman -Sy {i} --noconfirm")

    #Label saying installing commands
    for widget in installer.winfo_children():               #Clear all widgets
        widget.destroy()
    tk.Label(installer, text="Installing commands", font=("Courier New", 20)).place(relx=0.5, rely=0.6, anchor="center")
    for i in commands:
        linux.system(i.replace("USER", user).replace("PASSWORD", passw.get()).replace("HOST", hostname.get()).replace("DRIVE", drive.get()).replace("TIMEZONE", timezone.get()).replace("KERNEL", kernel.get()))

    #Label saying installing basepackages
    for widget in installer.winfo_children():               #Clear all widgets
        widget.destroy()
    tk.Label(installer, text="Installing basepackages", font=("Courier New", 20)).place(relx=0.5, rely=0.6, anchor="center")
    linux.system("pacman -Syu")
    for i in basepackages:
        linux.system(f"pacman -S {i} --noconfirm")

    #Label saying installing postpackages
    for widget in installer.winfo_children():               #Clear all widgets
        widget.destroy()
    tk.Label(installer, text="Installing postpackages", font=("Courier New", 20)).place(relx=0.5, rely=0.6, anchor="center")
    for i in postpackages:
        linux.system(f"pacman -S {i} --noconfirm")

    #Label saying executing postcommands
    tk.Label(installer, text="Executing postcommands", font=("Courier New", 20)).place(relx=0.5, rely=0.6, anchor="center")
    for i in postcommands:
        linux.system(i)

    for widget in installer.winfo_children():               #Clear all widgets
        widget.destroy()
    tk.Label(installer, text="Installation complete", font=("Courier New", 20)).place(relx=0.5, rely=0.5, anchor="center")
    tk.Button(installer, text="Reboot", command=installer.destroy).place(relx=0.5, rely=0.6, anchor="center")


#Welcome
def Welcome():
                                                            #Create a Welcome frame
    installer.wm_title("Welcome")
    tk.Label(installer, text="Welcome to the ArchCode installer", font=("Courier New", 20)).place(relx=0.5, rely=0.5, anchor="center")
    tk.Button(installer, text="Next", command=GetUserPass).place(relx=0.5, rely=0.6, anchor="center")

#Execute all functions
Welcome()

#Window settings
installer.resizable(width=False, height=False)
installer.title("Installer")
installer.geometry("1100x650")
installer.mainloop()
