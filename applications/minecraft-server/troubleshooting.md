# Minecraft Server Troubleshooting on Android

## 1. Introduction

Running a Minecraft Java server on an Android smartphone involves several components working together.

Our setup uses:

- Android as the host operating system.
- Termux as the command-line environment.
- Java as the runtime.
- PaperMC as the Minecraft server.
- tmux for managing the server session.
- Tailscale for remote network connectivity.

A problem with any of these components can affect the server.

For example, the server may fail to start because of an incompatible Java version, or a player may be unable to connect because of a network configuration problem.

This guide explains how to identify and troubleshoot common problems in our Android-based Minecraft server.

## 2. Understanding the Troubleshooting Process

Before changing any configuration, identify which component is causing the problem.

A useful troubleshooting sequence is:

1. Identify the error or unexpected behaviour.
2. Check whether PaperMC is running.
3. Inspect the server logs.
4. Check the Java runtime and server files.
5. Test network connectivity if players cannot connect.
6. Make one change at a time.
7. Verify that the problem is resolved.

Avoid reinstalling the entire server or changing several settings without understanding the cause.

### Identifying the affected component

| Component | Example Problem |
|---|---|
| Android | Background process restrictions |
| Termux | Permission or package errors |
| Java | Missing or incompatible runtime |
| PaperMC | Server startup failure |
| tmux | Missing or terminated session |
| Tailscale | Remote connectivity failure |
| Network | Incorrect IP address or unavailable port |
| Minecraft Client | Version or authentication problem |

## 3. Inspecting Minecraft Server Logs

Logs are one of the most useful sources of diagnostic information.

PaperMC records server events, warnings and errors in its log files.

The main log directory is:

```text
~/minecraft/logs/
```

The most recent server log is normally:

```text
~/minecraft/logs/latest.log
```

### Step 1: Navigate to the server directory

Execute this in the Termux shell:

```bash
cd ~/minecraft
```

### Step 2: Inspect available logs

```bash
ls -lh logs/
```

### Step 3: Display the latest log entries

```bash
tail -n 100 logs/latest.log
```

This displays the last 100 lines of the log.

### Step 4: Search for errors

```bash
grep -in "error" logs/latest.log
```

To search for warnings:

```bash
grep -in "warn" logs/latest.log
```

These commands help locate relevant messages, although not every problem is explicitly labelled as an error.

### Understanding crash reports

If PaperMC crashes, it may generate a crash report inside:

```text
~/minecraft/crash-reports/
```

Check whether the directory exists:

```bash
ls -lt ~/minecraft/crash-reports/
```

The newest crash report may contain information about what happened before the server terminated.

PaperMC also archives older logs, so they may not all appear as plain `.log` files.

**Important:** Before modifying server files during troubleshooting, stop PaperMC and create a backup of important data.

Reference:

[PaperMC Basic Troubleshooting](https://docs.papermc.io/paper/basic-troubleshooting/)

## 4. Java Troubleshooting

PaperMC requires a compatible Java runtime.

The Minecraft version determines which Java version is required.

For our initial Minecraft 26.3 setup, Java 25 is required.

### Problem 1: Java command not found

Possible error:

```text
bash: java: command not found
```

**Possible causes:**

- Java has not been installed.
- The installation failed.
- Java is not available in the shell's PATH.

**Solution:**

Check:

```bash
java -version
```

If Java is missing, search for available packages:

```bash
pkg search openjdk
```

Install the compatible runtime from the configured Termux repository.

For our Minecraft 26.3 setup:

```bash
pkg install openjdk-25
```

Then verify:

```bash
java -version
```

### Problem 2: Unsupported Java version

Possible error:

```text
UnsupportedClassVersionError
```

This can occur when the Java runtime is older than the version used to compile the server application.

**Solution:**

1. Identify your Minecraft version.
2. Check the corresponding PaperMC Java requirements.
3. Check the currently installed Java version.
4. Install a compatible runtime.
5. Start the server again.

Do not assume that the same Java version will be suitable for every future Minecraft release.

Reference:

[PaperMC Getting Started](https://docs.papermc.io/paper/getting-started/)

## 5. PaperMC Startup Problems

### Problem 1: Server does not start

Possible causes:

- Missing server JAR.
- Incompatible Java version.
- Incorrect startup command.
- Incomplete download.
- Insufficient storage or available memory.
- Configuration errors.

**Troubleshooting:**

Check the current directory:

```bash
pwd
```

Check the server files:

```bash
ls -lh ~/minecraft
```

Verify Java:

```bash
java -version
```

Then check whether the PaperMC JAR exists:

```bash
ls -lh ~/minecraft/paper.jar
```

If the file is present and the runtime is compatible, try the normal startup command:

```bash
cd ~/minecraft
java -Xms512M -Xmx2G -jar paper.jar --nogui
```

The memory values are examples from our initial setup, not universal requirements.

If the server still fails, inspect the complete terminal error and latest log.

### Problem 2: Unable to access jarfile

Possible error:

```text
Error: Unable to access jarfile paper.jar
```

**Possible causes:**

- Incorrect directory.
- Incorrect filename.
- Missing download.
- Incomplete file transfer.

**Solution:**

Execute:

```bash
cd ~/minecraft
```

Then:

```bash
ls -lh
```

Check the actual JAR filename.

If the filename is different, use the correct name in the startup command.

### Problem 3: EULA has not been accepted

During the first startup, PaperMC creates an `eula.txt` file.

Read the Minecraft EULA:

https://www.minecraft.net/eula

If you agree to its terms, edit:

```bash
nano ~/minecraft/eula.txt
```

Change:

```properties
eula=false
```

to:

```properties
eula=true
```

Save the file and restart PaperMC.

Do not accept the agreement without reviewing it.

### Problem 4: Port already in use

Possible error:

```text
Failed to bind to port
```

**Possible causes:**

- Another Minecraft server is already using the configured port.
- An earlier Java process is still running.
- The server has been configured to bind to an incorrect IP address.

Check active tmux sessions:

```bash
tmux ls
```

Check Java processes:

```bash
pgrep -af java
```

Check `server.properties`:

```bash
grep -n "server-ip\|server-port" ~/minecraft/server.properties
```

For a typical Termux installation, leaving `server-ip` empty is appropriate.

The Minecraft server normally uses TCP port 25565.

Do not start another server instance on the same port while the original server is still running.

## 6. tmux Troubleshooting

We use tmux to manage the PaperMC process without keeping the terminal attached continuously.

### Problem 1: Minecraft session not found

Possible error:

```text
no sessions
```

Check available sessions:

```bash
tmux ls
```

If the Minecraft session is missing, it may have terminated or may not have been created successfully.

Check whether Java is still running:

```bash
pgrep -af java
```

### Problem 2: Session already exists

If you attempt to create a second session with the same name, tmux may report that the session already exists.

Instead of creating another one, attach to the existing session:

```bash
tmux attach -t minecraft
```

### Problem 3: Server stops after detaching

The normal tmux detach shortcut is:

1. Press `Ctrl + B`.
2. Release the keys.
3. Press `D`.

This detaches from the session while leaving its processes running.

Do not use commands that kill the session when you only intend to detach.

### Problem 4: Cannot access the server console

List sessions:

```bash
tmux ls
```

Then attach:

```bash
tmux attach -t minecraft
```

If the session has terminated, inspect the latest log to understand why.

## 7. Minecraft Connection Problems

A player may be unable to join even when PaperMC starts successfully.

Connection troubleshooting should begin by separating network connectivity from Minecraft-specific configuration.

### Problem 1: Server is not visible on the local network

Possible causes:

- The phone and laptop are on different networks.
- The wrong local IP address is being used.
- Wi-Fi client isolation is enabled.
- PaperMC is not running.
- The server is listening on an unexpected interface or port.

**Troubleshooting:**

1. Connect both devices to the same local network.
2. Find the Android phone's current local IP address.
3. Confirm that PaperMC is running.
4. Check the server port in `server.properties`.
5. Test TCP connectivity from Windows.

Example PowerShell command:

```powershell
Test-NetConnection ANDROID_LOCAL_IP -Port 25565
```

Replace the placeholder with the actual local IP address.

Look for:

```text
TcpTestSucceeded : True
```

A successful result confirms that the TCP connection test worked.

### Problem 2: Minecraft displays a connection timeout

A connection timeout means that the expected connection was not established within the allowed period.

Possible causes:

- Incorrect destination IP.
- Network routing problems.
- Server unavailable.
- A firewall or network rule blocking traffic.
- The devices cannot communicate.

Check the server's running state and test the network connection separately.

Do not immediately change Minecraft authentication settings to solve a timeout.

### Problem 3: Minecraft displays a connection refused error

A connection refusal generally indicates that the destination was reached but the connection was rejected.

Possible causes include:

- No application is listening on the requested port.
- The server has stopped.
- The wrong port is being used.
- The service is listening on a different network interface.

Check the server console and confirm that PaperMC completed startup.

Then verify that the Minecraft client is using the configured port.

### Problem 4: getsockopt error

During our initial setup, we encountered a Minecraft connection error containing the term:

```text
getsockopt
```

This term refers to a socket-related operation. It does not identify one unique root cause.

Depending on the complete error message, it may be associated with connection timeouts, refused connections or other network problems.

**Troubleshooting approach:**

1. Confirm that the Minecraft server is running.
2. Verify the Android phone's IP address.
3. Check that Tailscale is connected when using remote access.
4. Verify device-sharing authorization.
5. Test the Minecraft TCP port separately.
6. Inspect server logs.
7. Investigate Minecraft authentication only after confirming network connectivity.

On Windows PowerShell:

```powershell
Test-NetConnection ANDROID_IP -Port 25565
```

Replace `ANDROID_IP` with the actual destination address.

A result of `False` means the TCP connection test failed.

Possible causes include an unavailable server, incorrect address, access-control restrictions or network problems.

A result of `True` confirms TCP connectivity, but does not guarantee that Minecraft authentication or gameplay will succeed.

## 8. Tailscale Connection Problems

Our setup uses Tailscale to let friends access the Android server from different locations.

The following checks help isolate remote connectivity problems.

### Problem 1: Android device appears offline

Check:

- Is Tailscale enabled on Android?
- Does the phone have internet access?
- Has Android restricted background activity?
- Is the user still signed in?

Open the Tailscale application and check its connection status.

### Problem 2: Friend cannot see the shared device

Possible causes:

- The sharing invitation has not been accepted.
- The wrong email address was used.
- The friend is signed into another Tailscale account.
- The invitation was revoked.
- The Android device is offline.

Review the sharing status in the Tailscale Admin Console.

The friend should accept the invitation using their own Tailscale account.

### Problem 3: Device is visible but unreachable

First, verify the Tailscale connection independently of Minecraft.

On Windows, if the Tailscale CLI is available, execute:

```powershell
tailscale status
```

Then:

```powershell
tailscale ping ANDROID_TAILSCALE_IP
```

Replace the placeholder with the Android device's actual Tailscale IP address.

The `tailscale ping` command checks connectivity between Tailscale devices. Its output can also indicate whether the connection is direct or relayed.

If connectivity fails, check:

- Tailscale client status.
- Device-sharing permissions.
- Access-control policies.
- Internet connectivity.
- The destination IP address.

Official guidance:

[Tailscale Connection Troubleshooting](https://tailscale.com/docs/reference/troubleshooting/connectivity)

### Problem 4: Tailscale works but Minecraft does not

Tailscale connectivity and application connectivity are separate.

A successful Tailscale ping does not prove that PaperMC is listening on TCP port 25565.

Use:

```powershell
Test-NetConnection ANDROID_TAILSCALE_IP -Port 25565
```

Then verify the server process and port configuration.

Tailscale's official connection guide recommends checking the device connection, target service, port and access policies independently.

Reference:

[Tailscale – Connect to Devices](https://tailscale.com/docs/how-to/connect-to-devices)

## 9. Whitelist and Authentication Problems

### Problem 1: A friend cannot join despite being on the whitelist

In the PaperMC console, execute:

```text
whitelist list
```

Verify the exact player entry.

Check:

- Whether the player was added correctly.
- Whether the whitelist is enabled.
- Whether the correct server is being accessed.
- Whether the authentication configuration matches the player's account type.

### Problem 2: Player identity appears incorrect

Minecraft Java servers normally authenticate players through official account services when:

```properties
online-mode=true
```

Our initial experimental configuration used:

```properties
online-mode=false
```

This disables normal account authentication.

In offline mode, player identity is not reliably verified. A whitelist does not prevent someone from impersonating an allowed username.

For servers requiring reliable identity verification, use appropriately authenticated Minecraft accounts and enable normal online authentication.

Do not publicly expose the experimental offline-mode server.

### Problem 3: Player cannot use administrative commands

Some commands require operator privileges.

To grant operator access:

```text
op PlayerName
```

To remove operator access:

```text
deop PlayerName
```

Only trusted administrators should receive operator privileges.

## 10. Performance and Lag Troubleshooting

A player may connect successfully but still experience lag.

It is important to distinguish client performance from server performance.

### 10.1 Understanding FPS

FPS stands for Frames Per Second.

It measures how frequently the Minecraft client renders frames.

Low FPS is generally associated with client-side performance.

Possible causes include:

- High graphics settings.
- Shaders.
- High render distance.
- Limited GPU performance.
- Other applications consuming resources.

For example, a player using heavy shaders may experience low FPS even when the Android server is performing normally.

### 10.2 Understanding TPS

TPS stands for Ticks Per Second.

Minecraft Java servers normally aim to process 20 ticks per second.

When the server cannot maintain its normal tick rate, players may experience delayed block updates, entity movement and other gameplay effects.

Low TPS is a server-side performance problem.

Possible causes include:

- Heavy world generation.
- Large entity counts.
- Demanding plugins.
- Excessive simulation distance.
- CPU limitations.
- Thermal throttling.

### 10.3 Understanding MSPT

MSPT stands for Milliseconds Per Tick.

At 20 TPS, the server has approximately 50 milliseconds to process each tick.

Lower MSPT is generally better.

If processing regularly exceeds the 50 ms budget, the server may fail to maintain 20 TPS.

### 10.4 Using Spark to Diagnose Performance

Recent PaperMC versions include the spark profiler.

It can help identify which parts of the server are consuming the most processing time.

From the Minecraft server console, execute:

```text
spark profiler start --timeout 300
```

This starts a profiler session with a five-minute timeout.

After profiling, PaperMC provides a report that can be inspected to investigate performance problems.

The profiling period should include the actual workload that causes the lag.

Official documentation:

[PaperMC Profiling](https://docs.papermc.io/paper/profiling/)

### 10.5 Reducing Server Workload

For an Android smartphone, experiment with conservative settings.

For example:

```properties
view-distance=6
simulation-distance=4
```

Also consider:

- Reducing unnecessary entities.
- Avoiding demanding plugins.
- Limiting simultaneous player activity during testing.
- Avoiding heavy background workloads.
- Monitoring device temperature.

Change one setting at a time and compare the results.

## 11. Android Background and Thermal Problems

### Problem 1: Server stops when the screen turns off

Possible causes:

- Battery optimization.
- Manufacturer-specific background restrictions.
- Memory pressure.
- Android terminating the application.

Check Termux's battery and background settings.

Termux also provides:

```bash
termux-wake-lock
```

This requests a wake lock while the server is running.

It can help prevent device suspension, but it does not guarantee that Android will keep the process alive indefinitely.

When no longer needed:

```bash
termux-wake-unlock
```

### Problem 2: Phone becomes hot

A Minecraft server performs continuous background processing.

Extended CPU usage can raise device temperature.

Recommendations:

- Keep the phone in a ventilated location.
- Avoid direct sunlight.
- Avoid covering the phone.
- Monitor temperature during extended sessions.
- Stop the server if the device becomes excessively hot.

Do not operate a device with a swollen or damaged battery.

### Problem 3: Performance decreases over time

Possible causes include:

- Thermal throttling.
- Increased world workload.
- Background processes.
- Memory pressure.
- Storage activity.

Compare performance shortly after startup with performance after extended gameplay.

A five-minute test does not prove that a device can maintain the same performance indefinitely.

## 12. A Practical Diagnostic Checklist

When a player reports that they cannot join the Minecraft server, use this sequence.

| Order | What to Check |
|---|---|
| 1 | Is PaperMC running? |
| 2 | Does the server console show startup errors? |
| 3 | Is the correct server IP being used? |
| 4 | Is the correct port being used? |
| 5 | Is Tailscale connected when remote access is required? |
| 6 | Has the device-sharing invitation been accepted? |
| 7 | Does the TCP connection test succeed? |
| 8 | Does the Minecraft version match? |
| 9 | Are authentication and whitelist settings correct? |

This process helps identify whether the issue is related to the server, network or Minecraft client.

## 13. Useful Diagnostic Commands

### Termux

Check Java:

```bash
java -version
```

Check the server files:

```bash
ls -lh ~/minecraft
```

Check the latest log:

```bash
tail -n 100 ~/minecraft/logs/latest.log
```

Check Java processes:

```bash
pgrep -af java
```

Check tmux sessions:

```bash
tmux ls
```

Check available storage:

```bash
df -h "$HOME"
```

Check server directory size:

```bash
du -sh ~/minecraft
```

### Windows PowerShell

Display network configuration:

```powershell
ipconfig
```

Test the Minecraft TCP port:

```powershell
Test-NetConnection ANDROID_IP -Port 25565
```

Check Tailscale devices:

```powershell
tailscale status
```

Test Tailscale device connectivity:

```powershell
tailscale ping ANDROID_TAILSCALE_IP
```

Replace placeholders with actual addresses. Do not publish your real device addresses in this public tutorial.

## 14. Important Troubleshooting Practices

Follow these practices:

1. Read the complete error message.
2. Inspect server logs before changing settings.
3. Identify which component is failing.
4. Change one configuration at a time.
5. Back up important files before making modifications.
6. Stop the server gracefully before editing its data.
7. Avoid unnecessary reinstalls.
8. Record the cause and verified solution.
9. Do not publish credentials or private logs.

A useful troubleshooting record contains:

| Field | Example |
|---|---|
| Problem | Server cannot start |
| Error | Unable to access jarfile |
| Cause | Incorrect JAR filename |
| Solution | Use the correct downloaded filename |
| Verification | PaperMC starts successfully |

## 15. Conclusion

Troubleshooting is an essential part of managing a Minecraft server.

In this tutorial, we covered:

- Java runtime errors.
- PaperMC startup failures.
- Missing or incorrect server files.
- Port conflicts.
- tmux session problems.
- Local network connection failures.
- Tailscale connectivity issues.
- getsockopt and connection timeout errors.
- Whitelist and authentication problems.
- FPS, TPS and MSPT.
- Android battery and thermal restrictions.

The most important lesson is to diagnose the problem before applying a solution.

The same troubleshooting approach can be reused when we introduce additional server applications into Android-Homelab.

## 16. References

- [PaperMC Basic Troubleshooting](https://docs.papermc.io/paper/basic-troubleshooting/)
- [PaperMC Profiling](https://docs.papermc.io/paper/profiling/)
- [PaperMC Getting Started](https://docs.papermc.io/paper/getting-started/)
- [Tailscale Troubleshooting](https://tailscale.com/docs/reference/troubleshooting/connectivity)
- [Tailscale Connect to Devices](https://tailscale.com/docs/how-to/connect-to-devices)
- [Termux Official Repository](https://github.com/termux/termux-app)
- [GNU Coreutils](https://www.gnu.org/software/coreutils/manual/coreutils.html)
