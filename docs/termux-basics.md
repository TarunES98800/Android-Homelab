# Linux Command-Line Fundamentals in Termux

## 1. Introduction

After installing Termux, the next step is learning how to use its command-line environment.

A command-line interface (CLI) allows users to interact with a computer by entering text commands instead of using graphical buttons and menus.

Linux systems commonly use the command line for:

- Managing files and directories.
- Installing and updating software.
- Running applications.
- Managing processes.
- Checking storage and system information.
- Automating repetitive tasks.

Since our Android homelab will use Termux to manage server applications, understanding these commands is essential.

This tutorial introduces commonly used commands with practical examples.

**Note:** Termux provides a Linux-like user-space environment inside Android. Some commands and system-management features may behave differently from those on a conventional Linux distribution.

## 2. Understanding the Terminal and Shell

When we open Termux, we see a terminal window.

The terminal is the interface through which we enter commands and view their output.

A shell is the program that interprets these commands and executes them.

Termux generally uses Bash as its default shell.

For example, a terminal prompt may look like:

```text
$
```

This indicates that the shell is ready to accept a command.

When a tutorial displays a command like:

```bash
pwd
```

Enter only `pwd` in Termux. Do not type the `$` prompt or the Markdown code-block formatting.

## 3. Understanding the Filesystem

A filesystem is the way an operating system organizes and stores files and directories.

In Linux-like environments, directories are organized in a hierarchical structure.

The top of this structure is called the root directory, represented by:

```text
/
```

Inside Termux, we normally work in our application-specific home directory.

The following command displays its location:

```bash
pwd
```

`pwd` stands for **Print Working Directory**.

A typical Termux home directory looks like:

```text
/data/data/com.termux/files/home
```

The exact environment path can depend on the application package and installation.

### Understanding the home directory

The home directory is represented by:

```bash
~
```

The environment variable `$HOME` also contains the path to this directory.

For example:

```bash
echo $HOME
```

This displays the home directory path.

Both of the following commands change to the home directory:

```bash
cd ~
```

```bash
cd $HOME
```

For our homelab, we will generally store application files and server data inside this private Termux home directory.

## 4. Navigating Directories

The `cd` command changes the current working directory.

Its name stands for **Change Directory**.

### Example 1: Move to the home directory

```bash
cd ~
```

### Example 2: Move into a directory

```bash
cd minecraft
```

This works when a directory called `minecraft` exists inside the current directory.

### Example 3: Move one level up

```bash
cd ..
```

The `..` notation represents the parent directory.

### Example 4: Return to the previous directory

```bash
cd -
```

This switches to the previous working directory.

### Example 5: Return home

```bash
cd
```

Running `cd` without a directory normally returns the shell to its home directory.

### Verify your location

After changing directories, execute:

```bash
pwd
```

This confirms where you are currently working.

## 5. Listing Files and Directories

The `ls` command displays the files and directories in a location.

### Basic usage

```bash
ls
```

This displays the contents of the current directory.

### Show hidden files

```bash
ls -a
```

Linux filenames beginning with a dot are treated as hidden by convention.

The `-a` option displays these files as well.

### Detailed listing

```bash
ls -l
```

This displays additional information such as permissions, ownership, file size and modification time.

### Combine options

```bash
ls -la
```

This displays a detailed listing, including hidden files.

### List another directory

```bash
ls ~/storage
```

This attempts to display the contents of the `storage` directory inside the home directory.

Remember that the directory must exist and the necessary storage setup must already have been completed.

## 6. Creating Directories

The `mkdir` command creates a new directory.

`mkdir` stands for **Make Directory**.

### Example 1: Create a directory

```bash
mkdir homelab
```

This creates a directory called `homelab` in the current working directory.

### Example 2: Create multiple directories

```bash
mkdir minecraft fileserver webserver
```

This creates three directories.

### Example 3: Create nested directories

```bash
mkdir -p homelab/applications/minecraft
```

The `-p` option creates any missing parent directories as needed.

This is particularly useful when organizing our server applications.

After executing the command, the directory structure will look like:

```text
homelab/
└── applications/
    └── minecraft/
```

### Verify the directory

```bash
ls
```

If you have the `tree` utility installed, you can also use:

```bash
tree homelab
```

This displays the directory structure in a tree-like format.

If `tree` is unavailable, install it using:

```bash
pkg install tree
```

## 7. Creating Files

The `touch` command creates an empty file if it does not already exist.

### Example

```bash
touch notes.txt
```

This creates an empty file named `notes.txt`.

You can create multiple files at once:

```bash
touch file1.txt file2.txt file3.txt
```

**Important:** If a file already exists, `touch` normally updates its modification timestamp rather than deleting its contents.

## 8. Reading File Contents

Linux provides several commands for displaying file contents.

### Using cat

```bash
cat notes.txt
```

`cat` displays the contents of a file in the terminal.

It can also display multiple files one after another:

```bash
cat file1.txt file2.txt
```

### Display the beginning of a file

```bash
head notes.txt
```

By default, `head` displays the first 10 lines.

To display the first five lines:

```bash
head -n 5 notes.txt
```

### Display the end of a file

```bash
tail notes.txt
```

By default, `tail` displays the last 10 lines.

To display the last five lines:

```bash
tail -n 5 notes.txt
```

These commands are particularly useful when inspecting server logs.

For example, when troubleshooting an application, we may want to examine the most recent error messages rather than reading an entire log file.

## 9. Copying Files and Directories

The `cp` command copies files and directories.

### Example 1: Copy a file

```bash
cp notes.txt backup.txt
```

This creates a copy of `notes.txt` named `backup.txt`.

### Example 2: Copy a file into another directory

```bash
cp notes.txt homelab/
```

This copies `notes.txt` into the `homelab` directory.

### Example 3: Copy a directory

```bash
cp -r minecraft minecraft-backup
```

The `-r` option means recursive.

It allows `cp` to copy a directory and its contents, including nested directories.

This operation can be useful when creating a basic copy of application data.

However, for a live server, copying files while they are being modified can produce an inconsistent backup. We will cover proper backup procedures in a dedicated chapter.

## 10. Moving and Renaming Files

The `mv` command moves files or directories and can also rename them.

### Example 1: Rename a file

```bash
mv notes.txt project-notes.txt
```

This renames `notes.txt` to `project-notes.txt`.

### Example 2: Move a file

```bash
mv project-notes.txt homelab/
```

This moves the file into the `homelab` directory.

### Example 3: Rename a directory

```bash
mv minecraft minecraft-server
```

This renames the directory.

Unlike `cp`, the `mv` command does not create a second copy of the original file when it moves it.

## 11. Removing Files and Directories

The `rm` command removes files and directories.

Because deletion can cause permanent data loss, always verify the target before executing a removal command.

### Example 1: Remove a file

```bash
rm notes.txt
```

This removes the file named `notes.txt`.

### Example 2: Ask before removing

```bash
rm -i notes.txt
```

The `-i` option asks for confirmation before removing the file.

### Example 3: Remove an empty directory

```bash
rmdir empty-folder
```

`rmdir` removes an empty directory.

### Example 4: Remove a directory and its contents

```bash
rm -r old-folder
```

The `-r` option recursively removes a directory and the files inside it.

**Security and data-loss warning:**

- Be especially careful when using `rm -r`.
- Verify the current directory and the target path.
- Do not experiment with `rm -rf` on important server directories.
- Keep backups of important application data.

For beginners, using `rm -i` is a safer way to learn file removal.

## 12. Editing Files Using Nano

`nano` is a terminal-based text editor.

It allows users to create and edit configuration files directly from Termux.

Install it if it is not already available:

```bash
pkg install nano
```

### Open or create a file

```bash
nano notes.txt
```

This opens the file in the Nano editor.

If the file does not exist, Nano creates it when the changes are saved.

### Useful Nano shortcuts

| Shortcut | Function |
|---|---|
| `Ctrl + O` | Save the file |
| `Enter` | Confirm the filename |
| `Ctrl + X` | Exit Nano |
| `Ctrl + W` | Search inside the file |
| `Ctrl + K` | Cut the current line |
| `Ctrl + U` | Paste a previously cut line |

On a phone, the Ctrl key may be available through Termux's extra keys row or keyboard settings.

For example, to save and exit:

1. Press `Ctrl + O`.
2. Press `Enter` to confirm.
3. Press `Ctrl + X`.

Nano is especially useful when editing configuration files such as `server.properties`.

## 13. Searching for Files

The `find` command searches for files and directories.

### Example 1: Find a file by name

```bash
find ~ -name "notes.txt"
```

This searches the Termux home directory and its subdirectories for a file named `notes.txt`.

### Example 2: Find directories by name

```bash
find ~ -type d -name "minecraft"
```

The `-type d` option restricts the results to directories.

### Example 3: Find files with a particular extension

```bash
find ~ -type f -name "*.txt"
```

This finds files ending in `.txt`.

The `-type f` option restricts the results to regular files.

## 14. Searching Within Files Using Grep

The `grep` command searches for text patterns inside files.

### Example

```bash
grep "error" notes.txt
```

This displays lines containing the word `error`.

### Ignore uppercase and lowercase differences

```bash
grep -i "error" notes.txt
```

The `-i` option performs a case-insensitive search.

### Display matching line numbers

```bash
grep -n "error" notes.txt
```

The `-n` option displays the line number for every matching result.

Grep is useful when searching application configuration files and logs.

For example:

```bash
grep -n "server-port" server.properties
```

This searches for a configuration entry containing `server-port`.

## 15. Understanding File Permissions

Linux-like environments use file permissions to control which users can read, write or execute files.

The `ls -l` command displays permission information.

For example:

```text
-rw-r--r--  1 u0_a123 u0_a123  1200 Nov 21 10:00 notes.txt
```

The first characters represent file type and permissions.

Common permission symbols include:

| Symbol | Meaning |
|---|---|
| `r` | Read |
| `w` | Write |
| `x` | Execute |
| `-` | Permission not granted |

The permissions are displayed in groups for the file owner, group and other users.

### Changing file permissions

The `chmod` command changes file permissions.

For example:

```bash
chmod +x script.sh
```

This adds execute permission for the applicable user classes according to the command's default behaviour.

It is often used when preparing shell scripts for execution.

**Important:** Android and Termux permissions are not identical to a traditional Linux server's permission model. The application also operates within Android's security restrictions.

## 16. Checking Storage Usage

Storage management becomes important when hosting applications that generate files, databases, logs and backups.

### Check filesystem storage

```bash
df -h
```

This displays filesystem capacity and available space in human-readable units.

To check the filesystem containing the Termux home directory:

```bash
df -h "$HOME"
```

### Check directory size

```bash
du -sh ~/minecraft
```

This displays the total size of the `minecraft` directory.

### Check individual directories

```bash
du -h --max-depth=1 ~
```

This displays the sizes of directories directly inside the home directory on systems supporting this `du` option.

The `-s` option summarizes a directory's total size, while `-h` makes the output easier to read.

## 17. Installing Packages with the Termux Package Manager

Termux provides a package-management command called `pkg`.

It makes installing and updating software easier.

### Install Nano

```bash
pkg install nano
```

### Install Git

```bash
pkg install git
```

### Install Python

```bash
pkg install python
```

### Search for a package

```bash
pkg search python
```

### Remove a package

```bash
pkg uninstall python
```

The exact packages available depend on the configured Termux repositories.

Always review package installation and removal prompts before confirming.

## 18. Combining Commands

The shell allows us to combine commands.

For example:

```bash
mkdir homelab && cd homelab
```

The `&&` operator runs the second command only when the first command succeeds.

This means:

1. Create the `homelab` directory.
2. Change into it if the directory was created successfully.

Another example:

```bash
pwd && ls
```

This prints the current directory and then lists its contents.

### Understanding command separators

| Operator | Meaning |
|---|---|
| `&&` | Run the next command if the previous command succeeds |
| `;` | Run the next command regardless of the previous command's success |
| `\|` | Pass the output of one command as input to another |

Example using a pipe:

```bash
ls -l | grep ".txt"
```

This sends the output of `ls -l` to `grep`, which searches it for `.txt`.

## 19. Practical Exercise: Create Your First Homelab Directory

Now that we understand the basic commands, let's apply them.

We will create a directory structure that can later hold our server applications.

### Step 1: Return to the home directory

```bash
cd ~
```

### Step 2: Create the main directory

```bash
mkdir homelab
```

### Step 3: Enter the directory

```bash
cd homelab
```

### Step 4: Create application directories

```bash
mkdir minecraft file-server web-server
```

### Step 5: Create a documentation directory

```bash
mkdir docs
```

### Step 6: Verify the structure

```bash
ls -la
```

If `tree` is installed, execute:

```bash
tree ~/homelab
```

The expected structure is:

```text
homelab/
├── minecraft/
├── file-server/
├── web-server/
└── docs/
```

Congratulations! You have created a basic directory structure for your future homelab services.

## 20. Important Notes for Android Homelab Users

### Always check your current directory

Before creating, moving or removing files, use:

```bash
pwd
```

This helps prevent accidentally working in the wrong location.

### Understand where your files are stored

Termux's private home directory is different from shared Android storage.

For server applications, we generally prefer the private home directory.

### Do not execute commands blindly

Understand the command and its target before executing it.

This is particularly important for commands that delete files, change permissions or modify server configurations.

### Termux shell versus application console

When a server application is running, it may provide its own console.

For example, a Minecraft server console accepts commands such as:

```text
list
```

However, commands such as:

```bash
pwd
ls
mkdir
```

belong to the Termux shell, not the Minecraft server console.

Understanding this distinction prevents many common mistakes.

## 21. Conclusion

In this chapter, we learned how to interact with the Termux command-line environment.

We covered:

- Understanding the terminal and shell.
- Navigating directories using `cd`.
- Listing files using `ls`.
- Creating files and directories.
- Reading and editing files.
- Copying, moving and removing files.
- Searching with `find` and `grep`.
- Understanding file permissions.
- Checking storage usage.
- Installing packages.
- Combining commands.
- Creating a practical homelab directory structure.

These commands form the foundation for managing applications in our Android homelab.

In the next chapter, we will explore networking fundamentals, including IP addresses, ports, TCP connections, local networks and how other devices communicate with our Android server.

## 22. References

- [Termux Official GitHub Repository](https://github.com/termux/termux-app)
- [GNU Coreutils Manual](https://www.gnu.org/software/coreutils/manual/coreutils.html)
- [GNU Findutils Manual](https://www.gnu.org/software/findutils/manual/html_mono/find.html)
- [GNU Grep Manual](https://www.gnu.org/software/grep/manual/grep.html)
- [GNU Nano Documentation](https://www.nano-editor.org/docs.php)
