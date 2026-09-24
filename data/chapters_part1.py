"""
Part I: Performing Basic System Management Tasks (Chapters 1 - 8)
10 Essential Commands per Chapter (80 commands total)
"""

PART_1_CHAPTERS = [
    # CHAPTER 1: Installing Red Hat Enterprise Linux
    {
        "chapter_id": 1,
        "part_id": 1,
        "part_title": "Part I: Performing Basic System Management Tasks",
        "chapter_title": "Installing Red Hat Enterprise Linux",
        "description": "Essential utilities for post-installation setup, system identification, and foundational hardware/OS queries.",
        "commands": [
            {
                "id": "ch1_hostnamectl",
                "name": "hostnamectl",
                "synopsis": "hostnamectl [OPTIONS...] COMMAND ...",
                "short_desc": "Control and query the system hostname and related settings.",
                "detailed_desc": "hostnamectl is the modern systemd utility used to query and change the system hostname and related machine metadata (transient, static, and pretty hostnames).",
                "category": "System Identification",
                "common_flags": [
                    {"flag": "status", "desc": "Show current system hostname and system architecture metadata (default)."},
                    {"flag": "set-hostname <NAME>", "desc": "Set the system hostname permanently across reboots."},
                    {"flag": "--static", "desc": "Only operate on the static hostname stored in /etc/hostname."},
                    {"flag": "--pretty", "desc": "Set a high-level descriptive UTF-8 hostname for display."}
                ],
                "sample_output": """ Static hostname: rhel9-node1.example.com
       Icon name: computer-vm
         Chassis: vm 🖴
      Machine ID: d4e1c278923a4bf88a6d9124fb7e0123
         Boot ID: 17b2f69e4f5a4358a9e701982b61cd77
  Virtualization: kvm
Operating System: Red Hat Enterprise Linux 9.2 (Plow)
     CPE OS Name: cpe:/o:redhat:enterprise_linux:9::baseos
          Kernel: Linux 5.14.0-284.11.1.el9_2.x86_64
    Architecture: x86-64
 Hardware Vendor: Red Hat
  Hardware Model: KVM""",
                "rhcsa_tips": [
                    "RHCSA frequently asks to configure a fully qualified domain name (FQDN). Always use 'hostnamectl set-hostname serverX.example.com'.",
                    "Changes made with hostnamectl immediately persist in '/etc/hostname' without needing a reboot."
                ],
                "default_run_cmd": "hostnamectl status"
            },
            {
                "id": "ch1_timedatectl",
                "name": "timedatectl",
                "synopsis": "timedatectl [OPTIONS...] COMMAND ...",
                "short_desc": "Control the system time and date settings.",
                "detailed_desc": "Query and alter the system clock, time zone, and NTP network time synchronization configuration.",
                "category": "System Time",
                "common_flags": [
                    {"flag": "status", "desc": "Display current time, RTC time, time zone, and NTP sync status."},
                    {"flag": "set-timezone <ZONE>", "desc": "Change system timezone (e.g., America/New_York)."},
                    {"flag": "list-timezones", "desc": "List all supported IANA time zones."},
                    {"flag": "set-ntp true/false", "desc": "Enable or disable network time synchronization (chronyd)."}
                ],
                "sample_output": """               Local time: Wed 2026-09-24 17:35:12 EDT
           Universal time: Wed 2026-09-24 21:35:12 UTC
                 RTC time: Wed 2026-09-24 21:35:12
                Time zone: America/New_York (EDT, -0400)
System clock synchronized: yes
              NTP service: active
          RTC in local TZ: no""",
                "rhcsa_tips": [
                    "Use 'timedatectl list-timezones | grep -i <city>' to quickly locate the correct timezone string in exam scenarios.",
                    "Verify NTP synchronization status with 'timedatectl status'."
                ],
                "default_run_cmd": "timedatectl status"
            },
            {
                "id": "ch1_localectl",
                "name": "localectl",
                "synopsis": "localectl [OPTIONS...] COMMAND ...",
                "short_desc": "Control the system locale and keyboard layout settings.",
                "detailed_desc": "Manages system locale (LANG, LC_MESSAGES) and keymaps for console and graphical environments.",
                "category": "Locale & Input",
                "common_flags": [
                    {"flag": "status", "desc": "Show current locale and keymap settings."},
                    {"flag": "set-locale LANG=<LOCALE>", "desc": "Set the primary system locale (e.g. en_US.UTF-8)."},
                    {"flag": "list-locales", "desc": "Display all available installed system locales."}
                ],
                "sample_output": """   System Locale: LANG=en_US.UTF-8
       VC Keymap: us
      X11 Layout: us""",
                "rhcsa_tips": ["Check /etc/locale.conf if manual verification of system locale is required."],
                "default_run_cmd": "localectl status"
            },
            {
                "id": "ch1_uname",
                "name": "uname",
                "synopsis": "uname [OPTION]...",
                "short_desc": "Print system and kernel architecture information.",
                "detailed_desc": "Prints basic operating system name, kernel release, machine hardware name, and processor architecture.",
                "category": "Kernel Info",
                "common_flags": [
                    {"flag": "-a, --all", "desc": "Print all available system information in sequence."},
                    {"flag": "-r, --kernel-release", "desc": "Print the current kernel release version."},
                    {"flag": "-m, --machine", "desc": "Print the machine hardware architecture (e.g., x86_64)."}
                ],
                "sample_output": "Linux rhel9-node1.example.com 5.14.0-284.11.1.el9_2.x86_64 #1 SMP PREEMPT_DYNAMIC Wed Apr 12 10:45:03 EDT 2023 x86_64 x86_64 x86_64 GNU/Linux",
                "rhcsa_tips": ["Use 'uname -r' when building kernel modules or verifying newly updated kernels after reboot."],
                "default_run_cmd": "uname -a"
            },
            {
                "id": "ch1_lsblk",
                "name": "lsblk",
                "synopsis": "lsblk [options] [device...]",
                "short_desc": "List information about block devices in a tree structure.",
                "detailed_desc": "Provides a clean hierarchical view of hard disks, SSDs, partitions, LVM logical volumes, and mount points.",
                "category": "Storage Query",
                "common_flags": [
                    {"flag": "-f, --fs", "desc": "Output info about filesystems (UUID, type, mountpoint, label)."},
                    {"flag": "-m, --perms", "desc": "Output permissions and device ownership."}
                ],
                "sample_output": """NAME          MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
vda           252:0    0   40G  0 disk 
├─vda1        252:1    0    1G  0 part /boot
└─vda2        252:2    0   39G  0 part 
  ├─rhel-root 253:0    0   35G  0 lvm  /
  └─rhel-swap 253:1    0    4G  0 lvm  [SWAP]
vdb           252:16   0   10G  0 disk """,
                "rhcsa_tips": ["Always run 'lsblk -f' before and after formatting partitions to double check filesystem UUIDs and types."],
                "default_run_cmd": "lsblk -f"
            },
            {
                "id": "ch1_fdisk",
                "name": "fdisk",
                "synopsis": "fdisk [options] <disk>",
                "short_desc": "Manipulate disk partition tables (MBR/GPT).",
                "detailed_desc": "Interactive menu-driven tool for viewing, creating, deleting, and modifying disk partitions.",
                "category": "Partitioning",
                "common_flags": [
                    {"flag": "-l, --list", "desc": "List the partition tables for specified devices or all devices."},
                    {"flag": "/dev/vdb", "desc": "Open interactive partition editor on target drive."}
                ],
                "sample_output": """Disk /dev/vda: 40 GiB, 42949672960 bytes, 83886080 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: 7F69AC1D-4BC2-4F18-BF5C-74EA7FE170B2

Device       Start      End  Sectors Size Type
/dev/vda1     2048  2099199  2097152   1G Linux filesystem
/dev/vda2  2099200 83884031 81784832  39G Linux LVM""",
                "rhcsa_tips": ["Remember to write changes with 'w' inside interactive fdisk and run 'partprobe' to refresh kernel partition tables."],
                "default_run_cmd": "fdisk -l"
            },
            {
                "id": "ch1_cat_os_release",
                "name": "cat /etc/os-release",
                "synopsis": "cat /etc/os-release",
                "short_desc": "View operating system identification and release details.",
                "detailed_desc": "Displays standard system identification variables defined by systemd, including RHEL version, ID, and support URLs.",
                "category": "OS Identification",
                "common_flags": [],
                "sample_output": """NAME="Red Hat Enterprise Linux"
VERSION="9.2 (Plow)"
ID="rhel"
ID_LIKE="fedora"
VERSION_ID="9.2"
PLATFORM_ID="platform:el9"
PRETTY_NAME="Red Hat Enterprise Linux 9.2 (Plow)"
ANSI_COLOR="0;31"
LOGO="fedora-logo-icon"
CPE_NAME="cpe:/o:redhat:enterprise_linux:9::baseos"
HOME_URL="https://www.redhat.com/"
DOCUMENTATION_URL="https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9"
REDHAT_BUGZILLA_PRODUCT="Red Hat Enterprise Linux 9"
REDHAT_SUPPORT_PRODUCT="Red Hat Enterprise Linux"
REDHAT_SUPPORT_PRODUCT_VERSION="9.2\"""",
                "rhcsa_tips": ["Fastest way to confirm the exact minor version in automated test environments."],
                "default_run_cmd": "cat /etc/os-release"
            },
            {
                "id": "ch1_subscription_manager",
                "name": "subscription-manager",
                "synopsis": "subscription-manager [options] [command]",
                "short_desc": "Manage Red Hat software subscriptions and repositories.",
                "detailed_desc": "Registers the system with the Red Hat Customer Portal or Red Hat Satellite and attaches content entitlements.",
                "category": "System Registration",
                "common_flags": [
                    {"flag": "status", "desc": "Check the current subscription registration state."},
                    {"flag": "register", "desc": "Register the node with Red Hat Network."},
                    {"flag": "repos --list-enabled", "desc": "List all active subscribed repositories."}
                ],
                "sample_output": """+-------------------------------------------+
   System Status Details
+-------------------------------------------+
Overall Status: Current
Content Access Mode: Simple Content Access

System Name: rhel9-node1.example.com
Registered: Yes
Product Name: Red Hat Enterprise Linux for x86_64
Status: Subscribed""",
                "rhcsa_tips": ["Local repos are usually pre-configured in /etc/yum.repos.d/ on exam workstations."],
                "default_run_cmd": "subscription-manager status"
            },
            {
                "id": "ch1_lscpu",
                "name": "lscpu",
                "synopsis": "lscpu [options]",
                "short_desc": "Display information on CPU architecture and virtualization.",
                "detailed_desc": "Gathers CPU architecture information from sysfs and /proc/cpuinfo, including core count and hyperthreading.",
                "category": "Hardware Inspection",
                "common_flags": [
                    {"flag": "-e, --extended", "desc": "Show information in human-friendly columns."}
                ],
                "sample_output": """Architecture:            x86_64
  CPU op-mode(s):        32-bit, 64-bit
  Address sizes:         39 bits physical, 48 bits virtual
  Byte Order:            Little Endian
CPU(s):                  4
  On-line CPU(s) list:   0-3
Vendor ID:               GenuineIntel
  Model name:            Intel(R) Xeon(R) CPU E5-2680 v4 @ 2.40GHz
Virtualization features: 
  Hypervisor vendor:     KVM""",
                "rhcsa_tips": ["Useful to verify hardware virtualization extensions (VT-x/AMD-V) when configuring containers."],
                "default_run_cmd": "lscpu"
            },
            {
                "id": "ch1_grub2_install",
                "name": "grub2-install",
                "synopsis": "grub2-install [OPTION...] [INSTALL_DEVICE]",
                "short_desc": "Install GRUB on your drive for BIOS/UEFI bootloading.",
                "detailed_desc": "Installs GRUB boot files and bootloader code to the designated storage device.",
                "category": "Bootloader Setup",
                "common_flags": [
                    {"flag": "--target=...", "desc": "Specify install target (e.g. i386-pc or x86_64-efi)."},
                    {"flag": "--recheck", "desc": "Probe device map even if it already exists."}
                ],
                "sample_output": """Installing for i386-pc platform.
Installation finished. No error reported.""",
                "rhcsa_tips": ["On modern RHEL 9 UEFI systems, grub configuration is typically rebuilt with grub2-mkconfig."],
                "default_run_cmd": "grub2-install --version"
            }
        ]
    },

    # CHAPTER 2: Using Essential Tools
    {
        "chapter_id": 2,
        "part_id": 1,
        "part_title": "Part I: Performing Basic System Management Tasks",
        "chapter_title": "Using Essential Tools",
        "description": "Foundational shell utilities, documentation navigation, command history, and aliases.",
        "commands": [
            {
                "id": "ch2_man",
                "name": "man",
                "synopsis": "man [SECTION] [PAGE]",
                "short_desc": "Format and display the on-line manual documentation pages.",
                "detailed_desc": "The primary documentation utility in Linux. Sections: 1 (Commands), 5 (File formats), 8 (System admin commands).",
                "category": "Documentation",
                "common_flags": [
                    {"flag": "-k <KEYWORD>", "desc": "Search apropos database for keywords matching summaries."},
                    {"flag": "5 <FILE>", "desc": "Read manual specifically for a configuration file format (e.g., man 5 crontab)."}
                ],
                "sample_output": """MAN(1)                        Manual pager utils                       MAN(1)

NAME
       man - an interface to the system reference manuals

SYNOPSIS
       man [man options] [[section] page ...] ...""",
                "rhcsa_tips": ["CRITICAL FOR RHCSA: If you forget syntax, 'man 5 <config-file>' provides full configuration syntax examples."],
                "default_run_cmd": "man ls | head -n 20"
            },
            {
                "id": "ch2_info",
                "name": "info",
                "synopsis": "info [OPTION]... [MENU-ITEM...]",
                "short_desc": "Read comprehensive GNU hypertext info documentation.",
                "detailed_desc": "Navigates multi-page GNU documentation structures that provide deeper tutorials than standard manpages.",
                "category": "Documentation",
                "common_flags": [{"flag": "--subnodes", "desc": "Recursively dump all menu items to standard output."}],
                "sample_output": "Coreutils documents version 8.32 of GNU core utilities for text and file manipulation.",
                "rhcsa_tips": ["For coreutils utilities like sed, coreutils info pages provide full script examples."],
                "default_run_cmd": "info coreutils | head -n 15"
            },
            {
                "id": "ch2_which",
                "name": "which",
                "synopsis": "which [options] [--] programname...",
                "short_desc": "Locate a command executable binary path in $PATH.",
                "detailed_desc": "Returns the exact absolute path that will be executed for a given command name based on the current user's $PATH variable.",
                "category": "Command Inspection",
                "common_flags": [{"flag": "-a", "desc": "Print all matching pathnames in PATH."}],
                "sample_output": "/usr/bin/python3",
                "rhcsa_tips": ["Use which when writing systemd service unit files or cron jobs that require absolute paths."],
                "default_run_cmd": "which systemctl"
            },
            {
                "id": "ch2_type",
                "name": "type",
                "synopsis": "type [-afptP] name [name ...]",
                "short_desc": "Determine how a command name is interpreted by the bash shell.",
                "detailed_desc": "Identifies if a command is a bash built-in, an alias, a shell function, or an external disk executable.",
                "category": "Command Inspection",
                "common_flags": [{"flag": "-a", "desc": "Display all locations containing the specified executable."}],
                "sample_output": "cd is a shell builtin\nls is aliased to `ls --color=auto'\nvim is /usr/bin/vim",
                "rhcsa_tips": ["Explains why 'man cd' might refer you to BASH_BUILTINS(1)."],
                "default_run_cmd": "type -a ls"
            },
            {
                "id": "ch2_history",
                "name": "history",
                "synopsis": "history [-c] [-d offset] [n]",
                "short_desc": "Display or manipulate the shell command history list.",
                "detailed_desc": "Displays previous commands executed in the session. Supports rerun with !<number>.",
                "category": "Shell Navigation",
                "common_flags": [{"flag": "-c", "desc": "Clear history list."}],
                "sample_output": "  101  nmcli connection show\n  102  firewall-cmd --list-all\n  103  systemctl status httpd",
                "rhcsa_tips": ["Use '!102' to rerun command 102 quickly without retyping long arguments."],
                "default_run_cmd": "history | tail -n 10"
            },
            {
                "id": "ch2_clear",
                "name": "clear",
                "synopsis": "clear",
                "short_desc": "Clear the terminal screen.",
                "detailed_desc": "Clears terminal buffer and repositions the cursor to the top-left of the display.",
                "category": "Terminal Utility",
                "common_flags": [],
                "sample_output": "[Terminal screen cleared]",
                "rhcsa_tips": ["Shortcut: Ctrl + L clears the screen in any bash shell."],
                "default_run_cmd": "clear"
            },
            {
                "id": "ch2_echo",
                "name": "echo",
                "synopsis": "echo [SHORT-OPTION]... [STRING]...",
                "short_desc": "Display a line of text or variable values.",
                "detailed_desc": "Echoes text strings or shell environment variables ($PATH, $USER) to standard output.",
                "category": "Shell Utility",
                "common_flags": [{"flag": "-e", "desc": "Enable interpretation of backslash escapes (\\n, \\t)."}],
                "sample_output": "Red Hat Enterprise Linux 9 Systems Administration",
                "rhcsa_tips": ["Frequently used with redirection: 'echo \"welcome\" > /var/www/html/index.html'."],
                "default_run_cmd": "echo \"System Kernel: $(uname -r)\""
            },
            {
                "id": "ch2_alias",
                "name": "alias",
                "synopsis": "alias [name[=value] ... ]",
                "short_desc": "Create command shortcuts or view current shell aliases.",
                "detailed_desc": "Defines custom abbreviated names for complex or frequently used commands.",
                "category": "Shell Customization",
                "common_flags": [{"flag": "-p", "desc": "Print all defined aliases in reusable format."}],
                "sample_output": "alias ll='ls -l --color=auto'\nalias ls='ls --color=auto'",
                "rhcsa_tips": ["To persist aliases across reboots, add them to '~/.bashrc' or '/etc/profile.d/'."],
                "default_run_cmd": "alias"
            },
            {
                "id": "ch2_date",
                "name": "date",
                "synopsis": "date [OPTION]... [+FORMAT]",
                "short_desc": "Display or set the system date and time.",
                "detailed_desc": "Displays current timestamp formatted to custom specifiers or sets the system clock.",
                "category": "Time & Date",
                "common_flags": [{"flag": "+%F_%T", "desc": "Format date as YYYY-MM-DD_HH:MM:SS for automated log stamps."}],
                "sample_output": "Wed Sep 24 17:36:00 EDT 2026",
                "rhcsa_tips": ["Useful in backup scripts: 'tar -czf /backup/etc_$(date +%F).tar.gz /etc'."],
                "default_run_cmd": "date '+%Y-%m-%d %H:%M:%S %Z'"
            },
            {
                "id": "ch2_help",
                "name": "help",
                "synopsis": "help [-dms] [pattern ...]",
                "short_desc": "Display information about builtin bash commands.",
                "detailed_desc": "Built-in documentation tool specifically for bash builtins like cd, export, umask, and read.",
                "category": "Documentation",
                "common_flags": [{"flag": "-s", "desc": "Output only a short usage synopsis for each pattern matching command."}],
                "sample_output": "cd: cd [-L|[-P [-e]]] [dir]\n    Change the shell working directory.",
                "rhcsa_tips": ["When 'man cd' fails to explain specific builtin flags, 'help cd' or 'help read' provides instant assistance."],
                "default_run_cmd": "help umask"
            }
        ]
    },

    # CHAPTER 3: Essential File Management Tools
    {
        "chapter_id": 3,
        "part_id": 1,
        "part_title": "Part I: Performing Basic System Management Tasks",
        "chapter_title": "Essential File Management Tools",
        "description": "Navigation, directory operations, copying, moving, linking, and file removal.",
        "commands": [
            {
                "id": "ch3_ls",
                "name": "ls",
                "synopsis": "ls [OPTION]... [FILE]...",
                "short_desc": "List directory contents with metadata and file attributes.",
                "detailed_desc": "Displays permissions, links, owner, group, size, and timestamp for directory items.",
                "category": "File Navigation",
                "common_flags": [
                    {"flag": "-l", "desc": "Use a long listing format with permissions, ownership, and size."},
                    {"flag": "-a, --all", "desc": "Do not ignore entries starting with . (hidden files)."},
                    {"flag": "-h", "desc": "With -l, print sizes like 1K 234M 2G."}
                ],
                "sample_output": """total 16
drwxr-xr-x. 2 root root 4096 Sep 24 10:15 bin
drwxr-xr-x. 4 root root 4096 Sep 24 10:20 config
-rw-r--r--. 1 root root  820 Sep 24 10:22 notes.txt""",
                "rhcsa_tips": ["Combine flags: 'ls -laZ' displays long listing including SELinux security contexts."],
                "default_run_cmd": "ls -lah /etc | head -n 12"
            },
            {
                "id": "ch3_cd",
                "name": "cd",
                "synopsis": "cd [-L|[-P [-e]]] [dir]",
                "short_desc": "Change the current working shell directory.",
                "detailed_desc": "Navigates between directories in the filesystem hierarchy.",
                "category": "Navigation",
                "common_flags": [
                    {"flag": "-", "desc": "Switch back to the previous working directory ($OLDPWD)."},
                    {"flag": "~", "desc": "Navigate directly to current user's home directory ($HOME)."}
                ],
                "sample_output": "/etc/systemd/system",
                "rhcsa_tips": ["'cd -' is great for rapid toggling between two deeply nested directories."],
                "default_run_cmd": "pwd && cd /var/log && pwd"
            },
            {
                "id": "ch3_pwd",
                "name": "pwd",
                "synopsis": "pwd [OPTION]...",
                "short_desc": "Print the current working directory path.",
                "detailed_desc": "Returns the exact full pathname of the current working directory.",
                "category": "Navigation",
                "common_flags": [{"flag": "-P", "desc": "Print the physical directory, resolving all symbolic links."}],
                "sample_output": "/home/student/lab-workspace",
                "rhcsa_tips": ["Use 'pwd -P' when you are inside a symlinked path and need to verify the real partition."],
                "default_run_cmd": "pwd"
            },
            {
                "id": "ch3_cp",
                "name": "cp",
                "synopsis": "cp [OPTION]... SOURCE... DIRECTORY",
                "short_desc": "Copy files and directories.",
                "detailed_desc": "Copies files and full directory trees with options to preserve timestamps, ownership, and file modes.",
                "category": "File Operations",
                "common_flags": [
                    {"flag": "-r, -R, --recursive", "desc": "Copy directories recursively."},
                    {"flag": "-p", "desc": "Preserve mode, ownership, and timestamps."},
                    {"flag": "-a, --archive", "desc": "Archive mode; preserves everything including symlinks and SELinux contexts."}
                ],
                "sample_output": "cp: copied '/etc/hosts' to '/tmp/hosts.bak'",
                "rhcsa_tips": ["RHCSA exam golden rule: When backing up configuration files before modifying them, use 'cp -p /etc/foo.conf /etc/foo.conf.bak'!"],
                "default_run_cmd": "cp -v /etc/hosts /tmp/hosts.sample"
            },
            {
                "id": "ch3_mv",
                "name": "mv",
                "synopsis": "mv [OPTION]... SOURCE... DIRECTORY",
                "short_desc": "Move or rename files and directories.",
                "detailed_desc": "Moves files between paths or renames files without modifying the underlying inode when on the same filesystem.",
                "category": "File Operations",
                "common_flags": [
                    {"flag": "-i, --interactive", "desc": "Prompt before overwriting existing destination files."},
                    {"flag": "-f, --force", "desc": "Do not prompt before overwriting."}
                ],
                "sample_output": "renamed 'draft_report.txt' -> 'final_report.txt'",
                "rhcsa_tips": ["Moving a file maintains its origin SELinux context, whereas cp creates a file inheriting destination context."],
                "default_run_cmd": "mv -v /tmp/hosts.sample /tmp/hosts.renamed"
            },
            {
                "id": "ch3_rm",
                "name": "rm",
                "synopsis": "rm [OPTION]... [FILE]...",
                "short_desc": "Remove files or directories.",
                "detailed_desc": "Unlinks files from directory entries and deletes files permanently.",
                "category": "File Operations",
                "common_flags": [
                    {"flag": "-r, -R, --recursive", "desc": "Remove directories and their contents recursively."},
                    {"flag": "-f, --force", "desc": "Ignore nonexistent files, never prompt."}
                ],
                "sample_output": "removed '/tmp/temp_cache.log'",
                "rhcsa_tips": ["Double-check absolute paths before running 'rm -rf'!"],
                "default_run_cmd": "rm -v /tmp/hosts.renamed"
            },
            {
                "id": "ch3_mkdir",
                "name": "mkdir",
                "synopsis": "mkdir [OPTION]... DIRECTORY...",
                "short_desc": "Create new directories.",
                "detailed_desc": "Creates one or more directory paths if they do not already exist.",
                "category": "File Operations",
                "common_flags": [
                    {"flag": "-p, --parents", "desc": "Make parent directories as needed without error if existing."},
                    {"flag": "-m, --mode=MODE", "desc": "Set file permission mode during creation."}
                ],
                "sample_output": "mkdir: created directory '/opt/rhcsa/data/shared'",
                "rhcsa_tips": ["Always use 'mkdir -p' in scripts and exam questions requiring deep path creation."],
                "default_run_cmd": "mkdir -p -v /tmp/test_rhcsa_dir/sub1/sub2"
            },
            {
                "id": "ch3_rmdir",
                "name": "rmdir",
                "synopsis": "rmdir [OPTION]... DIRECTORY...",
                "short_desc": "Remove EMPTY directories.",
                "detailed_desc": "Safely removes designated directory only if it contains no files or subdirectories.",
                "category": "File Operations",
                "common_flags": [{"flag": "-p, --parents", "desc": "Remove DIRECTORY and its ancestors that become empty."}],
                "sample_output": "rmdir: removing directory, '/tmp/empty_folder'",
                "rhcsa_tips": ["rmdir protects against accidental mass deletion because it fails if files are inside."],
                "default_run_cmd": "rmdir -p -v /tmp/test_rhcsa_dir/sub1/sub2"
            },
            {
                "id": "ch3_touch",
                "name": "touch",
                "synopsis": "touch [OPTION]... FILE...",
                "short_desc": "Update file timestamps or create empty files.",
                "detailed_desc": "Updates access and modification timestamps of files; creates empty file if it does not exist.",
                "category": "File Operations",
                "common_flags": [
                    {"flag": "-a", "desc": "Change only access time."},
                    {"flag": "-m", "desc": "Change only modification time."}
                ],
                "sample_output": "touch: created empty file 'server.lock'",
                "rhcsa_tips": ["Quickest way to create test dummy files for permissions or storage practice."],
                "default_run_cmd": "touch /tmp/rhcsa_test_file.txt && ls -l /tmp/rhcsa_test_file.txt"
            },
            {
                "id": "ch3_ln",
                "name": "ln",
                "synopsis": "ln [OPTION]... [-T] TARGET LINK_NAME",
                "short_desc": "Make links between files (symbolic or hard).",
                "detailed_desc": "Creates symbolic (soft) links or hard links sharing the same inode number.",
                "category": "File Linking",
                "common_flags": [
                    {"flag": "-s, --symbolic", "desc": "Make symbolic links instead of hard links."},
                    {"flag": "-f, --force", "desc": "Remove existing destination files before linking."}
                ],
                "sample_output": "lrwxrwxrwx. 1 root root 22 Sep 24 17:40 /var/www/site -> /opt/apps/webapp",
                "rhcsa_tips": ["Always use absolute paths for target when creating symlinks: 'ln -s /etc/hosts /tmp/hosts-symlink'."],
                "default_run_cmd": "ln -s -v /etc/issue /tmp/issue-symlink && ls -l /tmp/issue-symlink"
            }
        ]
    },

    # CHAPTER 4: Working with Text Files
    {
        "chapter_id": 4,
        "part_id": 1,
        "part_title": "Part I: Performing Basic System Management Tasks",
        "chapter_title": "Working with Text Files",
        "description": "Viewing, searching, filtering, and manipulating text streams and configuration files.",
        "commands": [
            {
                "id": "ch4_cat",
                "name": "cat",
                "synopsis": "cat [OPTION]... [FILE]...",
                "short_desc": "Concatenate files and print on standard output.",
                "detailed_desc": "Reads files sequentially and writes them to standard output.",
                "category": "Text Display",
                "common_flags": [{"flag": "-n", "desc": "Number all output lines starting from 1."}],
                "sample_output": "     1	127.0.0.1   localhost\n     2	::1         localhost",
                "rhcsa_tips": ["Use 'cat -n' to inspect line numbers for exam questions asking to edit specific line ranges."],
                "default_run_cmd": "cat -n /etc/hosts"
            },
            {
                "id": "ch4_less",
                "name": "less",
                "synopsis": "less [OPTION] [FILE]...",
                "short_desc": "View file contents with interactive forward/backward navigation.",
                "detailed_desc": "High-performance pager allowing forward and backward navigation and pattern searching (/pattern).",
                "category": "Text Pager",
                "common_flags": [{"flag": "-N", "desc": "Show line numbers on each page."}],
                "sample_output": "[Viewing file with less - press 'q' to exit]",
                "rhcsa_tips": ["Inside less, type '/pattern' to search forward, 'n' for next occurrence, 'N' for previous."],
                "default_run_cmd": "less -N /etc/passwd"
            },
            {
                "id": "ch4_head",
                "name": "head",
                "synopsis": "head [OPTION]... [FILE]...",
                "short_desc": "Output the first part of files.",
                "detailed_desc": "Outputs the beginning (first 10 lines by default) of specified text files.",
                "category": "Text Filtering",
                "common_flags": [{"flag": "-n <N>", "desc": "Print the first N lines instead of the default 10."}],
                "sample_output": "root:x:0:0:root:/root:/bin/bash\nbin:x:1:1:bin:/bin:/sbin/nologin",
                "rhcsa_tips": ["Combine with tail: 'head -n 20 /file | tail -n 5' extracts lines 16 through 20."],
                "default_run_cmd": "head -n 5 /etc/passwd"
            },
            {
                "id": "ch4_tail",
                "name": "tail",
                "synopsis": "tail [OPTION]... [FILE]...",
                "short_desc": "Output the last part of files or follow files in real-time.",
                "detailed_desc": "Outputs the end of files or live streams incoming appended lines.",
                "category": "Text Filtering",
                "common_flags": [
                    {"flag": "-n <N>", "desc": "Output the last N lines."},
                    {"flag": "-f, --follow", "desc": "Loop and output appended data as the file grows."}
                ],
                "sample_output": "Sep 24 17:42:15 rhel9-node1 systemd-logind[900]: New session 12 of user student.",
                "rhcsa_tips": ["'tail -f /var/log/messages' is the classic troubleshooting live-view."],
                "default_run_cmd": "tail -n 6 /var/log/messages"
            },
            {
                "id": "ch4_grep",
                "name": "grep",
                "synopsis": "grep [OPTIONS] PATTERN [FILE...]",
                "short_desc": "Print lines matching a pattern or regular expression.",
                "detailed_desc": "Searches input files for lines matching a regular expression.",
                "category": "Text Search",
                "common_flags": [
                    {"flag": "-i, --ignore-case", "desc": "Ignore case distinctions."},
                    {"flag": "-v, --invert-match", "desc": "Select non-matching lines (invert filter)."},
                    {"flag": "-E, --extended-regexp", "desc": "Interpret PATTERN as extended regular expression."}
                ],
                "sample_output": "student:x:1000:1000:Student User:/home/student:/bin/bash",
                "rhcsa_tips": ["Filter out comments and blank lines: 'grep -vE '^#|^$' /etc/named.conf'."],
                "default_run_cmd": "grep -E 'bash$' /etc/passwd"
            },
            {
                "id": "ch4_sed",
                "name": "sed",
                "synopsis": "sed [OPTION]... {script} [input-file]...",
                "short_desc": "Stream editor for filtering and transforming text.",
                "detailed_desc": "Performs basic text transformations on an input stream or file.",
                "category": "Stream Processing",
                "common_flags": [
                    {"flag": "-i", "desc": "Edit files in place."},
                    {"flag": "s/regexp/replacement/g", "desc": "Globally substitute matching patterns."}
                ],
                "sample_output": "[sed modified: 'SELINUX=enforcing' -> 'SELINUX=permissive']",
                "rhcsa_tips": ["'sed -i 's/SELINUX=enforcing/SELINUX=permissive/g' /etc/selinux/config' is a rapid in-place modifier."],
                "default_run_cmd": "sed 's/root/SUPERUSER/g' /etc/passwd | head -n 3"
            },
            {
                "id": "ch4_awk",
                "name": "awk",
                "synopsis": "awk [options] 'program' file",
                "short_desc": "Pattern scanning and processing language for columnar data.",
                "detailed_desc": "Extracts and reformats structured fields effortlessly.",
                "category": "Data Processing",
                "common_flags": [{"flag": "-F <FS>", "desc": "Define input field separator (e.g. -F: for /etc/passwd)."}],
                "sample_output": "Username: root | UID: 0 | Shell: /bin/bash",
                "rhcsa_tips": ["'awk -F: '$3 >= 1000 {print $1, $3}' /etc/passwd' filters regular users."],
                "default_run_cmd": "awk -F: '{print \"User: \" $1 \"\\tShell: \" $7}' /etc/passwd | head -n 6"
            },
            {
                "id": "ch4_cut",
                "name": "cut",
                "synopsis": "cut OPTION... [FILE]...",
                "short_desc": "Remove sections from each line of files by delimiter.",
                "detailed_desc": "Slices delimited columns or byte ranges from text inputs.",
                "category": "Text Filtering",
                "common_flags": [
                    {"flag": "-d <DELIM>", "desc": "Use DELIM instead of TAB."},
                    {"flag": "-f <LIST>", "desc": "Select only these fields."}
                ],
                "sample_output": "root:/bin/bash\nstudent:/bin/bash",
                "rhcsa_tips": ["'cut -d: -f1 /etc/passwd' produces a clean single-column list of all users."],
                "default_run_cmd": "cut -d: -f1,7 /etc/passwd | head -n 5"
            },
            {
                "id": "ch4_sort",
                "name": "sort",
                "synopsis": "sort [OPTION]... [FILE]...",
                "short_desc": "Sort lines of text files alphabetically or numerically.",
                "detailed_desc": "Sorts lines of text, supporting numeric evaluation and column selection.",
                "category": "Text Manipulation",
                "common_flags": [
                    {"flag": "-n, --numeric-sort", "desc": "Compare numerically."},
                    {"flag": "-u, --unique", "desc": "Output only first of an equal run."}
                ],
                "sample_output": "0:root\n1000:student",
                "rhcsa_tips": ["Pipe with uniq: 'sort data.txt | uniq -c' counts frequency."],
                "default_run_cmd": "sort -t: -k3 -n /etc/passwd | head -n 5"
            },
            {
                "id": "ch4_wc",
                "name": "wc",
                "synopsis": "wc [OPTION]... [FILE]...",
                "short_desc": "Print newline, word, and byte counts for each file.",
                "detailed_desc": "Counts lines (-l), words (-w), and characters/bytes (-c).",
                "category": "Text Metrics",
                "common_flags": [{"flag": "-l, --lines", "desc": "Print only newline counts."}],
                "sample_output": "48 /etc/passwd",
                "rhcsa_tips": ["Use 'rpm -qa | wc -l' to quickly count installed packages."],
                "default_run_cmd": "wc -l /etc/passwd"
            }
        ]
    },

    # CHAPTER 5: Connecting to RHEL 9
    {
        "chapter_id": 5,
        "part_id": 1,
        "part_title": "Part I: Performing Basic System Management Tasks",
        "chapter_title": "Connecting to Red Hat Enterprise Linux 9",
        "description": "Remote OpenSSH administration, secure file transfers, and multi-terminal session management.",
        "commands": [
            {
                "id": "ch5_ssh",
                "name": "ssh",
                "synopsis": "ssh [-p port] [user@]hostname [command]",
                "short_desc": "OpenSSH remote login client.",
                "detailed_desc": "Secure encrypted terminal connection to remote servers.",
                "category": "Remote Access",
                "common_flags": [
                    {"flag": "-i <key>", "desc": "Select private key identity file."},
                    {"flag": "-p <port>", "desc": "Port to connect to on the remote host (default 22)."}
                ],
                "sample_output": "[student@rhel9-node1 ~]$ ",
                "rhcsa_tips": ["Exam servers are headless: everything is managed via SSH connections."],
                "default_run_cmd": "ssh -V"
            },
            {
                "id": "ch5_scp",
                "name": "scp",
                "synopsis": "scp [options] [[user@]host1:]file1 [[user@]host2:]file2",
                "short_desc": "Secure copy files between hosts over SSH.",
                "detailed_desc": "Transfers files over an encrypted SSH transport.",
                "category": "File Transfer",
                "common_flags": [{"flag": "-r", "desc": "Recursively copy entire directories."}],
                "sample_output": "config.tar.gz          100%   24MB  48.2MB/s   00:00",
                "rhcsa_tips": ["Use 'scp -p' to retain original file timestamps."],
                "default_run_cmd": "scp --help | head -n 10"
            },
            {
                "id": "ch5_sftp",
                "name": "sftp",
                "synopsis": "sftp [options] [user@]host",
                "short_desc": "Interactive secure file transfer program.",
                "detailed_desc": "Interactive FTP-like subsystem running over SSH.",
                "category": "File Transfer",
                "common_flags": [{"flag": "-P <port>", "desc": "Connect to specific port."}],
                "sample_output": "Connected to rhel9-node2.example.com.",
                "rhcsa_tips": ["Used when shell login is restricted but file drop is permitted."],
                "default_run_cmd": "sftp -h"
            },
            {
                "id": "ch5_ssh_keygen",
                "name": "ssh-keygen",
                "synopsis": "ssh-keygen [-t dsa | ecdsa | ed25519 | rsa] [-b bits]",
                "short_desc": "Generate, manage and convert authentication keys for SSH.",
                "detailed_desc": "Generates private/public key pairs for passwordless authentication.",
                "category": "SSH Security",
                "common_flags": [
                    {"flag": "-t <type>", "desc": "Specifies type of key to create (rsa, ed25519)."},
                    {"flag": "-N ''", "desc": "Provide empty passphrase for non-interactive key generation."}
                ],
                "sample_output": "Your identification has been saved in /root/.ssh/id_rsa\nYour public key has been saved in /root/.ssh/id_rsa.pub",
                "rhcsa_tips": ["Configure key-based auth: 'ssh-keygen -t rsa -N \"\" -f ~/.ssh/id_rsa'."],
                "default_run_cmd": "ssh-keygen -l -f /etc/ssh/ssh_host_rsa_key.pub"
            },
            {
                "id": "ch5_ssh_copy_id",
                "name": "ssh-copy-id",
                "synopsis": "ssh-copy-id [-i [identity_file]] [user@]machine",
                "short_desc": "Install your public key in a remote machine's authorized_keys.",
                "detailed_desc": "Copies local public keys to remote ~/.ssh/authorized_keys file and ensures correct permissions (700 for ~/.ssh, 600 for authorized_keys).",
                "category": "SSH Setup",
                "common_flags": [{"flag": "-i <key>", "desc": "Specify public key file to append."}],
                "sample_output": "/usr/bin/ssh-copy-id: INFO: 1 key(s) added.",
                "rhcsa_tips": ["Always use ssh-copy-id instead of manually copy-pasting to avoid permission mistakes."],
                "default_run_cmd": "ssh-copy-id -h"
            },
            {
                "id": "ch5_w",
                "name": "w",
                "synopsis": "w [options] [user]",
                "short_desc": "Show who is logged on and what they are doing.",
                "detailed_desc": "Displays information about users currently on the machine and active processes, plus load averages.",
                "category": "User Tracking",
                "common_flags": [{"flag": "-s", "desc": "Use short format."}],
                "sample_output": " 17:45:00 up 4 days,  2 users,  load average: 0.08, 0.12, 0.09\nUSER     TTY      FROM             LOGIN@   IDLE   WHAT\nroot     pts/0    192.168.1.100    14:02    1.00s  w",
                "rhcsa_tips": ["Quick way to see active terminal sessions and system load."],
                "default_run_cmd": "w"
            },
            {
                "id": "ch5_who",
                "name": "who",
                "synopsis": "who [OPTION]... [ FILE | ARG1 ARG2 ]",
                "short_desc": "Show who is logged on.",
                "detailed_desc": "Reads /var/run/utmp to list all currently logged-in users.",
                "category": "User Tracking",
                "common_flags": [{"flag": "-b, --boot", "desc": "Time of last system boot."}],
                "sample_output": "root     pts/0        2026-09-24 14:02 (192.168.1.100)",
                "rhcsa_tips": ["'who -b' gives the exact last boot timestamp."],
                "default_run_cmd": "who -b"
            },
            {
                "id": "ch5_last",
                "name": "last",
                "synopsis": "last [-n num] [username...] [tty...]",
                "short_desc": "Show a listing of last logged in users.",
                "detailed_desc": "Searches /var/log/wtmp to present historical user login and reboot logs.",
                "category": "Security Auditing",
                "common_flags": [{"flag": "-n <N>", "desc": "Limit output to N entries."}],
                "sample_output": "student  pts/0        192.168.1.100    Wed Sep 24 14:02   still logged in\nreboot   system boot  5.14.0-284.el9   Sat Sep 20 14:33   still running",
                "rhcsa_tips": ["Check 'last reboot' to verify if a server rebooted recently."],
                "default_run_cmd": "last -n 5"
            },
            {
                "id": "ch5_tmux",
                "name": "tmux",
                "synopsis": "tmux [command]",
                "short_desc": "Terminal multiplexer for persistent remote sessions.",
                "detailed_desc": "Lets a single terminal window host multiple panes and detach sessions that continue running if network disconnects.",
                "category": "Session Multiplexing",
                "common_flags": [
                    {"flag": "new -s <name>", "desc": "Create a named tmux session."},
                    {"flag": "attach -t <name>", "desc": "Reattach to an active running session."}
                ],
                "sample_output": "rhcsa-lab: 2 windows (created Wed Sep 24 11:20:10 2026)",
                "rhcsa_tips": ["Running long commands in tmux prevents broken jobs if SSH connection drops."],
                "default_run_cmd": "tmux -V"
            },
            {
                "id": "ch5_screen",
                "name": "screen",
                "synopsis": "screen [-options] [cmd [args]]",
                "short_desc": "Screen manager with VT100/ANSI terminal emulation.",
                "detailed_desc": "Traditional terminal multiplexer allowing users to disconnect and reconnect to shell sessions.",
                "category": "Session Multiplexing",
                "common_flags": [{"flag": "-r", "desc": "Resume detached screen session."}],
                "sample_output": "There is a screen on: 14202.pts-0.rhel9 (Detached)",
                "rhcsa_tips": ["Useful alternative to tmux on legacy systems."],
                "default_run_cmd": "screen -v"
            }
        ]
    },

    # CHAPTER 6: User and Group Management
    {
        "chapter_id": 6,
        "part_id": 1,
        "part_title": "Part I: Performing Basic System Management Tasks",
        "chapter_title": "User and Group Management",
        "description": "Managing accounts, group memberships, password aging, sudo privileges, and security IDs.",
        "commands": [
            {
                "id": "ch6_useradd",
                "name": "useradd",
                "synopsis": "useradd [options] LOGIN",
                "short_desc": "Create a new user account.",
                "detailed_desc": "Creates system and regular user accounts, establishes UID, home directory, default shell, and initial group.",
                "category": "Account Management",
                "common_flags": [
                    {"flag": "-u <UID>", "desc": "Specify non-standard UID."},
                    {"flag": "-G <GROUPS>", "desc": "List of supplementary secondary groups."},
                    {"flag": "-s <SHELL>", "desc": "Login shell (e.g. /sbin/nologin or /bin/bash)."}
                ],
                "sample_output": "User 'natasha' successfully created with UID 2005.",
                "rhcsa_tips": ["Create user with secondary group: 'useradd -G sysadmin -s /sbin/nologin natasha'."],
                "default_run_cmd": "useradd -D"
            },
            {
                "id": "ch6_usermod",
                "name": "usermod",
                "synopsis": "usermod [options] LOGIN",
                "short_desc": "Modify a user account.",
                "detailed_desc": "Modifies user properties such as supplementary groups, shell, and home directory.",
                "category": "Account Management",
                "common_flags": [
                    {"flag": "-aG <GROUPS>", "desc": "CRITICAL: APPEND user to supplemental groups (without -a, replaces groups!)."},
                    {"flag": "-s <SHELL>", "desc": "Update user's default login shell."}
                ],
                "sample_output": "User 'sarah' modified: added to group 'wheel'.",
                "rhcsa_tips": ["NEVER forget the '-a' flag when using '-G' (always use 'usermod -aG group user')!"],
                "default_run_cmd": "usermod --help | head -n 12"
            },
            {
                "id": "ch6_userdel",
                "name": "userdel",
                "synopsis": "userdel [options] LOGIN",
                "short_desc": "Delete a user account and related files.",
                "detailed_desc": "Removes account from /etc/passwd, /etc/shadow, and /etc/group.",
                "category": "Account Management",
                "common_flags": [{"flag": "-r, --remove", "desc": "Remove home directory and mail spool."}],
                "sample_output": "userdel: user 'tempuser' removed along with '/home/tempuser'",
                "rhcsa_tips": ["Always use 'userdel -r' when the exam asks to completely purge an account."],
                "default_run_cmd": "userdel --help"
            },
            {
                "id": "ch6_groupadd",
                "name": "groupadd",
                "synopsis": "groupadd [options] GROUP",
                "short_desc": "Create a new group.",
                "detailed_desc": "Creates a new security group entry in /etc/group with specified or auto-allocated GID.",
                "category": "Group Management",
                "common_flags": [{"flag": "-g <GID>", "desc": "Assign specific numerical group ID."}],
                "sample_output": "Group 'devops' created with GID 3000.",
                "rhcsa_tips": ["Use 'groupadd -g 3000 sysadmin' when an exact GID is mandated."],
                "default_run_cmd": "groupadd --help"
            },
            {
                "id": "ch6_groupmod",
                "name": "groupmod",
                "synopsis": "groupmod [options] GROUP",
                "short_desc": "Modify a group definition on the system.",
                "detailed_desc": "Updates group name or numerical group ID.",
                "category": "Group Management",
                "common_flags": [{"flag": "-n <NEW_NAME>", "desc": "Rename group to NEW_NAME."}],
                "sample_output": "Group 'devops' renamed to 'cloud-eng'.",
                "rhcsa_tips": ["Verify changes in /etc/group."],
                "default_run_cmd": "groupmod --help"
            },
            {
                "id": "ch6_groupdel",
                "name": "groupdel",
                "synopsis": "groupdel [options] GROUP",
                "short_desc": "Delete a group from the system.",
                "detailed_desc": "Removes entry from /etc/group. Fails if group is primary group of any user.",
                "category": "Group Management",
                "common_flags": [],
                "sample_output": "groupdel: group 'cloud-eng' removed",
                "rhcsa_tips": ["Cannot delete a group that is currently any user's primary group."],
                "default_run_cmd": "groupdel --help"
            },
            {
                "id": "ch6_passwd",
                "name": "passwd",
                "synopsis": "passwd [options] [LOGIN]",
                "short_desc": "Change user password and expiry settings.",
                "detailed_desc": "Updates user authorization token in /etc/shadow.",
                "category": "Account Security",
                "common_flags": [{"flag": "--stdin", "desc": "Read password from standard input."}],
                "sample_output": "passwd: all authentication tokens updated successfully.",
                "rhcsa_tips": ["Scripting password assignment: 'echo \"redhat\" | passwd --stdin student'."],
                "default_run_cmd": "passwd --status root"
            },
            {
                "id": "ch6_id",
                "name": "id",
                "synopsis": "id [OPTION]... [USER]",
                "short_desc": "Print real and effective user and group IDs.",
                "detailed_desc": "Outputs UID, GID, and list of all supplementary groups with names and IDs.",
                "category": "Account Inspection",
                "common_flags": [
                    {"flag": "-u", "desc": "Print user ID."},
                    {"flag": "-g", "desc": "Print group ID."},
                    {"flag": "-G", "desc": "Print all group IDs."}
                ],
                "sample_output": "uid=1000(student) gid=1000(student) groups=1000(student),10(wheel),3000(sysadmin)",
                "rhcsa_tips": ["Always run 'id <user>' after useradd/usermod to verify group membership!"],
                "default_run_cmd": "id"
            },
            {
                "id": "ch6_chage",
                "name": "chage",
                "synopsis": "chage [options] LOGIN",
                "short_desc": "Change user password expiry and aging policy.",
                "detailed_desc": "Modifies password aging fields in /etc/shadow.",
                "category": "Account Policy",
                "common_flags": [
                    {"flag": "-l", "desc": "List current password aging policy for user."},
                    {"flag": "-M <DAYS>", "desc": "Set maximum number of days password is valid (e.g., 90)."}
                ],
                "sample_output": "Maximum number of days between password change: 90",
                "rhcsa_tips": ["Configure user password expiration: 'chage -M 90 natasha'."],
                "default_run_cmd": "chage -l root"
            },
            {
                "id": "ch6_sudo",
                "name": "sudo",
                "synopsis": "sudo [-u user] command",
                "short_desc": "Execute a command as another user or superuser (root).",
                "detailed_desc": "Grants delegated administrative privileges based on rules configured in /etc/sudoers.",
                "category": "Privilege Escalation",
                "common_flags": [
                    {"flag": "-i", "desc": "Simulate initial login (spawns root login shell)."},
                    {"flag": "-l", "desc": "List allowed and forbidden commands for current user."}
                ],
                "sample_output": "User student may run the following commands on rhel9-node1: (ALL) ALL",
                "rhcsa_tips": ["On RHEL 9, adding a user to group 'wheel' automatically confers full sudo rights."],
                "default_run_cmd": "sudo -l"
            }
        ]
    },

    # CHAPTER 7: Permissions Management
    {
        "chapter_id": 7,
        "part_id": 1,
        "part_title": "Part I: Performing Basic System Management Tasks",
        "chapter_title": "Permissions Management",
        "description": "Standard permissions (rwx), special permissions (SUID, SGID, Sticky bit), POSIX Access Control Lists (ACLs), and default umask.",
        "commands": [
            {
                "id": "ch7_chmod",
                "name": "chmod",
                "synopsis": "chmod [OPTION]... MODE[,MODE]... FILE...",
                "short_desc": "Change file access permissions (modes).",
                "detailed_desc": "Changes permission bits (read, write, execute) for user, group, and others in octal (e.g. 755, 2770) or symbolic format (u+rwx, g+s).",
                "category": "Permissions",
                "common_flags": [
                    {"flag": "-R, --recursive", "desc": "Change files and directories recursively."},
                    {"flag": "2770", "desc": "Set SGID on directory (new files inherit group ownership)."},
                    {"flag": "1777", "desc": "Set Sticky bit on shared directory (only file owners can delete)."}
                ],
                "sample_output": "mode of '/shared/projects' changed from 0755 to 2770 (rwxrws---)",
                "rhcsa_tips": [
                    "RHCSA CLASSIC QUESTION: 'Configure directory /shared/sales so members of group sales can collaborate, new files inherit group ownership, and non-members have no access': chmod 2770 /shared/sales."
                ],
                "default_run_cmd": "chmod 755 /tmp/rhcsa_test_file.txt && ls -l /tmp/rhcsa_test_file.txt"
            },
            {
                "id": "ch7_chown",
                "name": "chown",
                "synopsis": "chown [OPTION]... [OWNER][:[GROUP]] FILE...",
                "short_desc": "Change file owner and group ownership.",
                "detailed_desc": "Assigns user and group ownership for files and directories.",
                "category": "Ownership",
                "common_flags": [
                    {"flag": "-R, --recursive", "desc": "Operate on files and directories recursively."},
                    {"flag": "user:group", "desc": "Change both owner and group simultaneously."}
                ],
                "sample_output": "changed ownership of '/var/www/html' from root:root to apache:apache",
                "rhcsa_tips": ["Use 'chown -R student:sysadmin /opt/app' to set both user and group in a single command."],
                "default_run_cmd": "chown root:root /tmp/rhcsa_test_file.txt && ls -l /tmp/rhcsa_test_file.txt"
            },
            {
                "id": "ch7_chgrp",
                "name": "chgrp",
                "synopsis": "chgrp [OPTION]... GROUP FILE...",
                "short_desc": "Change group ownership of files.",
                "detailed_desc": "Modifies the owning group of each given file.",
                "category": "Ownership",
                "common_flags": [{"flag": "-R", "desc": "Recursively change group ownership."}],
                "sample_output": "group of '/opt/data' changed to 'sysadmin'",
                "rhcsa_tips": ["Handy when you only want to reassign the group without touching the owner."],
                "default_run_cmd": "chgrp root /tmp/rhcsa_test_file.txt"
            },
            {
                "id": "ch7_umask",
                "name": "umask",
                "synopsis": "umask [-p] [-S] [mode]",
                "short_desc": "Get or set the file mode creation mask.",
                "detailed_desc": "Determines the default permissions stripped from newly created files (base 666) and directories (base 777).",
                "category": "Permissions",
                "common_flags": [
                    {"flag": "-S", "desc": "Display mask symbolically (e.g. u=rwx,g=rx,o=rx)."},
                    {"flag": "0022", "desc": "Set standard umask (files 644, dirs 755)."},
                    {"flag": "0002", "desc": "Set collaborative umask (files 664, dirs 775)."}
                ],
                "sample_output": "0022\nu=rwx,g=rx,o=rx",
                "rhcsa_tips": ["To make umask changes persistent for all users, update '/etc/profile' or '/etc/bashrc'."],
                "default_run_cmd": "umask -S"
            },
            {
                "id": "ch7_getfacl",
                "name": "getfacl",
                "synopsis": "getfacl [-aceEsRLPtpndvh] file ...",
                "short_desc": "Get file access control lists (ACLs).",
                "detailed_desc": "Displays fine-grained POSIX access control lists for users and groups beyond traditional ugo permissions.",
                "category": "Access Control Lists",
                "common_flags": [
                    {"flag": "-R", "desc": "Recurse into subdirectories."},
                    {"flag": "-d", "desc": "Display default ACL of a directory."}
                ],
                "sample_output": """# file: shared/data.csv
# owner: root
# group: root
user::rw-
user:sarah:rwx
group::r--
mask::rwx
other::---""",
                "rhcsa_tips": ["A plus sign (+) at the end of 'ls -l' permissions (e.g., -rw-r-----+ 1) indicates an active ACL!"],
                "default_run_cmd": "getfacl /etc/hosts"
            },
            {
                "id": "ch7_setfacl",
                "name": "setfacl",
                "synopsis": "setfacl [-bkndRLPvh] [{-m|-x} acl_spec] [{-M|-X} acl_file] file ...",
                "short_desc": "Set file access control lists (ACLs).",
                "detailed_desc": "Applies specific user (u:name:perms) or group (g:name:perms) permissions, or configures inheritance default ACLs (d:u:name:perms).",
                "category": "Access Control Lists",
                "common_flags": [
                    {"flag": "-m u:<USER>:<PERMS>", "desc": "Modify ACL for specific user (e.g. setfacl -m u:natasha:rwx file)."},
                    {"flag": "-m g:<GROUP>:<PERMS>", "desc": "Modify ACL for specific group."},
                    {"flag": "-m d:u:<USER>:<PERMS>", "desc": "Set DEFAULT ACL on directory (inherited by new files!)."},
                    {"flag": "-x u:<USER>", "desc": "Remove ACL entry for user."},
                    {"flag": "-b", "desc": "Remove all extended ACL entries."}
                ],
                "sample_output": "ACL applied to '/var/log/audit/audit.log' for user 'auditor': read-only (r--)",
                "rhcsa_tips": [
                    "RHCSA FREQUENT EXAM TASK: 'Ensure user natasha has read/write permissions on /shared/file and user harry has no access': setfacl -m u:natasha:rw,u:harry:--- /shared/file.",
                    "For inherited directory permissions, set both standard AND default: 'setfacl -m u:natasha:rwx,d:u:natasha:rwx /shared/dir'."
                ],
                "default_run_cmd": "setfacl --help | head -n 15"
            },
            {
                "id": "ch7_stat",
                "name": "stat",
                "synopsis": "stat [OPTION]... FILE...",
                "short_desc": "Display detailed file or filesystem status.",
                "detailed_desc": "Shows exact inode number, octal permissions, links, and accurate access, modify, and change timestamps.",
                "category": "File Inspection",
                "common_flags": [
                    {"flag": "-c %a", "desc": "Print only the octal permission bits (e.g. 755)."}
                ],
                "sample_output": """  File: /etc/passwd
  Size: 2480       Blocks: 8          IO Block: 4096   regular file
Device: fd00h/64768d  Inode: 16781290    Links: 1
Access: (0644/-rw-r--r--)  Uid: (    0/    root)   Gid: (    0/    root)
Context: system_u:object_r:passwd_file_t:s0
Access: 2026-09-24 17:00:02.124567890 -0400
Modify: 2026-09-24 14:15:30.987654321 -0400
Change: 2026-09-24 14:15:30.987654321 -0400
 Birth: 2026-09-20 10:00:00.000000000 -0400""",
                "rhcsa_tips": ["Best tool to distinguish between 'Modify' (content changed) and 'Change' (metadata/permissions changed) timestamps."],
                "default_run_cmd": "stat /etc/passwd"
            },
            {
                "id": "ch7_chattr",
                "name": "chattr",
                "synopsis": "chattr [-RVf] [+-=attributes] [files...]",
                "short_desc": "Change file attributes on a Linux file system.",
                "detailed_desc": "Applies special ext4/xfs filesystem attributes such as immutable (+i, prevents any modification/deletion even by root) or append-only (+a).",
                "category": "Attributes",
                "common_flags": [
                    {"flag": "+i", "desc": "Make file immutable (cannot be written, renamed, or deleted by anyone)."},
                    {"flag": "-i", "desc": "Remove immutable attribute."},
                    {"flag": "+a", "desc": "Allow only appending to file (great for logs)."}
                ],
                "sample_output": "Attribute +i set on '/etc/resolv.conf'",
                "rhcsa_tips": ["If root gets 'Operation not permitted' when trying to delete or edit a file, check for +i with lsattr!"],
                "default_run_cmd": "chattr --help"
            },
            {
                "id": "ch7_lsattr",
                "name": "lsattr",
                "synopsis": "lsattr [-RVadlv] [files...]",
                "short_desc": "List file attributes on a Linux second extended file system.",
                "detailed_desc": "Displays immutable, append, and other filesystem flags on files.",
                "category": "Attributes",
                "common_flags": [{"flag": "-d", "desc": "List directories like other files, rather than listing their contents."}],
                "sample_output": "----i---------e----- /etc/resolv.conf\n--------------e----- /etc/hosts",
                "rhcsa_tips": ["Look for the 'i' flag when troubleshooting un-deletable files."],
                "default_run_cmd": "lsattr -d /etc"
            },
            {
                "id": "ch7_find_perm",
                "name": "find -perm",
                "synopsis": "find [path] -perm [mode]",
                "short_desc": "Locate files matching specific permission bits (SUID, SGID).",
                "detailed_desc": "Audits filesystem for security risks or files with SUID/SGID/sticky bits set.",
                "category": "Security Auditing",
                "common_flags": [
                    {"flag": "-perm -4000", "desc": "Find files with SUID bit set."},
                    {"flag": "-perm -2000", "desc": "Find files with SGID bit set."},
                    {"flag": "-perm -0002", "desc": "Find world-writable files."}
                ],
                "sample_output": """/usr/bin/passwd
/usr/bin/sudo
/usr/bin/chage
/usr/bin/gpasswd""",
                "rhcsa_tips": ["'find / -perm -4000 -type f 2>/dev/null' is the standard RHCSA command to audit all SUID executables."],
                "default_run_cmd": "find /usr/bin -perm -4000 -type f 2>/dev/null | head -n 5"
            }
        ]
    },

    # CHAPTER 8: Configuring Networking
    {
        "chapter_id": 8,
        "part_id": 1,
        "part_title": "Part I: Performing Basic System Management Tasks",
        "chapter_title": "Configuring Networking",
        "description": "NetworkManager configuration, nmcli, nmtui, IP addressing, routing tables, and socket inspection.",
        "commands": [
            {
                "id": "ch8_nmcli_con",
                "name": "nmcli connection",
                "synopsis": "nmcli connection {show | up | down | add | modify | delete} ...",
                "short_desc": "NetworkManager CLI for connection profile management.",
                "detailed_desc": "Configures persistent IP addresses, netmasks, gateways, and DNS servers in NetworkManager keyfiles (/etc/NetworkManager/system-connections/).",
                "category": "Network Configuration",
                "common_flags": [
                    {"flag": "show", "desc": "List all configured connection profiles."},
                    {"flag": "modify <CON> ipv4.addresses <IP/NETMASK>", "desc": "Set static IP address."},
                    {"flag": "modify <CON> ipv4.gateway <GW>", "desc": "Set default gateway."},
                    {"flag": "modify <CON> ipv4.dns <DNS>", "desc": "Set DNS nameserver."},
                    {"flag": "modify <CON> ipv4.method manual", "desc": "Switch IP configuration method to static."},
                    {"flag": "up <CON>", "desc": "Reactivate and apply connection configuration immediately."}
                ],
                "sample_output": """NAME    UUID                                  TYPE      DEVICE 
enp1s0  c9a1b8e4-1b3d-4c3e-9f0a-123456789abc  ethernet  enp1s0 
lo      4a2d3c1e-9876-4321-abcd-ef0123456789  loopback  lo     """,
                "rhcsa_tips": [
                    "RHCSA MANDATORY REQUIREMENT: 'nmcli con mod \"enp1s0\" ipv4.addresses 192.168.1.50/24 ipv4.gateway 192.168.1.1 ipv4.dns 192.168.1.1 ipv4.method manual && nmcli con up \"enp1s0\"'. Always remember to run 'nmcli con up' to activate the change!"
                ],
                "default_run_cmd": "nmcli connection show"
            },
            {
                "id": "ch8_nmcli_dev",
                "name": "nmcli device",
                "synopsis": "nmcli device {status | show | connect | disconnect} [IFACE]",
                "short_desc": "NetworkManager CLI for hardware network interfaces.",
                "detailed_desc": "Inspects and controls physical and virtual network hardware devices.",
                "category": "Network Hardware",
                "common_flags": [
                    {"flag": "status", "desc": "Show high-level interface status and connection mapping."},
                    {"flag": "show <IFACE>", "desc": "Display all IP, MAC, and MTU details for interface."}
                ],
                "sample_output": """DEVICE  TYPE      STATE      CONNECTION 
enp1s0  ethernet  connected  enp1s0     
lo      loopback  unmanaged  --         """,
                "rhcsa_tips": ["Use 'nmcli dev status' to identify the exact device name (e.g., eth0 vs ens3 vs enp1s0) before configuring connections."],
                "default_run_cmd": "nmcli device status"
            },
            {
                "id": "ch8_nmtui",
                "name": "nmtui",
                "synopsis": "nmtui [edit | connect | hostname]",
                "short_desc": "Text User Interface for NetworkManager.",
                "detailed_desc": "Curses-based interactive terminal UI for configuring IP addresses, hostnames, and connections without remembering nmcli syntax.",
                "category": "Interactive Network",
                "common_flags": [
                    {"flag": "edit", "desc": "Directly launch into the connection profile editor."},
                    {"flag": "hostname", "desc": "Directly launch into the hostname editor."}
                ],
                "sample_output": "[Interactive nmtui curses screen launched in terminal]",
                "rhcsa_tips": ["If you get stuck on nmcli syntax during the RHCSA exam, 'nmtui' provides a foolproof graphical menu right in your terminal!"],
                "default_run_cmd": "nmtui --help"
            },
            {
                "id": "ch8_ip_addr",
                "name": "ip addr",
                "synopsis": "ip [OPTIONS] address {show | add | del} ...",
                "short_desc": "Display or manipulate network interface IP addresses.",
                "detailed_desc": "Modern Linux iproute2 utility to inspect IPv4 and IPv6 addresses on network interfaces.",
                "category": "IP Inspection",
                "common_flags": [
                    {"flag": "show", "desc": "Display IP address properties on all active interfaces."},
                    {"flag": "show dev <IFACE>", "desc": "Display addresses for a specific device only."}
                ],
                "sample_output": """2: enp1s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 52:54:00:12:34:56 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.50/24 brd 192.168.1.255 scope global noprefixroute enp1s0
       valid_lft forever preferred_lft forever
    inet6 fe80::5054:ff:fe12:3456/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever""",
                "rhcsa_tips": ["Use 'ip -br addr show' for a clean, concise single-line tabular view."],
                "default_run_cmd": "ip -br addr show"
            },
            {
                "id": "ch8_ip_route",
                "name": "ip route",
                "synopsis": "ip route {show | add | del} ...",
                "short_desc": "Display and manipulate the kernel routing table.",
                "detailed_desc": "Inspects active routing paths, gateway destinations, and metric priorities.",
                "category": "Routing",
                "common_flags": [
                    {"flag": "show", "desc": "List all active routing table entries."},
                    {"flag": "get <IP>", "desc": "Simulate and display the exact route kernel will take to reach an IP."}
                ],
                "sample_output": """default via 192.168.1.1 dev enp1s0 proto static metric 100 
192.168.1.0/24 dev enp1s0 proto kernel scope link src 192.168.1.50 metric 100 """,
                "rhcsa_tips": ["'ip route get 8.8.8.8' immediately reveals which interface and gateway traffic will exit through."],
                "default_run_cmd": "ip route show"
            },
            {
                "id": "ch8_ping",
                "name": "ping",
                "synopsis": "ping [options] destination",
                "short_desc": "Send ICMP ECHO_REQUEST packets to network hosts.",
                "detailed_desc": "Verifies network reachability, latency, and packet loss to a remote host.",
                "category": "Diagnostics",
                "common_flags": [
                    {"flag": "-c <COUNT>", "desc": "Stop after sending COUNT packets (crucial in scripts!)."},
                    {"flag": "-W <TIMEOUT>", "desc": "Time to wait for a response in seconds."}
                ],
                "sample_output": """PING 192.168.1.1 (192.168.1.1) 56(84) bytes of data.
64 bytes from 192.168.1.1: icmp_seq=1 ttl=64 time=0.428 ms
64 bytes from 192.168.1.1: icmp_seq=2 ttl=64 time=0.381 ms

--- 192.168.1.1 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 0.381/0.404/0.428/0.023 ms""",
                "rhcsa_tips": ["Always use 'ping -c 2 <host>' so the command terminates on its own rather than running indefinitely."],
                "default_run_cmd": "ping -c 2 127.0.0.1"
            },
            {
                "id": "ch8_ss",
                "name": "ss",
                "synopsis": "ss [options] [FILTER]",
                "short_desc": "Another utility to investigate sockets (replaces netstat).",
                "detailed_desc": "Dumps socket statistics, open TCP/UDP listening ports, and active network connections.",
                "category": "Diagnostics",
                "common_flags": [
                    {"flag": "-t", "desc": "Display TCP sockets."},
                    {"flag": "-u", "desc": "Display UDP sockets."},
                    {"flag": "-l", "desc": "Display only listening sockets."},
                    {"flag": "-n", "desc": "Show numeric ports instead of service names (e.g. 22 instead of ssh)."},
                    {"flag": "-p", "desc": "Show process using the socket."}
                ],
                "sample_output": """Netid State  Recv-Q Send-Q Local Address:Port  Peer Address:PortProcess
tcp   LISTEN 0      128          0.0.0.0:22         0.0.0.0:*    users:(("sshd",pid=820,fd=3))
tcp   LISTEN 0      128          0.0.0.0:80         0.0.0.0:*    users:(("httpd",pid=1200,fd=4))
tcp   LISTEN 0      128             [::]:22            [::]:*    users:(("sshd",pid=820,fd=4))""",
                "rhcsa_tips": [
                    "RHCSA MEMORIZE: 'ss -tulpn' is the definitive command to verify if services like httpd (port 80) or sshd (port 22) are actively listening on their ports!"
                ],
                "default_run_cmd": "ss -tulpn"
            },
            {
                "id": "ch8_traceroute",
                "name": "traceroute",
                "synopsis": "traceroute [options] host [packetlen]",
                "short_desc": "Print the route packets trace to network host.",
                "detailed_desc": "Discovers every intermediate router hop between localhost and destination host.",
                "category": "Diagnostics",
                "common_flags": [
                    {"flag": "-n", "desc": "Do not resolve IP addresses to domain names (faster output)."},
                    {"flag": "-m <max_ttl>", "desc": "Set the max number of hops."}
                ],
                "sample_output": """traceroute to 192.168.1.1 (192.168.1.1), 30 hops max, 60 byte packets
 1  gateway (192.168.1.1)  0.512 ms  0.480 ms  0.420 ms""",
                "rhcsa_tips": ["Useful to diagnose where packets get dropped in multi-segment networks."],
                "default_run_cmd": "traceroute -n 127.0.0.1"
            },
            {
                "id": "ch8_dig",
                "name": "dig",
                "synopsis": "dig [@server] [-p port] [name] [type]",
                "short_desc": "DNS lookup utility.",
                "detailed_desc": "Queries Domain Name System (DNS) servers for records (A, CNAME, MX, PTR).",
                "category": "DNS Diagnostics",
                "common_flags": [
                    {"flag": "+short", "desc": "Provide terse, script-friendly output (only the resolved IP)."}
                ],
                "sample_output": """192.168.1.50""",
                "rhcsa_tips": ["'dig +short server1.example.com' quickly tests if DNS resolution in /etc/resolv.conf is functioning."],
                "default_run_cmd": "dig +short localhost"
            },
            {
                "id": "ch8_curl",
                "name": "curl",
                "synopsis": "curl [options...] <url>",
                "short_desc": "Transfer data from or to a server using supported protocols.",
                "detailed_desc": "Performs HTTP/HTTPS/FTP requests to test web services, API endpoints, and download files.",
                "category": "Web / Network Client",
                "common_flags": [
                    {"flag": "-I, --head", "desc": "Fetch only HTTP headers (checks HTTP 200 OK without downloading body)."},
                    {"flag": "-s, --silent", "desc": "Silent mode, hides progress meter."},
                    {"flag": "-o <file>", "desc": "Write output to file instead of stdout."}
                ],
                "sample_output": """HTTP/1.1 200 OK
Date: Wed, 24 Sep 2026 17:50:00 GMT
Server: Apache/2.4.57 (Red Hat Enterprise Linux)
Content-Type: text/html; charset=UTF-8""",
                "rhcsa_tips": ["Always verify Apache web server configuration on the exam using 'curl -I http://localhost'!"],
                "default_run_cmd": "curl -I https://www.redhat.com"
            }
        ]
    }
]
