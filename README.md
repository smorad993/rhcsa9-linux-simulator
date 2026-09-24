# Linux Command Simulator & RHCSA 9 Learning Hub
## Architecture Plan, C4 Diagrams (L1–L4), Flowcharts & Curriculum Breakdown

[🇺🇸 English](README.md) | [🇮🇷 نسخه فارسی (Persian)](README_FA.md)

The **Linux Command Simulator & RHCSA 9 Learning Hub** is a full-featured Flask web application and interactive terminal simulator covering all 26 chapters from the *Red Hat RHCSA 9 Cert Guide (EX200)*, featuring the **Top 10 essential Linux commands per chapter** (260 commands total).

📁 **Project Location:**  
`/Users/moradi/Documents/Mylab/Topics/07-Automation-Scripts/Linux-command`

---

## 1. What Was Built & Delivered

### 📦 Git Repository Initialized
- Initialized local Git repository in `/Users/moradi/Documents/Mylab/Topics/07-Automation-Scripts/Linux-command`.
- Initial commits containing complete application source code, dataset catalog, test suite, and configuration.

### 📚 Complete 26-Chapter Curriculum & 260 Curated Commands
- **Part I: Basic System Management (Ch 1–8):** `hostnamectl`, `timedatectl`, `localectl`, `uname`, `lsblk`, `fdisk`, `man`, `ls`, `grep`, `ssh`, `useradd`, `chmod`, `setfacl`, `nmcli`, `ip`, `ss`, etc.
- **Part II: Operating Running Systems (Ch 9–15):** `dnf`, `rpm`, `ps aux`, `top`, `kill`, `systemctl`, `crontab`, `journalctl`, `mkfs.xfs`, `mount`, `blkid`, `lvextend`, `stratis`, etc.
- **Part III: Advanced Administration (Ch 16–19):** `uname -r`, `lsmod`, `modprobe`, `sysctl`, `grub2-mkconfig`, `systemctl set-default`, `strace`, `lsof`, `tcpdump`, `bash` scripting, etc.
- **Part IV: Managing Network Services (Ch 20–26):** SSH hardening, Apache `httpd`, SELinux (`sestatus`, `semanage fcontext`, `restorecon`, `setsebool`), `firewall-cmd`, NFS/CIFS (`showmount`, `autofs`), Chrony time sync, and Podman containers (`podman run`, `podman generate systemd`).

### 🖥️ Modern Web GUI & Interactive Terminal
- **Dark Glassmorphic UI:** Styled with Vanilla CSS, Outfit and JetBrains Mono typography, status badges, and subtle glow animations.
- **26-Topic Sidebar:** Structured into Parts I–IV with instant topic switching.
- **Top 10 Commands Grid:** Interactive badges and cards displaying category, command name, and brief synopsis.
- **Command Inspector Drawer:** Displays full command syntax with copy button, detailed explanation, flags table, practical **RHCSA EX200 Exam Tips & Gotchas**, and realistic output preview.
- **Live Web Terminal:** Features a colorized prompt (`[root@rhel9-node1 ~]#`), interactive typing, command history (`↑` / `↓` arrows), tab completion, error emulation, and a **"▶ Run in Simulator"** one-click action button.
- **Instant Search Modal:** Triggered with `Ctrl + K` / `Cmd + K` to search across all 260 commands, flags, and descriptions.

### 🧪 Testing & Quality Assurance
- Self-verification test suite (`test_app.py`) with 100% pass rate (**6/6 tests passing**).
- Verifies all 26 chapters, 260 command structures, REST API endpoints, and virtual shell simulation output.

---

## 2. Quick Start & How to Access

### Access the Running Application
The Flask server runs as a service. Open your browser directly at:
👉 **[http://localhost:5050](http://localhost:5050)** (or `http://127.0.0.1:5050`)

*(Port `5050` was chosen to avoid macOS ControlCenter AirPlay conflicts on port `5000`).*

### Option A: Run with Docker Compose (Recommended)
You can run the entire simulator in an isolated container without installing Python or dependencies:
```bash
# Clone the repository
git clone https://github.com/smorad993/rhcsa9-linux-simulator.git
cd rhcsa9-linux-simulator

# Start container in detached mode
docker compose up -d

# View real-time container logs
docker compose logs -f

# Stop container
docker compose down
```

### Option B: Run directly with Docker
```bash
# Build the Docker image
docker build -t rhcsa9-linux-simulator .

# Run the container
docker run -d -p 5050:5050 --name rhcsa9-sim rhcsa9-linux-simulator
```

### Option C: Manual Python Launch
```bash
# Navigate to the project directory
cd /Users/moradi/Documents/Mylab/Topics/07-Automation-Scripts/Linux-command

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the test suite
python3 test_app.py

# Launch the Flask application
python3 app.py
```

---

## 3. System Architecture & C4 Model

```
Level 1: System Context  ---> Who uses it and what systems it touches
Level 2: Container       ---> Flask app, Frontend UI, Mock Engine, Catalog Store
Level 3: Component       ---> Blueprints, Services, Controller, Parsers
Level 4: Code / Schema   ---> Data models, classes, and command execution flow
```

### 2.1 C4 Level 1: System Context Diagram
```mermaid
graph TD
    User["Learner / RHCSA Candidate<br/>(Web Browser)"]
    
    subgraph SystemBoundary["Linux Command Simulator Boundary"]
        Simulator["Linux Command Simulator System<br/>(Flask + Modern Web GUI)<br/>Provides interactive terminal, command taxonomy, and realistic CLI simulation"]
    end
    
    ExtDoc["Linux Manpages & RHCSA Exam Objectives<br/>(Knowledge Reference)"]
    
    User -->|"Explores topics, clicks commands, executes mock shell sessions (HTTP/JSON)"| Simulator
    Simulator -.->|"Curated from standard Red Hat documentation & man-pages"| ExtDoc
```

### 2.2 C4 Level 2: Container Diagram
```mermaid
graph TB
    User["Learner / Browser Client"]

    subgraph LinuxSimulatorContainer["Linux Simulator Application Host"]
        Frontend["Frontend Single Page UI<br/>(HTML5, Vanilla CSS Glassmorphism, Vanilla JS)<br/>Terminal emulator window, 26-chapter sidebar, command cards, inspector drawer"]
        
        WebServer["Flask Application Server<br/>(Python 3 / Flask WSGI)<br/>Routes requests, serves assets, exposes API endpoints"]
        
        CatalogEngine["Command Catalog Store<br/>(Structured Catalog Models)<br/>26 Chapters x 10 Commands with flags, syntax, RHCSA tips, and mock outputs"]
        
        ExecutionEngine["Virtual Shell Simulation Engine<br/>(Python Command Parser)<br/>Parses typed/clicked commands, matches flags, generates realistic outputs, manages mock file system"]
    end

    User -->|"HTTP GET / (Static Assets & HTML)"| WebServer
    WebServer -->|"Delivers rendered interface"| Frontend
    Frontend -->|"REST API: GET /api/topics, /api/commands/<id>"| WebServer
    Frontend -->|"REST API: POST /api/simulate (cmd, args)"| WebServer
    WebServer -->|"Queries command taxonomy & metadata"| CatalogEngine
    WebServer -->|"Evaluates command syntax & generates output"| ExecutionEngine
```

### 2.3 C4 Level 3: Component Diagram
```mermaid
graph TD
    subgraph FrontendComponents["Frontend UI Layer (Browser)"]
        UI_Nav["TopicNavigator Component<br/>(Renders Parts I-IV & 26 Chapters)"]
        UI_Grid["CommandGrid Component<br/>(Displays Top 10 clickable command badges)"]
        UI_Drawer["CommandInspector Component<br/>(Details, flags, description, practical examples)"]
        UI_Terminal["WebTerminal Component<br/>(xterm-style interactive shell with command history & auto-run)"]
        UI_Search["SearchFilter Component<br/>(Instant search across 260 commands and tags)"]
    end

    subgraph BackendComponents["Flask Application Core (Backend)"]
        API_Router["App & Route Controller (app.py)<br/>Handles page rendering and /api/* routes"]
        Service_Catalog["Catalog Service<br/>Loads, validates, and serves 260 command definitions"]
        Service_Simulator["Terminal Simulator Service<br/>Simulates Linux utilities (ls, systemctl, nmcli, podman, etc.)"]
        Service_MockFS["Virtual FS State Manager<br/>Simulates virtual directories (/etc, /var/log, /home, systemd units)"]
    end

    UI_Nav -->|"Select Chapter"| API_Router
    UI_Grid -->|"Click Command"| UI_Drawer
    UI_Grid -->|"Run Command"| UI_Terminal
    UI_Terminal -->|"POST /api/simulate"| API_Router
    UI_Search -->|"GET /api/search?q="| API_Router
    
    API_Router --> Service_Catalog
    API_Router --> Service_Simulator
    Service_Simulator --> Service_MockFS
```

### 2.4 C4 Level 4: Code & Data Model Diagram
```mermaid
classDiagram
    class Topic {
        +int chapter_id
        +string part_title
        +string chapter_title
        +string description
        +List~Command~ commands
        +to_dict() dict
    }

    class Command {
        +string id
        +string name
        +string synopsis
        +string category
        +string short_desc
        +string detailed_desc
        +List~FlagOption~ common_flags
        +string sample_output
        +List~string~ rhcsa_exam_tips
        +List~ExampleUsage~ examples
        +to_dict() dict
    }

    class FlagOption {
        +string flag
        +string argument
        +string explanation
    }

    class ExampleUsage {
        +string command_line
        +string context
        +string expected_output
    }

    class SimulatorEngine {
        +VirtualFileSystem vfs
        +dict command_registry
        +parse(raw_command: str) ParsedCommand
        +execute(raw_command: str) SimulationResult
        +get_auto_completion(buffer: str) list
    }

    class SimulationResult {
        +int exit_code
        +string stdout
        +string stderr
        +string execution_time
    }

    Topic "1" *-- "10" Command : contains
    Command "1" *-- "*" FlagOption : has
    Command "1" *-- "*" ExampleUsage : has
    SimulatorEngine ..> SimulationResult : produces
```

---

## 4. Operational Flowchart

```mermaid
flowchart TD
    Start([User opens Linux Simulator]) --> ViewUI[Dashboard with 26 RHCSA Chapters]
    ViewUI --> UserChoice{User Action}

    %% Path A: Exploring Catalog
    UserChoice -->|Browses Topics| SelectChapter[Select Chapter from Part I-IV]
    SelectChapter --> ShowTop10[Display 10 Curated Command Cards]
    ShowTop10 --> ClickCommand[Click Command Link / Badge]
    ClickCommand --> OpenDrawer[Open Command Inspector Drawer]
    OpenDrawer --> DisplayInfo[Display: Description, Flags, RHCSA Tips, Sample Output]
    DisplayInfo --> ClickRun{"Click 'Try in Terminal'?"}
    ClickRun -->|Yes| PopulateTerminal[Auto-type & execute in Web Terminal]
    ClickRun -->|No| StayDrawer[Continue reading & comparing flags]

    %% Path B: Typing Directly in Terminal
    UserChoice -->|Types command in Terminal| InputCmd[User enters CLI string]
    PopulateTerminal --> ExecPipeline
    InputCmd --> ExecPipeline[Send command string to Simulator API]

    %% Execution Pipeline
    ExecPipeline --> ParseCmd[Parser extracts binary, flags, arguments]
    ParseCmd --> KnownCheck{Is command in Catalog / Engine?}
    KnownCheck -->|Yes| RunSim[Simulator computes realistic output & exit code]
    KnownCheck -->|No| GenericSim[Simulate standard bash output or 'command not found']
    RunSim --> ReturnJSON[Return JSON Response with stdout & exit_code]
    GenericSim --> ReturnJSON
    ReturnJSON --> RenderTerminal[Print formatted output in terminal with colored prompts]
    RenderTerminal --> NextPrompt([Ready for next command])
```

---

## 5. 26-Chapter Section Breakdown & 260 Commands

### Part I: Performing Basic System Management Tasks

| Chapter | Topic Title | 10 Essential Commands Covered |
|---|---|---|
| **Ch 1** | **Installing Red Hat Enterprise Linux** | `hostnamectl`, `timedatectl`, `localectl`, `subscription-manager`, `uname`, `lsblk`, `fdisk`, `cat /etc/os-release`, `grub2-install`, `lscpu` |
| **Ch 2** | **Using Essential Tools** | `man`, `info`, `help`, `which`, `type`, `history`, `clear`, `echo`, `alias`, `date` |
| **Ch 3** | **Essential File Management Tools** | `ls`, `cd`, `pwd`, `cp`, `mv`, `rm`, `mkdir`, `rmdir`, `touch`, `ln` |
| **Ch 4** | **Working with Text Files** | `cat`, `less`, `head`, `tail`, `grep`, `sed`, `awk`, `cut`, `sort`, `wc` |
| **Ch 5** | **Connecting to Red Hat Enterprise Linux 9** | `ssh`, `scp`, `sftp`, `ssh-keygen`, `ssh-copy-id`, `w`, `who`, `last`, `tmux`, `screen` |
| **Ch 6** | **User and Group Management** | `useradd`, `usermod`, `userdel`, `groupadd`, `groupmod`, `groupdel`, `passwd`, `id`, `chage`, `sudo` |
| **Ch 7** | **Permissions Management** | `chmod`, `chown`, `chgrp`, `umask`, `getfacl`, `setfacl`, `ls -l`, `stat`, `chattr`, `lsattr` |
| **Ch 8** | **Configuring Networking** | `ip addr`, `ip route`, `nmcli connection`, `nmcli device`, `nmtui`, `ping`, `traceroute`, `ss`, `dig`, `curl` |

### Part II: Operating Running Systems

| Chapter | Topic Title | 10 Essential Commands Covered |
|---|---|---|
| **Ch 9** | **Managing Software** | `dnf install`, `dnf remove`, `dnf update`, `dnf search`, `dnf repolist`, `dnf module`, `dnf history`, `rpm -qa`, `rpm -ql`, `rpm -qf` |
| **Ch 10** | **Managing Processes** | `ps aux`, `top`, `htop`, `kill`, `killall`, `pkill`, `pgrep`, `nice`, `renice`, `free -h` |
| **Ch 11** | **Working with Systemd** | `systemctl start`, `systemctl stop`, `systemctl enable`, `systemctl status`, `systemctl mask`, `systemctl isolate`, `systemctl daemon-reload`, `systemctl list-units`, `systemd-analyze`, `default-target` |
| **Ch 12** | **Scheduling Tasks** | `crontab -e`, `crontab -l`, `at`, `atq`, `atrm`, `systemd-run`, `systemctl list-timers`, `anacron`, `batch`, `sleep` |
| **Ch 13** | **Configuring Logging** | `journalctl`, `journalctl -u`, `journalctl -xe`, `journalctl -b`, `logger`, `tail -f /var/log/messages`, `tail -f /var/log/secure`, `rsyslogd`, `logrotate`, `dmesg` |
| **Ch 14** | **Managing Storage** | `lsblk`, `fdisk`, `gdisk`, `parted`, `mkfs.xfs`, `mkfs.ext4`, `mount`, `umount`, `blkid`, `df -h` |
| **Ch 15** | **Managing Advanced Storage** | `pvcreate`, `vgcreate`, `lvcreate`, `pvs`, `vgs`, `lvs`, `lvextend`, `lvreduce`, `stratis`, `vdo` |

### Part III: Performing Advanced System Administration Tasks

| Chapter | Topic Title | 10 Essential Commands Covered |
|---|---|---|
| **Ch 16** | **Basic Kernel Management** | `uname -r`, `lsmod`, `modinfo`, `modprobe`, `insmod`, `rmmod`, `sysctl`, `sysctl -p`, `sysctl -a`, `dracut` |
| **Ch 17** | **Managing & Understanding Boot Procedure** | `grub2-mkconfig`, `grub2-editenv`, `systemctl get-default`, `systemctl set-default`, `systemctl emergency`, `systemctl rescue`, `reboot`, `poweroff`, `journalctl -b`, `kexec` |
| **Ch 18** | **Essential Troubleshooting Skills** | `journalctl -p err`, `strace`, `lsof`, `vmstat`, `iostat`, `uptime`, `dmesg -T`, `sosreport`, `tcpdump`, `find / -perm -4000` |
| **Ch 19** | **Bash Shell Scripting & Automation** | `bash`, `chmod +x`, `read`, `test / [ ]`, `expr`, `source`, `export`, `env`, `case`, `for / while` |

### Part IV: Managing Network Services

| Chapter | Topic Title | 10 Essential Commands Covered |
|---|---|---|
| **Ch 20** | **Configuring SSH** | `ssh-keygen -t rsa`, `ssh-copy-id`, `sshd -t`, `cat ~/.ssh/authorized_keys`, `scp`, `sftp`, `ssh -v`, `systemctl restart sshd`, `ssh-add`, `ssh-agent` |
| **Ch 21** | **Managing Apache HTTP Services** | `systemctl status httpd`, `apachectl configtest`, `curl -I localhost`, `firewall-cmd --add-service=http`, `cat /var/log/httpd/access_log`, `cat /var/log/httpd/error_log`, `httpd -v`, `httpd -M`, `semanage port -l`, `restorecon -Rv /var/www/html` |
| **Ch 22** | **Managing SELinux** | `getenforce`, `setenforce`, `sestatus`, `ls -Z`, `ps -eZ`, `semanage fcontext`, `restorecon -v`, `semanage port`, `sealert`, `ausearch` |
| **Ch 23** | **Configuring a Firewall** | `firewall-cmd --state`, `firewall-cmd --get-active-zones`, `firewall-cmd --add-service`, `firewall-cmd --add-port`, `firewall-cmd --permanent`, `firewall-cmd --reload`, `firewall-cmd --list-all`, `firewall-cmd --remove-service`, `iptables-save`, `nft list ruleset` |
| **Ch 24** | **Accessing Network Storage (NFS/CIFS)** | `mount -t nfs`, `showmount -e`, `exportfs -v`, `cat /etc/exports`, `smbclient -L`, `mount -t cifs`, `systemctl status autofs`, `systemctl status nfs-server`, `rpcinfo -p`, `df -hT` |
| **Ch 25** | **Configuring Time Services** | `chronyc sources -v`, `chronyc tracking`, `chronyc sourcestats`, `timedatectl status`, `timedatectl set-ntp true`, `systemctl status chronyd`, `cat /etc/chrony.conf`, `hwclock`, `date -R`, `tzselect` |
| **Ch 26** | **Managing Containers with Podman** | `podman run`, `podman ps -a`, `podman images`, `podman pull`, `podman stop`, `podman rm`, `podman generate systemd`, `podman volume ls`, `podman build`, `skopeo inspect` |


---

## 6. Project Directory Structure
```
Linux-command/
├── README.md                      # Architecture, C4 diagrams, and curriculum
├── requirements.txt               # Flask dependencies
├── app.py                         # Main Flask application and REST routes
├── data/
│   ├── __init__.py
│   └── commands_data.py           # 26 chapters x 10 commands knowledge database
├── services/
│   ├── __init__.py
│   ├── catalog_service.py         # Topic catalog and search
│   └── simulator_service.py       # Simulation parser and mock terminal executor
├── static/
│   ├── css/
│   │   └── style.css              # Dark glassmorphic modern UI
│   └── js/
│       └── app.js                 # Terminal emulation & interactive drawer UI
└── templates/
    └── index.html                 # Main dashboard interface
```
