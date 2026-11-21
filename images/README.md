# Project Images and Screenshots

This directory contains screenshots from the Android-Homelab implementation. They provide visual evidence for the setup and are embedded in the relevant tutorials.

## Current files

| Directory | File | Description |
|---|---|---|
| `termux/` | `java-version.jpeg` | OpenJDK version and architecture reported by Termux |
| `minecraft/` | `paper-server-initial-startup.jpeg` | Initial PaperMC startup log on the Redmi Note 8 Pro |
| `minecraft/` | `minecraft-gameplay.jpeg` | Minecraft gameplay connected to the Android-hosted server |
| `networking/` | `tailscale-connection-result.png` | Windows TCP connectivity test to port 25565 over Tailscale |

The system architecture diagrams are maintained as Mermaid source in [docs/architecture.md](../docs/architecture.md), rather than as exported image files.

## Image guidelines

- Prefer screenshots from actual project tests.
- Keep commands and relevant output readable.
- Hide passwords, authentication tokens, email addresses, private IP addresses and other information that should not be public.
- Do not upload private server configurations, world backups or credentials.
- Use descriptive filenames and link each image from the relevant tutorial.
- Label screenshots accurately; a successful startup message does not imply that every warning has been resolved.
