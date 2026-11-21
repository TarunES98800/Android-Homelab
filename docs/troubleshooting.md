# Troubleshooting an Android Homelab

## 1. Introduction

Building a homelab involves installing software, configuring applications, managing storage and establishing network connections.

During this process, errors are normal.

A server may fail to start, a package may refuse to install, a remote connection may time out or Android may terminate a background process.

The important skill is learning how to identify the cause instead of randomly changing settings.

This chapter documents common problems encountered while building an Android homelab using Termux, PaperMC and Tailscale.

It also provides a systematic troubleshooting approach that can be applied to other server applications.

## 2. A Systematic Troubleshooting Approach

When something goes wrong, do not immediately reinstall everything or change several configurations.

Follow a structured process.

### Step 1: Identify the problem

Observe what happened.

For example:

- Did the application fail to start?
- Did it start and then close?
- Can the server be accessed locally?
- Does remote access fail?
- Is the device overheating?
- Is there an error message?

### Step 2: Identify the affected component

An Android homelab contains multiple components.

| Component | Possible Problem |
|---|---|
| Android | Background restrictions or overheating |
| Termux | Installation, permission or package errors |
| Java | Missing or incompatible runtime |
| PaperMC | Startup failure or server crash |
| Tailscale | Remote connectivity failure |
| Network | Incorrect IP address or blocked port |
| Storage | Insufficient space or missing files |

Identify the component most closely related to the problem.

### Step 3: Inspect the error message and logs

Applications often record useful diagnostic information.

Check the terminal output, application logs and system messages where available.

Do not delete log files before inspecting them.

### Step 4: Reproduce the problem

Try to determine which action causes the problem.

For example, does the server fail every time it starts, or only after a friend connects?

Reproducing the issue helps narrow down the possible causes.

### Step 5: Make one change at a time

Avoid changing multiple settings simultaneously.

Make one controlled change, test it and record the result.

This makes it easier to identify which change actually fixed the issue.

### Step 6: Back up before modifying important data

Before changing server configurations, plugins or world data, create a backup.

See [Backups and Recovery](backups-and-recovery.md).

## 3. Termux Troubleshooting

Termux is the foundation of our Android homelab. Problems with its installation, package manager or permissions can affect every application running inside it.

### Problem 1: Termux cannot install packages

**Possible symptoms:**

- Package download fails.
- Repository connection errors appear.
- Package installation stops unexpectedly.
- The package manager reports repository or dependency errors.

**Possible causes:**

- No internet connection.
- Package repository temporarily unavailable.
- Outdated package information.
- Incorrect repository configuration.
- An unsupported or mixed installation source.

**Troubleshooting:**

First, verify that the Android phone has an internet connection.

Then execute:

```bash
pkg update
```

If package information updates successfully, try installing the required package again.

For example:

```bash
pkg install nano
```

If the error persists, read the complete error message and consult the official Termux package-management documentation.

Do not randomly change repositories or download packages from unknown websites.

Reference:

[Termux Package Management](https://github.com/termux/termux-packages/wiki/Package-Management)

### Problem 2: Termux reports permission errors

**Possible symptoms:**

- A command cannot access a file.
- Shared storage cannot be opened.
- A script cannot be executed.
- File operations fail with a permission-denied message.

**Possible causes:**

- Android has not granted the required permission.
- The file is in a restricted storage location.
- The file does not have the required permissions.
- The application is attempting to access a directory outside its permitted environment.

**Troubleshooting:**

For shared storage access, execute:

```bash
termux-setup-storage
```

Review the Android permission request and grant access if needed.

To inspect file permissions:

```bash
ls -l
```

To inspect the current working directory:

```bash
pwd
```

Do not use broad commands such as `chmod 777` to fix every permission error. First identify which permission is missing and why.

### Problem 3: Termux closes unexpectedly

**Possible symptoms:**

- The terminal disappears.
- A server stops when the screen is turned off.
- A background application is terminated.
- The server works temporarily but stops later.

**Possible causes:**

- Android battery optimization.
- Manufacturer-specific background restrictions.
- Insufficient available memory.
- Excessive processor usage.
- Device overheating.

**Troubleshooting:**

1. Open Android Settings.
2. Find the Termux application settings.
3. Inspect its battery usage and background restrictions.
4. Select an appropriate unrestricted or less restrictive option if available.
5. Check whether the phone is overheating.
6. Monitor the server after making the changes.

The names of battery settings differ between Android versions and manufacturers.

Termux also provides a command called:

```bash
termux-wake-lock
```

This requests a wake lock to help prevent the device from suspending while Termux is active.

It does not guarantee that Android will keep every process alive, nor does it disable all manufacturer-specific background restrictions.

When the wake lock is no longer needed, release it using:

```bash
termux-wake-unlock
```

Use wake locks carefully because they can increase battery consumption and heat.

### Problem 4: Termux storage is full

**Possible symptoms:**

- Archives cannot be created.
- Applications cannot download files.
- Package installation fails.
- Server applications cannot save additional data.

**Troubleshooting:**

Check available storage:

```bash
df -h "$HOME"
```

Check the total Minecraft server directory size:

```bash
du -sh ~/minecraft
```

Inspect large directories before deleting anything.

Move important backups to another trusted storage location.

Do not delete world files, application directories or configurations simply because storage is running low.

## 4. Java Troubleshooting

Java-based applications require a compatible Java Runtime Environment.

Our Minecraft Java server uses Java to execute PaperMC.

### Problem 1: Java command not found

**Possible error:**

```text
bash: java: command not found
```

**Possible cause:**

Java is not installed, or the executable is not available in the shell's PATH.

**Troubleshooting:**

Check whether Java is available:

```bash
java -version
```

If Java is not installed, install an appropriate package available for the current Termux repository.

For example:

```bash
pkg search openjdk
```

Then install the appropriate Java runtime package.

For example, if the selected package is available:

```bash
pkg install openjdk-25
```

Package names and available versions can change. Check the repository before relying on a particular package name.

After installation, verify:

```bash
java -version
```

### Problem 2: Unsupported Java version

**Possible error:**

```text
UnsupportedClassVersionError
```

This error can occur when the Java runtime is older than the version used to compile the application.

For example, a server built for a newer Java runtime may not run under an older one.

**Troubleshooting:**

1. Identify the Minecraft and Paper versions.
2. Check the Java requirement for that server version.
3. Check the installed Java version.
4. Install a compatible runtime.
5. Start the server again.

Use the official PaperMC requirements:

[PaperMC Getting Started](https://docs.papermc.io/paper/getting-started/)

Java requirements are version-dependent. Do not assume that every Paper release requires the same Java version.

### Problem 3: Multiple Java versions cause confusion

If multiple Java installations are present, the shell may execute a different version from the one expected.

Check the executable location:

```bash
which java
```

Check the active version:

```bash
java -version
```

Verify the version again in the same Termux environment used to launch the server.

## 5. PaperMC Troubleshooting

PaperMC is the Minecraft Java server implementation used in our first homelab application.

Its console and log files provide important information about startup and runtime problems.

### Problem 1: PaperMC does not start

**Possible symptoms:**

- Java exits immediately.
- The server JAR cannot be loaded.
- The application displays an error and returns to the shell.
- The server stops during initialization.

**Troubleshooting:**

First, enter the server directory:

```bash
cd ~/minecraft
```

List the files:

```bash
ls -lh
```

Check that the server JAR exists.

For our initial configuration, the JAR was named:

```text
paper.jar
```

Verify Java:

```bash
java -version
```

Then run:

```bash
java -Xms512M -Xmx2G -jar paper.jar --nogui
```

The memory values are examples from our initial setup, not universal requirements for every phone.

If the server still fails, inspect the complete error message before changing its configuration.

### Problem 2: Unable to access jarfile

**Possible error:**

```text
Error: Unable to access jarfile paper.jar
```

**Possible causes:**

- The terminal is in the wrong directory.
- The JAR filename is different.
- The download failed.
- The file is missing.

Check:

```bash
pwd
```

Then:

```bash
ls -lh
```

If the JAR has a different filename, use its actual name in the startup command.

For example:

```bash
java -jar actual-server-file.jar --nogui
```

Do not rename or replace files without first confirming which server version they contain.

### Problem 3: EULA error

On its first startup, a Minecraft server requires the user to review and accept the Minecraft End User License Agreement.

If the server reports that the EULA has not been accepted:

1. Stop the startup attempt.
2. Open the `eula.txt` file.
3. Read the agreement.
4. Only if you agree to its terms, change the setting to:

```properties
eula=true
```

5. Save the file.
6. Start the server again.

The acceptance setting should not be changed blindly without reviewing the agreement.

### Problem 4: Server reports that the port is already in use

**Possible error:**

```text
Failed to bind to port
```

**Possible causes:**

- Another Minecraft server is already running on that port.
- An existing Java process has not terminated.
- The server is configured to bind to an incorrect network address.

Check existing tmux sessions:

```bash
tmux ls
```

Inspect running Java processes:

```bash
pgrep -af java
```

If an earlier server is still running, connect to its session and stop it gracefully.

In many PaperMC setups, the `server-ip` field in `server.properties` should be left empty rather than filled with the phone's public IP address.

Do not change this setting without understanding which network interface the server should use.

Reference:

[PaperMC Basic Troubleshooting](https://docs.papermc.io/paper/basic-troubleshooting/)

### Problem 5: Minecraft world cannot be loaded

**Possible symptoms:**

- The server crashes while loading a world.
- The console reports world-data errors.
- The world was previously opened with a newer Minecraft version.

A common cause is using a server version older than the version that last saved the world.

Minecraft world downgrades are not generally supported and may result in corruption.

**Troubleshooting:**

1. Stop the server.
2. Create a backup of the world.
3. Identify the Minecraft version used by the backup.
4. Check which server version is compatible.
5. Start with a compatible server version using a separate test copy where possible.

Do not attempt an unsupported downgrade on your only world copy.

### Problem 6: Plugin causes a server crash

**Possible causes:**

- Plugin incompatible with the current Minecraft version.
- Missing plugin dependency.
- Incorrect plugin configuration.
- Plugin conflict.
- Incompatible Java version.

Inspect the latest server log:

```bash
tail -n 100 ~/minecraft/logs/latest.log
```

Look for error messages mentioning the plugin.

If necessary:

1. Stop the server.
2. Back up the server directory.
3. Identify the problematic plugin.
4. Check its official documentation.
5. Test with the plugin removed or updated on a separate copy.

Do not delete several plugins at once without recording which changes were made.

### Problem 7: Minecraft server stops without an obvious error

Check the latest log:

```bash
tail -n 100 ~/minecraft/logs/latest.log
```

Check whether a crash report exists:

```bash
ls -lt ~/minecraft/crash-reports/
```

If no crash report exists, the process may have been terminated externally.

Possible causes include:

- Android background management.
- Memory pressure.
- Device overheating.
- Unexpected process termination.

On conventional Linux systems, PaperMC may recommend checking kernel logs for process termination. However, a normal unrooted Termux installation may not have permission to inspect Android's full kernel logs.

Do not assume that the absence of a crash report proves the application shut down normally.

## 6. tmux Troubleshooting

We use tmux to keep the Minecraft server session available while working in other Termux sessions.

### Problem 1: Cannot attach to the server session

**Possible error:**

```text
no sessions
```

Check available tmux sessions:

```bash
tmux ls
```

If no Minecraft session exists, the session may have terminated or may never have been created.

If a session exists, attach using:

```bash
tmux attach -t minecraft
```

### Problem 2: tmux reports that the session already exists

**Possible cause:**

A Minecraft tmux session is already running.

Instead of creating another one, attach to the existing session:

```bash
tmux attach -t minecraft
```

Check the session list before starting a duplicate server.

### Problem 3: Detaching from tmux stops the server

The normal tmux detach shortcut is:

```text
Ctrl + B
```

Then press:

```text
D
```

This detaches from the tmux session without intentionally stopping its process.

Make sure you are using the tmux shortcut rather than closing or killing the server session.

### Problem 4: The server is still running but cannot be found

Check:

```bash
tmux ls
```

If the session is missing, check Java processes:

```bash
pgrep -af java
```

A running Java process does not necessarily mean it is healthy or accepting connections. Inspect the relevant logs and process state.

## 7. Tailscale Troubleshooting

Tailscale allows authorized devices to communicate over a private network.

When remote access fails, diagnose Tailscale connectivity separately from the application being hosted.

### Problem 1: Android device does not appear online

**Possible causes:**

- Tailscale is disconnected.
- The phone has no internet connection.
- Android has restricted the application.
- The device needs to reconnect or sign in again.

**Troubleshooting:**

1. Open Tailscale on Android.
2. Check its connection status.
3. Verify that the phone has internet access.
4. Check whether Android battery settings restrict Tailscale.
5. Inspect the device in the Tailscale Admin Console.

### Problem 2: Friend cannot see the shared Android device

**Possible causes:**

- The sharing invitation has not been accepted.
- The friend is signed into the wrong account.
- The device was not shared with the intended email address.
- The sharing invitation has been revoked.
- The Android device is offline.

**Troubleshooting:**

1. Open the Tailscale Admin Console.
2. Find the Android device.
3. Review its sharing status.
4. Confirm that the invitation was sent to the correct account.
5. Ask the friend to check the invitation and accept it.
6. Reconnect the Tailscale clients.

### Problem 3: Shared device appears, but cannot be reached

**Possible causes:**

- The shared device is offline.
- The wrong Tailscale IP was entered.
- An access-control policy blocks communication.
- The target application is not running.
- The target port is incorrect.

Test Tailscale connectivity separately from Minecraft connectivity.

On a Windows computer with the Tailscale command-line interface available, execute:

```powershell
tailscale status
```

To test connectivity to the Android device:

```powershell
tailscale ping YOUR_ANDROID_TAILSCALE_IP
```

Replace the placeholder with the actual Tailscale IP address.

If the device is reachable through Tailscale, the next step is testing the application port.

Official guidance:

[Tailscale – Connect to Devices](https://tailscale.com/docs/how-to/connect-to-devices)

### Problem 4: Minecraft TCP connection test returns False

On Windows, execute:

```powershell
Test-NetConnection YOUR_ANDROID_TAILSCALE_IP -Port 25565
```

Look for:

```text
TcpTestSucceeded : True
```

If the result is False, check:

1. Is PaperMC running?
2. Is Tailscale connected on the Android phone?
3. Has the friend accepted the sharing invitation?
4. Is the correct Tailscale IP being used?
5. Is PaperMC listening on TCP port 25565?
6. Do the sharing and access-control policies permit the connection?

Do not change Minecraft authentication settings to solve a network connectivity failure.

### Problem 5: Minecraft shows a getsockopt or connection error

A message containing `getsockopt` is related to a socket/network operation.

It does not identify one single root cause.

The full error message and connection test results are needed to diagnose it properly.

Possible causes include:

- Unreachable destination.
- Incorrect IP address.
- Connection timeout.
- Target application unavailable.
- Network filtering.
- Connection refusal.

First run:

```powershell
Test-NetConnection YOUR_ANDROID_TAILSCALE_IP -Port 25565
```

Then inspect the server's running state and logs.

If the TCP test fails, troubleshoot the network path and server listener before investigating Minecraft login or gameplay settings.

If the TCP test succeeds but Minecraft still cannot join, investigate the Minecraft version, authentication, whitelist and server configuration separately.

### Problem 6: Tailscale works, but server performance is poor

Connectivity does not guarantee high performance.

Slow gameplay may be caused by:

- Internet connection quality.
- Network latency.
- Packet loss.
- Relayed rather than direct connectivity.
- Android hardware limitations.
- High server CPU usage.

Use Tailscale diagnostics and compare performance on the local network when possible.

Reference:

[Tailscale Troubleshooting](https://tailscale.com/docs/reference/troubleshooting)

## 8. Minecraft Gameplay Performance Troubleshooting

A player may be able to connect successfully but still experience lag.

It is important to distinguish client performance from server performance.

### Client FPS

FPS stands for Frames Per Second.

It measures how frequently the player's computer renders frames.

Low FPS may result from:

- Graphics settings.
- Shaders.
- High render distance.
- Insufficient GPU performance.
- Other applications using system resources.

Server changes do not necessarily fix low client FPS.

### Server TPS

TPS stands for Ticks Per Second.

Minecraft Java servers normally aim to process 20 ticks per second.

When the server cannot keep up, players may experience delayed actions, block updates or entity movement.

### Possible causes of low server TPS

- Excessive entity count.
- Heavy world generation.
- Too many demanding plugins.
- High CPU usage.
- Thermal throttling.
- Insufficient available memory.

### Troubleshooting steps

1. Check the server console.
2. Observe CPU usage and device temperature using available tools.
3. Reduce excessive view and simulation distances when appropriate.
4. Check whether plugins are consuming excessive resources.
5. Avoid heavy background tasks while the server is running.
6. Test with a smaller workload.

Do not assume that a faster client computer automatically improves server TPS.

The Android phone is responsible for processing server-side game logic.

## 9. Android Device Performance Problems

### Problem 1: Phone becomes excessively hot

Possible causes:

- Sustained CPU usage.
- Poor ventilation.
- High ambient temperature.
- Charging while running demanding applications.
- Heavy background workloads.

Recommendations:

- Place the phone in a well-ventilated area.
- Avoid direct sunlight.
- Monitor device temperature.
- Reduce unnecessary workloads.
- Stop the server if the phone becomes excessively hot.

If the battery becomes swollen or damaged, disconnect the device from power and have it assessed by a qualified repair professional.

### Problem 2: Server stops when screen turns off

Possible causes:

- Android battery optimization.
- Manufacturer-specific background restrictions.
- Memory pressure.
- Lack of appropriate wake-lock handling.

Review the Android battery settings for Termux.

If required, use `termux-wake-lock` and monitor whether the server remains active.

Remember that a wake lock does not guarantee uninterrupted execution.

### Problem 3: Server becomes slower after running for a long time

Possible causes:

- Thermal throttling.
- Increasing world workload.
- Memory pressure.
- Storage-related activity.
- Background processes.

Compare performance shortly after startup with performance after extended operation.

A short successful test does not prove that the device can maintain the same performance continuously.

## 10. Backup and Recovery Troubleshooting

### Problem 1: Not enough storage to create an archive

Check available storage:

```bash
df -h "$HOME"
```

Check the server directory size:

```bash
du -sh ~/minecraft
```

Move older backups to a separate storage location.

Do not delete the original world simply to make space without first confirming that another verified copy exists.

### Problem 2: TAR reports an error

Check whether the archive utility is installed:

```bash
tar --version
```

If it is missing:

```bash
pkg install tar
```

Check the source directory:

```bash
ls -la ~/minecraft
```

Make sure the server is stopped when creating a consistent file-level backup.

### Problem 3: Backup archive cannot be restored

Test the archive contents:

```bash
tar -tzf YOUR_BACKUP_FILE.tar.gz
```

Extract it into a separate test directory:

```bash
mkdir -p ~/restore-test
```

```bash
tar -xzf YOUR_BACKUP_FILE.tar.gz -C ~/restore-test
```

Inspect the extracted files before replacing the original server directory.

Never overwrite the only remaining copy of a server world with an unverified archive.

## 11. Useful Diagnostic Commands

The following commands are useful when investigating common Android homelab problems.

| Command | Purpose |
|---|---|
| `pwd` | Display current directory |
| `ls -lh` | List files and sizes |
| `df -h` | Check filesystem space |
| `du -sh DIRECTORY` | Check directory size |
| `java -version` | Check Java runtime version |
| `which java` | Locate Java executable |
| `termux-info` | Display Termux environment information |
| `tmux ls` | List tmux sessions |
| `pgrep -af java` | Inspect Java processes |
| `tail -n 100 FILE` | Display the last 100 lines of a file |
| `tar -tzf FILE.tar.gz` | Inspect a compressed TAR archive |

Some commands may require installing additional Termux packages.

For Windows networking diagnostics:

```powershell
ipconfig
```

Displays network configuration.

```powershell
Test-NetConnection HOST -Port PORT
```

Tests TCP connectivity to a specified host and port.

```powershell
tailscale status
```

Displays Tailscale connection information when the CLI is available.

## 12. Important Troubleshooting Practices

Follow these rules when diagnosing problems:

1. Read the complete error message before changing anything.
2. Check logs and application status.
3. Identify whether the problem is related to Android, Termux, the application or the network.
4. Change one setting at a time.
5. Back up important data before modifying server files.
6. Avoid unnecessary reinstalls.
7. Do not publish private credentials or logs containing sensitive information.
8. Record the error, root cause and solution for future reference.

A good troubleshooting record should contain:

| Field | Example |
|---|---|
| Problem | Minecraft server does not start |
| Error | Unable to access jarfile |
| Cause | Incorrect JAR filename |
| Solution | Use the actual downloaded filename |
| Verification | Server starts successfully |

This format also makes it easier to contribute troubleshooting improvements to the repository.

## 13. Conclusion

Troubleshooting is an essential skill for anyone managing a server.

In this chapter, we covered common problems involving:

- Termux installation and permissions.
- Package management.
- Java runtime compatibility.
- PaperMC startup and world loading.
- tmux sessions.
- Tailscale device connectivity.
- Minecraft connection failures.
- Client FPS and server TPS.
- Android overheating and background restrictions.
- Backup and restoration problems.

The most important lesson is to identify the cause of a problem before applying a solution.

As this homelab grows and additional applications are introduced, this chapter can be expanded with new problems and verified solutions.

## 14. References

- [Termux Official GitHub Repository](https://github.com/termux/termux-app)
- [Termux Package Management](https://github.com/termux/termux-packages/wiki/Package-Management)
- [PaperMC Basic Troubleshooting](https://docs.papermc.io/paper/basic-troubleshooting/)
- [PaperMC Getting Started](https://docs.papermc.io/paper/getting-started/)
- [Tailscale Connect to Devices](https://tailscale.com/docs/how-to/connect-to-devices)
- [Tailscale Troubleshooting](https://tailscale.com/docs/reference/troubleshooting)
- [GNU TAR Manual](https://www.gnu.org/software/tar/manual/)
