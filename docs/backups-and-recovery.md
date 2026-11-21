# Backups and Recovery for an Android Homelab

## 1. Introduction

A homelab server stores important information such as application data, configuration files, databases and user-generated content.

If this information is accidentally deleted or corrupted, recovering it without a backup can be difficult.

For example, imagine that our Android smartphone is hosting a Minecraft server and several friends have been playing on the same world for weeks.

If the world directory is accidentally deleted or the phone develops a storage problem, all that progress could be lost.

This is why backups are an essential part of server administration.

In this chapter, we will learn:

- What backups are and why they matter.
- Which files should be backed up.
- How to create compressed backups using Termux.
- How to back up a Minecraft server.
- How to restore data from an archive.
- How to protect backups from device failure.
- How backup strategies apply to other server applications.

## 2. What Is a Backup?

A backup is a separate copy of important data that can be used to recover information when the original data is lost, damaged or unavailable.

Backups are commonly used to protect against:

- Accidental deletion.
- Hardware failure.
- Software corruption.
- Failed application updates.
- Incorrect configuration changes.
- Device loss or damage.
- Malware and unauthorized modifications.

For an Android homelab, backups allow us to recover the information stored by our hosted applications.

### Backup vs Original Data

Consider this example:

```text
Android Homelab
│
├── minecraft/
│   ├── world/
│   ├── server.properties
│   ├── whitelist.json
│   └── paper.jar
│
└── backups/
    └── minecraft-backup.tar.gz
```

The `minecraft` directory contains the original server files.

The archive inside `backups` contains a separate copy of those files.

If something happens to the original server directory, we can use the archive to restore it.

However, storing both copies on the same phone does not protect against the phone itself being lost or damaged.

We will discuss off-device backups later in this chapter.

## 3. What Should We Back Up?

The files that need to be backed up depend on the application.

For our Minecraft server, the safest beginner-friendly approach is to back up the complete server directory.

Our server directory is:

```text
~/minecraft/
```

It may contain:

| File or Directory | Purpose |
|---|---|
| `world/` | Main Minecraft world |
| `world_nether/` | Nether world on server versions/configurations using this layout |
| `world_the_end/` | End world on server versions/configurations using this layout |
| `server.properties` | Main server configuration |
| `whitelist.json` | Whitelisted player profiles |
| `ops.json` | Operator configuration |
| `banned-players.json` | Banned player information |
| `plugins/` | Installed Paper plugins and their data |
| `paper.jar` | Paper server application |

The exact world directory names and layout can vary depending on the Minecraft and Paper version and server configuration.

Backing up the entire server directory helps preserve files that might otherwise be overlooked.

Some files, such as logs and temporary caches, may not be essential for recovery. However, backing up the complete directory is a convenient starting point for beginners.

## 4. Important Rule: Stop the Server Before Backing Up

Before creating a backup of our Minecraft server, we should shut it down cleanly.

A running server may still be writing data to the world files.

Copying files while they are actively changing can result in an inconsistent backup.

### Step 1: Open the Minecraft server console

If PaperMC is running inside tmux, attach to the session:

```bash
tmux attach -t minecraft
```

### Step 2: Stop the server

Enter this command in the PaperMC server console:

```text
stop
```

Do not enter it in the normal Termux shell.

### Step 3: Wait for shutdown

Allow PaperMC to save the world and finish shutting down.

Wait until the Java server process terminates and the Termux shell prompt returns.

Only then should we begin copying the server files.

**Important:** Do not force-close Termux or terminate the Java process when trying to perform a normal shutdown. Use the server's own `stop` command.

For applications other than Minecraft, use the application's documented shutdown or consistent-backup procedure.

## 5. Checking the Server Directory Size

Before creating an archive, it is useful to know how much storage the server is consuming.

In the normal Termux shell, execute:

```bash
du -sh ~/minecraft
```

This displays the total size of the Minecraft server directory.

For example:

```text
1.8G    /data/data/com.termux/files/home/minecraft
```

This is an illustrative output. Your server's actual size will depend on its world and installed software.

To inspect available storage, execute:

```bash
df -h "$HOME"
```

Check that there is enough free space to create the archive.

A compressed backup may be smaller than the original server directory, but the required space depends on the contents and how compressible they are.

## 6. Understanding Archive Files

An archive is a file that contains multiple files and directories.

Instead of copying every individual file separately, we can combine them into one archive.

A common archive format in Linux environments is TAR.

TAR stands for **Tape Archive**.

A TAR archive can store multiple files and directories while preserving their directory structure.

We can also compress the archive using GZIP.

A compressed TAR archive commonly uses the extension:

```text
.tar.gz
```

For example:

```text
minecraft-backup.tar.gz
```

This file contains an archived and compressed copy of the Minecraft server directory.

### Why use TAR and GZIP?

- Multiple files can be stored together.
- Directory structures can be preserved.
- Compression can reduce the archive size.
- The archive can be copied and transferred as a single file.

## 7. Creating a Minecraft Server Backup Using Termux

We will now create our first backup.

### Step 1: Check whether TAR is installed

Execute:

```bash
tar --version
```

If the command is unavailable, install the package:

```bash
pkg install tar
```

### Step 2: Return to the home directory

```bash
cd ~
```

Our Minecraft server directory should be located at:

```text
~/minecraft
```

### Step 3: Create a backup filename

We can include the current date and time in the filename.

Execute:

```bash
BACKUP="$HOME/minecraft-backup-$(date +%F-%H%M).tar.gz"
```

This creates a shell variable containing the backup file path.

For example:

```text
minecraft-backup-2026-11-21-1030.tar.gz
```

The displayed filename is an example. The actual date and time will depend on when the command is executed.

### Step 4: Create the archive

Execute:

```bash
tar -czf "$BACKUP" -C "$HOME" minecraft
```

Let's understand the command.

| Part | Meaning |
|---|---|
| `tar` | Archive utility |
| `-c` | Create a new archive |
| `-z` | Compress using GZIP |
| `-f` | Specify the archive filename |
| `"$BACKUP"` | Destination archive path |
| `-C "$HOME"` | Change to the home directory before archiving |
| `minecraft` | Directory to include in the archive |

After completion, the archive should be created inside your Termux home directory.

### Step 5: Verify that the archive exists

Execute:

```bash
ls -lh "$BACKUP"
```

You should see the archive's filename and size.

**Important:** Do not consider the backup complete just because an archive exists. We should also inspect its contents and test that it can be extracted.

## 8. Inspecting and Verifying a Backup

A backup should be checked before we depend on it.

### Step 1: List archive contents

Execute:

```bash
tar -tzf "$BACKUP"
```

This displays the files and directories stored inside the archive.

The output should contain entries similar to:

```text
minecraft/
minecraft/paper.jar
minecraft/server.properties
minecraft/whitelist.json
minecraft/world/
minecraft/world/level.dat
```

The actual entries depend on your server directory.

### Step 2: Check archive integrity

Execute:

```bash
tar -tzf "$BACKUP" > /dev/null
```

This asks TAR to read through the archive without displaying its file list.

If the command finishes successfully, the archive could be read without TAR reporting an error.

This is a useful basic integrity check, but it does not prove that every application file is valid or that the server will start successfully.

### Step 3: Record the archive size

```bash
du -h "$BACKUP"
```

This displays the size of the backup archive.

Keep a record of when the backup was created and which server version it represents.

## 9. Restoring a Backup

Now imagine that the original Minecraft server directory was damaged or accidentally modified.

We can restore it from our backup archive.

**Important:** For this example, we will first extract the backup into a separate test directory. This prevents us from overwriting the existing server files.

### Step 1: Identify the backup

Navigate to the home directory:

```bash
cd ~
```

List available backups:

```bash
ls -lh minecraft-backup-*.tar.gz
```

Choose the appropriate backup archive.

### Step 2: Create a test restoration directory

```bash
mkdir -p ~/restore-test
```

This creates a directory where we can safely inspect the extracted files.

### Step 3: Extract the archive

Replace the example filename with your actual backup filename.

```bash
tar -xzf ~/minecraft-backup-YYYY-MM-DD-HHMM.tar.gz -C ~/restore-test
```

The `-x` option tells TAR to extract the archive.

The extracted structure should look like:

```text
restore-test/
└── minecraft/
    ├── paper.jar
    ├── server.properties
    ├── whitelist.json
    └── world/
```

### Step 4: Inspect the restored files

Execute:

```bash
ls -la ~/restore-test/minecraft
```

Check that the important files and directories are present.

Do not start the restored server until you have checked that the archive contains the expected data and that the server version is compatible.

## 10. Replacing a Damaged Server Directory

After verifying the restored copy, we can perform an actual restoration.

This procedure should be followed carefully.

### Step 1: Stop PaperMC

If the server is running, stop it using:

```text
stop
```

Wait for the complete shutdown.

### Step 2: Preserve the existing server directory

Instead of immediately deleting the damaged directory, rename it.

For example:

```bash
mv ~/minecraft ~/minecraft-before-restore
```

This keeps the existing files available for inspection.

Make sure that `~/minecraft-before-restore` does not already exist before executing this command.

### Step 3: Extract the chosen backup

Replace the example filename with the actual archive:

```bash
tar -xzf ~/minecraft-backup-YYYY-MM-DD-HHMM.tar.gz -C ~
```

Because the archive contains the top-level `minecraft` directory, this should recreate:

```text
~/minecraft
```

### Step 4: Verify the restored directory

```bash
ls -la ~/minecraft
```

Check that:

- The Paper server JAR is present.
- The configuration files are present.
- The required world directories are present.
- The expected plugin files are present, if applicable.

### Step 5: Start the server

Use the same compatible Java and Paper versions that the backup requires.

For our initial server setup, the example startup command is:

```bash
cd ~/minecraft
tmux new -s minecraft
java -Xms512M -Xmx2G -jar paper.jar --nogui
```

Wait for the server to complete startup.

Check the console for errors and confirm that the expected world is loaded.

The old `minecraft-before-restore` directory should be retained until the restoration has been verified. Delete it only after you are certain that everything works and you no longer need it.

## 11. Storing Backups Outside the Termux Environment

Creating a backup inside Termux is useful, but it is not sufficient for complete protection.

For example, if Termux is uninstalled, its private application data can be deleted.

If the only backup is stored inside that private directory, it may be lost as well.

We therefore need to move important backups to a separate storage location.

### Option 1: Android shared storage

Termux can request access to shared Android storage.

If you have not already configured storage permissions, execute:

```bash
termux-setup-storage
```

Review and approve the Android permission request.

Termux normally creates directory links under:

```text
~/storage/
```

A common shared-storage location is:

```text
~/storage/shared/
```

Create a backup directory:

```bash
mkdir -p ~/storage/shared/Android-Homelab-Backups
```

Copy the backup archive:

```bash
cp "$BACKUP" ~/storage/shared/Android-Homelab-Backups/
```

Check that it was copied:

```bash
ls -lh ~/storage/shared/Android-Homelab-Backups/
```

**Android storage limitation:** Shared storage permissions and file access behaviour vary between Android versions and manufacturers. Android 11 and later also impose scoped-storage restrictions. If the copy fails, check Termux's Android storage permission and consult the Termux documentation.

### Option 2: Transfer to another device

For stronger protection, transfer the archive to another device, such as:

- A laptop.
- An external storage device.
- Another computer.
- A trusted network storage system.

This protects the backup against some failures affecting the Android phone.

### Option 3: Cloud storage

A trusted cloud-storage provider can provide an additional backup location.

Before uploading:

- Review the provider's security and privacy practices.
- Encrypt sensitive backups when appropriate.
- Protect the storage account with strong authentication.
- Keep recovery credentials somewhere safe.

## 12. Understanding the 3-2-1 Backup Strategy

The 3-2-1 backup strategy is a widely used approach to data protection.

It recommends:

- Keeping three copies of important data.
- Storing them on two different types of storage.
- Keeping one copy off-site.

For example:

| Copy | Storage Location |
|---|---|
| Original | Android homelab |
| Backup 1 | Laptop or external storage |
| Backup 2 | Separate off-site or cloud storage |

The purpose is to avoid relying on one device or one physical location.

For a beginner's Android homelab, even maintaining one verified off-device backup is a significant improvement over keeping everything on the phone.

## 13. Backup Strategies for Other Applications

Different server applications store different types of data.

The backup procedure must therefore be adapted to the application.

### 13.1 File Server

For a file server, important data may include:

- User-uploaded files.
- Directory structures.
- Access-control information.
- Application configuration.

Back up important files while ensuring that they are not being modified during the backup.

### 13.2 Web Server

For a web server, important data may include:

- Website source files.
- Application configuration.
- Database contents.
- Custom scripts.
- Required deployment information.

A database should normally be backed up using its supported export or dump mechanism rather than blindly copying its active internal files.

### 13.3 Minecraft Server

For Minecraft, important data includes:

- World directories.
- Server configuration.
- Player and permissions data.
- Plugin files and plugin configurations.
- Other application-specific data.

For a simple setup, backing up the complete server directory after a clean shutdown is a convenient option.

## 14. Understanding Backup Frequency

How frequently should a server be backed up?

That depends on how much data you can afford to lose.

For example:

| Usage | Possible Backup Approach |
|---|---|
| Occasional experimentation | Before major changes |
| Regular Minecraft gameplay | After important sessions or at a planned interval |
| Frequently updated file server | Regular scheduled backups |
| Important data service | More frequent backups with tested recovery procedures |

A backup that is several months old may not contain recent changes.

Create backups regularly and before operations that could damage data, such as software upgrades or major configuration changes.

Automated backups can reduce the need to remember manual backup operations. We will explore automation in a later chapter.

## 15. Common Backup Problems

### Problem 1: Not enough storage space

Possible causes:

- The world directory is large.
- Previous backups are consuming storage.
- Android has limited free internal storage.

Check available storage using:

```bash
df -h "$HOME"
```

Transfer older backups to another storage location before considering their deletion.

### Problem 2: Archive creation fails

Possible causes:

- TAR is not installed.
- The source directory does not exist.
- Storage space is exhausted.
- The shell is using an incorrect file path.
- File access is restricted.

Check the directory:

```bash
ls -la ~/minecraft
```

If TAR is unavailable:

```bash
pkg install tar
```

### Problem 3: Backup archive cannot be extracted

Possible causes:

- The archive is incomplete.
- The file was corrupted during transfer.
- The wrong archive path was entered.
- The backup was created unsuccessfully.

Check the archive:

```bash
tar -tzf YOUR_BACKUP_FILE.tar.gz
```

Do not overwrite the original server directory with an unverified archive.

### Problem 4: Restored Minecraft server does not start

Possible causes:

- An incompatible Java version.
- An incompatible Paper server version.
- Missing files.
- Plugin compatibility problems.
- Incorrect configuration.

Check the server console and use the server version associated with the backup where possible.

Always preserve the original backup before attempting additional recovery operations.

## 16. Important Backup Safety Practices

Follow these practices when managing homelab backups:

- Stop applications cleanly before making file-level backups when consistency requires it.
- Keep at least one copy outside the Android phone.
- Verify archives after creation.
- Test the restoration process periodically.
- Protect private files and credentials.
- Keep backups before updating server software.
- Avoid deleting older backups until newer backups have been verified.
- Never upload private world data or credentials to the public GitHub repository.

A backup that has never been tested should not be assumed to be recoverable.

## 17. Conclusion

Backups are an essential part of running an Android homelab.

In this chapter, we learned:

1. What backups are and why they matter.
2. Which files should be backed up.
3. Why applications should be stopped before consistent file-level backups.
4. How to create compressed TAR archives.
5. How to inspect and verify backup files.
6. How to restore a Minecraft server.
7. How to move backups outside Termux.
8. The 3-2-1 backup strategy.
9. How backup requirements differ between applications.
10. How to troubleshoot common backup and recovery problems.

By implementing a backup strategy, we can protect the data stored by our Android homelab and recover from common failures.

The next stage of the project will explore automating repetitive server-management tasks using shell scripts.

## 18. References

- [PaperMC – Basic Troubleshooting and Backup Recommendations](https://docs.papermc.io/paper/basic-troubleshooting/)
- [PaperMC – Next Steps and Backups](https://docs.papermc.io/paper/next-steps/)
- [PaperMC – Updating](https://docs.papermc.io/paper/updating/)
- [Termux – Official GitHub Repository](https://github.com/termux/termux-app)
- [Termux – Storage and Backup Documentation](https://github.com/termux/termux-tools/blob/master/doc/termux.1.md.in)
- [GNU TAR Manual](https://www.gnu.org/software/tar/manual/)
