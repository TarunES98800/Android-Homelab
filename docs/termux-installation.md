# Installing and Setting Up Termux on Android

## 1. Introduction

Termux is an Android application that provides a terminal emulator and a Linux-like command-line environment.

It allows users to install compatible software packages, run command-line tools, write scripts and execute programs directly on an Android smartphone.

In this project, Termux will act as the foundation of our Android homelab. We will use it to install and manage the software required by different server applications.

Some examples include:

- Java for running Java-based applications.
- Python for scripting and compatible web applications.
- Git for downloading and managing source code.
- Networking utilities for testing connections.
- tmux for managing long-running terminal sessions.

**Important:** Termux does not replace Android with a full Linux operating system. It runs within Android and provides its own user-space environment.

## 2. Requirements

Before installing Termux, make sure you have:

- An Android smartphone.
- Android 7 or later for the currently supported Termux app and package environment.
- A working internet connection.
- Sufficient free storage space.
- Permission to install applications from the selected installation source.

The device used in the initial implementation of this project is a Redmi Note 8 Pro running Android 11.

## 3. Downloading Termux

Termux should be downloaded from a trusted distribution source.

For this tutorial, we use F-Droid.

### Why use F-Droid?

F-Droid is a repository for free and open-source Android applications. It provides a distribution channel for Termux.

The Termux project also publishes releases through its official GitHub repository.

**Official download links:**

- [Termux on F-Droid](https://f-droid.org/packages/com.termux/)
- [Official Termux GitHub repository](https://github.com/termux/termux-app)

Avoid downloading Termux APK files from unknown websites or unofficial file-sharing sources.

### Installing Termux through F-Droid

1. Open the official [F-Droid website](https://f-droid.org/).
2. Download and install the F-Droid application if it is not already installed.
3. Open F-Droid.
4. Allow it to load and refresh its application repository.
5. Search for **Termux**.
6. Open the Termux application listing.
7. Select Install.
8. Allow Android to install the application if it asks for permission.

Once installation is complete, Termux should appear in your Android application list.

### Important: Do not mix installation sources

Termux and its optional add-ons must be installed from the same distribution source.

For example, do not install the main Termux app through F-Droid and then install a Termux add-on from a different source.

Different distribution sources can sign their APK files with different signing keys. Mixing them can cause installation and update errors.

If you ever need to change distribution sources, first understand the backup and reinstallation procedure. Uninstalling Termux can delete the files stored in its private application directory.

For this project, we will continue using the F-Droid distribution.

## 4. First Launch of Termux

Open Termux after installation.

The first launch may take some time because Termux needs to prepare its initial environment.

Once initialization is complete, you should see a terminal window.

A terminal is a text-based interface where users enter commands to interact with the system.

Instead of selecting buttons and menus, we type instructions and receive text output.

You will usually see a prompt similar to:

```text
$
```

The exact appearance may vary depending on the Termux version and terminal configuration.

The `$` symbol indicates that the shell is ready to receive a command.

## 5. Understanding the Shell

Termux provides a shell, which is a program that interprets commands entered by the user.

The default shell is generally Bash.

For example, enter:

```bash
pwd
```

The command prints the current working directory.

In a new Termux installation, this should normally point to the Termux user's home directory.

Now enter:

```bash
whoami
```

This displays the username or Android-assigned application identity under which the shell is running.

Unlike a conventional Linux server, a normal Termux installation does not give us root privileges.

We can therefore manage files and processes within the permissions granted to the Termux application, but we cannot freely control Android's entire operating system.

## 6. Updating Termux Packages

Before installing additional software, we should update the package information and upgrade the installed packages.

Termux includes a package manager called `pkg`.

A package manager downloads, installs, updates and removes software packages.

### Step 1: Update package information

Run:

```bash
pkg update
```

This checks the configured package repositories and downloads the latest available package information.

### Step 2: Upgrade installed packages

After the update finishes, run:

```bash
pkg upgrade
```

This upgrades installed packages when newer versions are available.

Termux may ask for confirmation during the process.

Read the prompt and enter:

```text
y
```

when you are ready to continue.

The process may take some time depending on your internet connection and the number of updates.

### Understanding the commands

| Command | Purpose |
|---|---|
| `pkg` | Termux package-management command |
| `update` | Refresh package repository information |
| `upgrade` | Upgrade installed packages |

Updating packages regularly is important because software improvements, compatibility updates and security fixes may be distributed through package repositories.

If package repositories are unavailable or report an error, consult the official [Termux package-management documentation](https://github.com/termux/termux-packages/wiki/Package-Management) before changing repository settings.

## 7. Understanding Termux Storage

By default, Termux has access to its own private application storage.

This is where we should normally install software and keep server-related files.

Termux can also request permission to access shared Android storage, such as the Downloads and Pictures directories.

This is useful when transferring files between Termux and other Android applications.

### Granting shared storage access

If you need Termux to access shared storage, execute:

```bash
termux-setup-storage
```

Android will display a permission prompt.

Review the requested permission and grant it if you want to use this feature.

After permission is granted, Termux creates convenient directory links under:

```text
~/storage/
```

Some examples include:

| Directory | Purpose |
|---|---|
| `~/storage/shared` | Shared internal storage |
| `~/storage/downloads` | Downloads directory |
| `~/storage/dcim` | Camera photos and videos |
| `~/storage/pictures` | Pictures directory |
| `~/storage/movies` | Movies directory |

### Where should server files be stored?

For this project, we will generally keep server applications and their data inside Termux's private home directory.

For example:

```text
$HOME/
└── minecraft/
    ├── paper.jar
    ├── server.properties
    └── world/
```

This avoids many limitations associated with Android shared storage, including restrictions on file permissions and executing programs.

**Important:** Termux's private files are tied to the application's data. Uninstalling Termux can delete this data. Always back up important server files before uninstalling or changing the installation source.

Storage access is optional for the initial setup. You can skip `termux-setup-storage` if you do not need to access shared Android files.

## 8. Verifying the Installation

After updating Termux, we should confirm that the environment is working correctly.

Run the following commands individually.

### Check the current directory

```bash
pwd
```

This should display the current working directory.

### Check processor architecture

```bash
uname -m
```

This displays the processor architecture reported by the environment.

Common outputs include:

- `aarch64`
- `armv7l`
- `x86_64`
- `i686`

The output depends on the device.

### Check available storage

```bash
df -h "$HOME"
```

This displays filesystem storage information in a human-readable format.

Pay attention to the available space.

### Check Termux environment information

```bash
termux-info
```

This displays information about the Termux installation and environment.

Together, these commands help us confirm that Termux is installed and functioning.

## 9. Important Android Settings for Long-Running Services

Android is designed primarily for mobile applications, not continuous server workloads.

Depending on the smartphone manufacturer, Android may restrict background applications to reduce battery consumption.

When we begin hosting long-running services, these restrictions may interrupt server processes.

Before using a phone as a continuously running server, check its application battery settings.

On some devices, you may be able to select a setting such as:

- No restrictions
- Allow background activity
- Don't optimize battery usage

The exact wording and availability depend on the Android version and manufacturer.

For the initial installation, no special background setting is required. We will configure and test these settings when setting up long-running applications.

## 10. Common Problems

### Problem 1: Termux cannot download packages

Possible causes:

- No internet connection.
- Package repositories temporarily unavailable.
- Incorrect repository configuration.

First, verify that the phone has an internet connection.

If the issue continues, consult the official [Termux package-management guide](https://github.com/termux/termux-packages/wiki/Package-Management).

### Problem 2: Android refuses to install the APK

Possible causes:

- Android has not granted permission to install applications from the selected source.
- The APK is incompatible with the Android version.
- Another Termux installation from a different source is already present.

Only download APKs from the official sources listed in this tutorial. Do not uninstall an existing Termux installation without backing up important data.

### Problem 3: Termux closes unexpectedly

Possible causes include:

- Android background restrictions.
- Battery optimization.
- Device memory pressure.
- Excessive CPU usage or overheating.

Check the device's battery and application settings before assuming Termux itself is broken.

### Problem 4: Storage permission does not work

Run:

```bash
termux-setup-storage
```

Then review the Android permission prompt.

If permission was denied previously, check Termux's application permissions in Android Settings.

## 11. Conclusion

Termux provides the foundation for running compatible command-line software on Android.

In this chapter, we:

1. Installed Termux through F-Droid.
2. Opened the terminal environment.
3. Learned what the shell does.
4. Updated the package repositories and installed packages.
5. Learned about private and shared storage.
6. Verified the installation using basic commands.
7. Discussed Android background restrictions.

Our Android smartphone is now ready for the next stage of the homelab setup.

In the following chapter, we will explore essential Linux commands and learn how to navigate the Termux filesystem, manage directories and work with files.

## 12. References

- [Official Termux GitHub repository](https://github.com/termux/termux-app)
- [Termux on F-Droid](https://f-droid.org/packages/com.termux/)
- [Termux package-management documentation](https://github.com/termux/termux-packages/wiki/Package-Management)
