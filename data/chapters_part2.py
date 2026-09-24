"""
Part II: Operating Running Systems (Chapters 9 - 15)
10 Essential Commands per Chapter (70 commands total)
"""

PART_2_CHAPTERS = [
    # CHAPTER 9: Managing Software
    {
        "chapter_id": 9,
        "part_id": 2,
        "part_title": "Part II: Operating Running Systems",
        "chapter_title": "Managing Software",
        "description": "Package management with DNF/YUM, software repositories, Application Streams (AppStream), and low-level RPM queries.",
        "commands": [
            {
                "id": "ch9_dnf_install",
                "name": "dnf install",
                "synopsis": "dnf [options] install <package-spec>...",
                "short_desc": "Install packages and all required dependencies.",
                "detailed_desc": "Resolves dependencies from enabled repositories and installs RPM packages onto the system.",
                "category": "Package Management",
                "common_flags": [
                    {"flag": "-y, --assumeyes", "desc": "Automatically answer yes to all prompts."},
                    {"flag": "--allowerasing", "desc": "Allow erasing of installed packages to resolve conflicts."}
                ],
                "sample_output": """Dependencies resolved.
================================================================================
 Package             Arch       Version             Repository             Size
================================================================================
Installing:
 httpd               x86_64     2.4.57-5.el9_2      rhel-9-appstream-rpms 1.4 M

Transaction Summary
================================================================================
Install  1 Package

Complete!""",
                "rhcsa_tips": ["Always append '-y' in automated installation scripts: 'dnf install -y httpd'."],
                "default_run_cmd": "dnf check-update"
            },
            {
                "id": "ch9_dnf_remove",
                "name": "dnf remove",
                "synopsis": "dnf [options] remove <package-spec>...",
                "short_desc": "Remove packages from the system along with unused dependencies.",
                "detailed_desc": "Uninstalls designated packages and cascades removal to packages that depended on them.",
                "category": "Package Management",
                "common_flags": [{"flag": "-y", "desc": "Do not prompt for confirmation."}],
                "sample_output": "Removed: httpd-2.4.57-5.el9_2.x86_64\nComplete!",
                "rhcsa_tips": ["Be mindful: removing a foundational library could prompt removing dependent system services."],
                "default_run_cmd": "dnf --help | head -n 12"
            },
            {
                "id": "ch9_dnf_search",
                "name": "dnf search",
                "synopsis": "dnf search [options] <keywords>...",
                "short_desc": "Search package names and summaries for matching strings.",
                "detailed_desc": "Scans repository metadata to help locate the exact package name.",
                "category": "Package Query",
                "common_flags": [{"flag": "--all", "desc": "Search descriptions as well as summaries and names."}],
                "sample_output": """====================== Name & Summary Matched: nginx ======================
nginx.x86_64 : A high performance web server and reverse proxy server
nginx-core.x86_64 : nginx core components""",
                "rhcsa_tips": ["Use dnf search when you know the software function but not the exact RPM package name."],
                "default_run_cmd": "dnf search nginx"
            },
            {
                "id": "ch9_dnf_repolist",
                "name": "dnf repolist",
                "synopsis": "dnf repolist [all | enabled | disabled]",
                "short_desc": "Display configured and enabled software repositories.",
                "detailed_desc": "Reads all .repo configuration files in /etc/yum.repos.d/ and outputs active repository IDs.",
                "category": "Repositories",
                "common_flags": [
                    {"flag": "-v, --verbose", "desc": "Show detailed repo URL and package count."}
                ],
                "sample_output": """repo id                      repo name
rhel-9-for-x86_64-appstream-rpms Red Hat Enterprise Linux 9 AppStream (RPMs)
rhel-9-for-x86_64-baseos-rpms    Red Hat Enterprise Linux 9 BaseOS (RPMs)""",
                "rhcsa_tips": ["RHCSA MANDATORY: Verify your custom repository is active with 'dnf repolist' after creating its .repo file!"],
                "default_run_cmd": "dnf repolist"
            },
            {
                "id": "ch9_dnf_module",
                "name": "dnf module",
                "synopsis": "dnf module {list | enable | disable | install | reset} <module-spec>",
                "short_desc": "Manage AppStream modules and modular streams.",
                "detailed_desc": "Enables choosing between multiple parallel versions of runtime software (e.g. nodejs 18 vs 20, python 3.9 vs 3.11).",
                "category": "AppStream Modules",
                "common_flags": [
                    {"flag": "list <name>", "desc": "List available streams and profiles for a module."},
                    {"flag": "enable <name>:<stream>", "desc": "Enable a specific software stream."},
                    {"flag": "install <name>:<stream>/<profile>", "desc": "Install a stream with a specific profile (e.g., nodejs:18/common)."}
                ],
                "sample_output": """Red Hat Enterprise Linux 9 for x86_64 - AppStream (RPMs)
Name        Stream     Profiles                                Summary
nodejs      18         common [d], development, minimal, s2i   Javascript runtime
nodejs      20         common [d], development, minimal, s2i   Javascript runtime

Hint: [d]efault, [e]nabled, [x]disabled, [i]nstalled""",
                "rhcsa_tips": [
                    "RHCSA EXAM OBJECTIVE: 'Install nodejs stream 18 using default profile': dnf module install -y nodejs:18."
                ],
                "default_run_cmd": "dnf module list nodejs"
            },
            {
                "id": "ch9_dnf_history",
                "name": "dnf history",
                "synopsis": "dnf history {list | info | undo | rollback} [ID]",
                "short_desc": "Inspect or roll back past package management transactions.",
                "detailed_desc": "Displays transaction logs, dates, and allows undoing mistakes by transaction ID.",
                "category": "Package History",
                "common_flags": [
                    {"flag": "undo <ID>", "desc": "Revert all package changes performed in transaction ID."},
                    {"flag": "info <ID>", "desc": "Show specific packages touched in transaction ID."}
                ],
                "sample_output": """ID     | Command line             | Date and time    | Action(s)      | Altered
-------------------------------------------------------------------------------
     3 | install -y httpd         | 2026-09-24 16:30 | Install        |    1   
     2 | update -y                | 2026-09-20 12:15 | Upgrade        |   14 EE
     1 |                          | 2026-09-15 08:00 | Install        |  485 EE""",
                "rhcsa_tips": ["'dnf history undo <id>' can save your exam if you accidentally installed the wrong package stack."],
                "default_run_cmd": "dnf history list"
            },
            {
                "id": "ch9_rpm_qa",
                "name": "rpm -qa",
                "synopsis": "rpm -qa [package_name]",
                "short_desc": "Query all installed RPM packages.",
                "detailed_desc": "Queries the local RPM database (/var/lib/rpm) and prints names and versions of installed software.",
                "category": "RPM Query",
                "common_flags": [
                    {"flag": "--last", "desc": "Sort packages by install time, most recent first."}
                ],
                "sample_output": """kernel-5.14.0-284.11.1.el9_2.x86_64
systemd-252-13.el9_2.x86_64
httpd-2.4.57-5.el9_2.x86_64
bash-5.1.8-6.el9.x86_64""",
                "rhcsa_tips": ["Combine with grep: 'rpm -qa | grep -i chrony' to verify if a daemon package is installed."],
                "default_run_cmd": "rpm -qa | head -n 10"
            },
            {
                "id": "ch9_rpm_ql",
                "name": "rpm -ql",
                "synopsis": "rpm -ql <package-name>",
                "short_desc": "List all files installed by a specific RPM package.",
                "detailed_desc": "Displays configuration files, executables, man pages, and documentation provided by an installed package.",
                "category": "RPM Query",
                "common_flags": [
                    {"flag": "-qc", "desc": "List ONLY configuration files installed by package."},
                    {"flag": "-qd", "desc": "List ONLY documentation files installed by package."}
                ],
                "sample_output": """/etc/httpd/conf/httpd.conf
/etc/httpd/conf.d/welcome.conf
/usr/sbin/httpd
/usr/share/man/man8/httpd.8.gz""",
                "rhcsa_tips": ["Use 'rpm -qc <pkg>' to discover where the configuration files are located when you don't know the exact file path!"],
                "default_run_cmd": "rpm -ql bash | head -n 12"
            },
            {
                "id": "ch9_rpm_qf",
                "name": "rpm -qf",
                "synopsis": "rpm -qf <file-path>",
                "short_desc": "Find which RPM package owns a specific file on the filesystem.",
                "detailed_desc": "Queries the RPM database to identify which installed package supplied the specified file path.",
                "category": "RPM Query",
                "common_flags": [],
                "sample_output": "httpd-2.4.57-5.el9_2.x86_64",
                "rhcsa_tips": ["EXAM FAVORITE: 'rpm -qf /etc/hosts' or 'dnf provides /path/to/binary' to identify software origins."],
                "default_run_cmd": "rpm -qf /etc/passwd"
            },
            {
                "id": "ch9_dnf_provides",
                "name": "dnf provides",
                "synopsis": "dnf provides <file-or-feature>",
                "short_desc": "Find which package provides a specific command or file (even uninstalled!).",
                "detailed_desc": "Searches uninstalled repository catalogs for packages delivering specific binaries or headers.",
                "category": "Package Discovery",
                "common_flags": [],
                "sample_output": """httpd-core-2.4.57-5.el9_2.x86_64 : httpd core components
Repo        : rhel-9-appstream-rpms
Matched from:
Filename    : /usr/sbin/semanage""",
                "rhcsa_tips": [
                    "RHCSA LIFE SAVER: If a command is missing (like semanage or semanage port), run 'dnf provides */semanage' to know what package to install (policycoreutils-python-utils)!"
                ],
                "default_run_cmd": "dnf provides */semanage"
            }
        ]
    },

    # CHAPTER 10: Managing Processes
    {
        "chapter_id": 10,
        "part_id": 2,
        "part_title": "Part II: Operating Running Systems",
        "chapter_title": "Managing Processes",
        "description": "Process monitoring, CPU and memory utilization, signals (SIGTERM, SIGKILL), priorities (nice/renice), and process trees.",
        "commands": [
            {
                "id": "ch10_ps_aux",
                "name": "ps aux",
                "synopsis": "ps [options]",
                "short_desc": "Report a snapshot of the current processes across the system.",
                "detailed_desc": "BSD-style syntax to report all running processes with user, PID, CPU%, MEM%, virtual memory, TTY, state, and command line.",
                "category": "Process Monitoring",
                "common_flags": [
                    {"flag": "-ef", "desc": "Standard UNIX syntax format (UID, PID, PPID, C, STIME, TTY, TIME, CMD)."},
                    {"flag": "--sort=-%mem", "desc": "Sort processes by memory consumption descending."},
                    {"flag": "--sort=-%cpu", "desc": "Sort processes by CPU consumption descending."}
                ],
                "sample_output": """USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.3 171804 13580 ?        Ss   Sep20   0:04 /usr/lib/systemd/systemd
root       820  0.0  0.1  16752  7340 ?        Ss   Sep20   0:00 /usr/sbin/sshd -D
apache    1240  0.0  0.4 228400 16200 ?        S    10:15   0:01 /usr/sbin/httpd -DFOREGROUND""",
                "rhcsa_tips": ["Use 'ps -ef | grep process_name' or 'pgrep' to find a target process PID."],
                "default_run_cmd": "ps aux | head -n 12"
            },
            {
                "id": "ch10_top",
                "name": "top",
                "synopsis": "top [options]",
                "short_desc": "Display dynamic real-time view of running processes and system resources.",
                "detailed_desc": "Interactive resource monitor showing uptime, load average, CPU states, memory, and top active tasks.",
                "category": "Process Monitoring",
                "common_flags": [
                    {"flag": "-b", "desc": "Batch mode (ideal for piping output to file or head)."},
                    {"flag": "-n <N>", "desc": "Number of iterations before exiting."}
                ],
                "sample_output": """top - 17:55:01 up 4 days,  2:30,  2 users,  load average: 0.15, 0.08, 0.05
Tasks: 182 total,   1 running, 181 sleeping,   0 stopped,   0 zombie
%Cpu(s):  1.2 us,  0.5 sy,  0.0 ni, 98.1 id,  0.1 wa,  0.0 hi,  0.1 si,  0.0 st
MiB Mem :   3820.5 total,   1410.2 free,    980.4 used,   1429.9 buff/cache
MiB Swap:   4096.0 total,   4096.0 free,      0.0 used.   2560.1 avail Mem""",
                "rhcsa_tips": ["Inside top: press 'M' to sort by Memory, 'P' to sort by CPU, and 'k' to kill a PID."],
                "default_run_cmd": "top -b -n 1 | head -n 15"
            },
            {
                "id": "ch10_kill",
                "name": "kill",
                "synopsis": "kill [-s signal | -p] [--] pid...",
                "short_desc": "Send a signal to specified process IDs.",
                "detailed_desc": "Terminates or signals processes. Key signals: SIGTERM (15, graceful), SIGKILL (9, immediate unblockable termination), SIGHUP (1, reload config).",
                "category": "Process Control",
                "common_flags": [
                    {"flag": "-9, -SIGKILL", "desc": "Force kill immediately (kernel drops process table entry)."},
                    {"flag": "-15, -SIGTERM", "desc": "Request graceful termination (default)."},
                    {"flag": "-l", "desc": "List all signal names and numeric codes."}
                ],
                "sample_output": "kill: (1240) - Process terminated",
                "rhcsa_tips": ["Always try SIGTERM (kill <PID>) first to let the process clean up locks before resorting to 'kill -9 <PID>'."],
                "default_run_cmd": "kill -l"
            },
            {
                "id": "ch10_killall",
                "name": "killall",
                "synopsis": "killall [options] [-s signal] name...",
                "short_desc": "Kill processes by name rather than PID.",
                "detailed_desc": "Sends a signal to all processes running any of the specified commands.",
                "category": "Process Control",
                "common_flags": [
                    {"flag": "-9", "desc": "Force kill all instances."},
                    {"flag": "-u <user>", "desc": "Kill only processes owned by specified user."}
                ],
                "sample_output": "Killed 4 httpd worker processes.",
                "rhcsa_tips": ["Use 'killall -u student' to terminate all rogue processes spawned by a user."],
                "default_run_cmd": "killall --help"
            },
            {
                "id": "ch10_pkill",
                "name": "pkill",
                "synopsis": "pkill [options] pattern",
                "short_desc": "Signal processes based on pattern match of name and other attributes.",
                "detailed_desc": "Finds processes matching regex patterns and delivers signals.",
                "category": "Process Control",
                "common_flags": [
                    {"flag": "-f", "desc": "Match against entire command line argument string, not just process name."},
                    {"flag": "-t <tty>", "desc": "Match processes attached to a specific terminal."}
                ],
                "sample_output": "pkill: matched 2 processes",
                "rhcsa_tips": ["'pkill -u student -9' kicks student off all sessions."],
                "default_run_cmd": "pkill --help"
            },
            {
                "id": "ch10_pgrep",
                "name": "pgrep",
                "synopsis": "pgrep [options] pattern",
                "short_desc": "Look up processes based on name and other attributes.",
                "detailed_desc": "Outputs process IDs matching the regex criteria.",
                "category": "Process Query",
                "common_flags": [
                    {"flag": "-l", "desc": "List the process name as well as the process ID."},
                    {"flag": "-a", "desc": "List the full command line."},
                    {"flag": "-u <user>", "desc": "Only match processes owned by user."}
                ],
                "sample_output": """820 sshd
1240 httpd
1241 httpd""",
                "rhcsa_tips": ["Use 'pgrep -l httpd' to quickly see PIDs without parsing messy grep pipelines."],
                "default_run_cmd": "pgrep -l systemd"
            },
            {
                "id": "ch10_nice",
                "name": "nice",
                "synopsis": "nice [OPTION] [COMMAND [ARG]...]",
                "short_desc": "Run a program with modified scheduling priority.",
                "detailed_desc": "Starts a process with custom niceness value (-20 highest priority to +19 lowest priority; default 0).",
                "category": "Scheduling Priority",
                "common_flags": [
                    {"flag": "-n <ADJUSTMENT>", "desc": "Specify nice value between -20 and 19 (e.g. nice -n 10 bash)."}
                ],
                "sample_output": "Started 'backup.sh' with nice level 15",
                "rhcsa_tips": ["Only root can start processes with negative nice values (higher CPU priority). Regular users can only be 'nicer' (0 to 19)."],
                "default_run_cmd": "nice -n 5 echo 'Running with nice 5'"
            },
            {
                "id": "ch10_renice",
                "name": "renice",
                "synopsis": "renice [-n] priority [[-p] pid...] [[-g] pgrp...] [[-u] user...]",
                "short_desc": "Alter priority of running processes.",
                "detailed_desc": "Adjusts the scheduling priority of already running tasks.",
                "category": "Scheduling Priority",
                "common_flags": [
                    {"flag": "-n <PRIORITY>", "desc": "Target priority value (-20 to 19)."},
                    {"flag": "-p <PID>", "desc": "Target process ID."}
                ],
                "sample_output": "1240 (process ID) old priority 0, new priority 10",
                "rhcsa_tips": ["RHCSA EXAM PROMPT: 'Change priority of running process 1240 to priority 10': renice -n 10 -p 1240."],
                "default_run_cmd": "renice --help"
            },
            {
                "id": "ch10_free",
                "name": "free",
                "synopsis": "free [options]",
                "short_desc": "Display amount of free and used memory in the system.",
                "detailed_desc": "Summarizes total, used, free, shared, cache/buffers, and available RAM and SWAP space.",
                "category": "Resource Monitoring",
                "common_flags": [
                    {"flag": "-h, --human", "desc": "Show human-readable units (GiB, MiB)."},
                    {"flag": "-m", "desc": "Display in megabytes."}
                ],
                "sample_output": """               total        used        free      shared  buff/cache   available
Mem:           3.7Gi       980Mi       1.4Gi        24Mi       1.4Gi       2.5Gi
Swap:          4.0Gi          0B       4.0Gi""",
                "rhcsa_tips": ["Always check the 'available' column rather than 'free', as buff/cache memory can be reclaimed on demand by the kernel."],
                "default_run_cmd": "free -h"
            },
            {
                "id": "ch10_uptime",
                "name": "uptime",
                "synopsis": "uptime [options]",
                "short_desc": "Tell how long the system has been running and load averages.",
                "detailed_desc": "Prints current time, system uptime, logged in user count, and 1-, 5-, and 15-minute CPU load averages.",
                "category": "Resource Monitoring",
                "common_flags": [
                    {"flag": "-p, --pretty", "desc": "Show uptime in human pretty format."},
                    {"flag": "-s, --since", "desc": "Show date/time of system boot."}
                ],
                "sample_output": " 17:58:12 up 4 days,  2:33,  2 users,  load average: 0.12, 0.07, 0.02\nup 4 days, 2 hours, 33 minutes",
                "rhcsa_tips": ["A load average higher than your CPU core count (checked via lscpu) indicates CPU saturation."],
                "default_run_cmd": "uptime -p"
            }
        ]
    },

    # CHAPTER 11: Working with Systemd
    {
        "chapter_id": 11,
        "part_id": 2,
        "part_title": "Part II: Operating Running Systems",
        "chapter_title": "Working with Systemd",
        "description": "Managing units, starting/stopping services, boot targets, masking services, and systemd performance profiling.",
        "commands": [
            {
                "id": "ch11_systemctl_start",
                "name": "systemctl start",
                "synopsis": "systemctl start UNIT...",
                "short_desc": "Start (activate) one or more units immediately.",
                "detailed_desc": "Instructs systemd manager to activate the service or target right away.",
                "category": "Service Management",
                "common_flags": [],
                "sample_output": "Started httpd.service - The Apache HTTP Server.",
                "rhcsa_tips": ["Remember: 'systemctl start' activates the service now, but DOES NOT survive a reboot unless you also 'enable' it!"],
                "default_run_cmd": "systemctl status sshd --no-pager"
            },
            {
                "id": "ch11_systemctl_enable",
                "name": "systemctl enable",
                "synopsis": "systemctl enable [--now] UNIT...",
                "short_desc": "Enable one or more units to start automatically at boot.",
                "detailed_desc": "Creates symlinks in /etc/systemd/system/*.wants/ to ensure activation on future system boots.",
                "category": "Service Management",
                "common_flags": [
                    {"flag": "--now", "desc": "SUPER TIP: Enable for boot AND start the service immediately in one command!"}
                ],
                "sample_output": "Created symlink /etc/systemd/system/multi-user.target.wants/httpd.service → /usr/lib/systemd/system/httpd.service.",
                "rhcsa_tips": [
                    "RHCSA GOLDEN RULE: 'systemctl enable --now httpd' satisfies both requirements (start now AND ensure active on reboot) in a single command!"
                ],
                "default_run_cmd": "systemctl is-enabled sshd"
            },
            {
                "id": "ch11_systemctl_status",
                "name": "systemctl status",
                "synopsis": "systemctl status [UNIT...]",
                "short_desc": "Show runtime status information about units.",
                "detailed_desc": "Displays active/inactive state, PID, memory, execution tree, and recent journal log entries for the unit.",
                "category": "Service Diagnostics",
                "common_flags": [
                    {"flag": "-l, --full", "desc": "Don't truncate log lines."},
                    {"flag": "--no-pager", "desc": "Do not pipe output into a pager."}
                ],
                "sample_output": """● httpd.service - The Apache HTTP Server
     Loaded: loaded (/usr/lib/systemd/system/httpd.service; enabled; preset: disabled)
     Active: active (running) since Wed 2026-09-24 16:30:10 EDT; 1h 30min ago
       Docs: man:httpd.service(8)
   Main PID: 1240 (httpd)
     Status: "Total requests: 120; Idle/Busy workers 100/0;Requests/sec: 0.02"
      Tasks: 213 (limit: 23120)
     Memory: 28.5M
        CPU: 1.450s
     CGroup: /system.slice/httpd.service
             ├─1240 /usr/sbin/httpd -DFOREGROUND
             └─1241 /usr/sbin/httpd -DFOREGROUND""",
                "rhcsa_tips": ["Always check 'Loaded' (enabled/disabled) and 'Active' (active/running) lines."],
                "default_run_cmd": "systemctl status sshd --no-pager"
            },
            {
                "id": "ch11_systemctl_stop",
                "name": "systemctl stop",
                "synopsis": "systemctl stop UNIT...",
                "short_desc": "Stop (deactivate) one or more units.",
                "detailed_desc": "Stops running processes associated with the service unit.",
                "category": "Service Management",
                "common_flags": [],
                "sample_output": "Stopped httpd.service - The Apache HTTP Server.",
                "rhcsa_tips": ["Stopping a service does not disable it from starting at next boot."],
                "default_run_cmd": "systemctl is-active sshd"
            },
            {
                "id": "ch11_systemctl_mask",
                "name": "systemctl mask",
                "synopsis": "systemctl mask UNIT...",
                "short_desc": "Mask a unit to link it to /dev/null, preventing it from starting.",
                "detailed_desc": "Stronger than disable: points unit to /dev/null so neither users nor other services can start it.",
                "category": "Service Security",
                "common_flags": [],
                "sample_output": "Created symlink /etc/systemd/system/firewalld.service → /dev/null.",
                "rhcsa_tips": ["If you get 'Failed to start ... Unit is masked', unmask it with 'systemctl unmask <unit>'."],
                "default_run_cmd": "systemctl is-enabled firewalld"
            },
            {
                "id": "ch11_systemctl_isolate",
                "name": "systemctl isolate",
                "synopsis": "systemctl isolate UNIT",
                "short_desc": "Start a unit and dependencies and stop all other unneeded units (switch target).",
                "detailed_desc": "Switches the running system between runlevels/targets (e.g. multi-user.target vs graphical.target).",
                "category": "Target Management",
                "common_flags": [],
                "sample_output": "Switched to multi-user.target.",
                "rhcsa_tips": [
                    "RHCSA OBJECTIVE: 'Switch system to graphical mode without reboot': systemctl isolate graphical.target."
                ],
                "default_run_cmd": "systemctl get-default"
            },
            {
                "id": "ch11_default_target",
                "name": "systemctl set-default",
                "synopsis": "systemctl set-default TARGET.target",
                "short_desc": "Set the default target to boot into permanently.",
                "detailed_desc": "Updates the default.target symlink in /etc/systemd/system/ (e.g., multi-user.target or graphical.target).",
                "category": "Target Management",
                "common_flags": [],
                "sample_output": "Removed /etc/systemd/system/default.target.\nCreated symlink /etc/systemd/system/default.target → /usr/lib/systemd/system/multi-user.target.",
                "rhcsa_tips": [
                    "RHCSA REQUIREMENT: 'Ensure node boots into multi-user target by default': systemctl set-default multi-user.target."
                ],
                "default_run_cmd": "systemctl get-default"
            },
            {
                "id": "ch11_daemon_reload",
                "name": "systemctl daemon-reload",
                "synopsis": "systemctl daemon-reload",
                "short_desc": "Reload systemd manager configuration after editing unit files.",
                "detailed_desc": "Rereads all generator and unit files in /etc/systemd/system and /usr/lib/systemd/system.",
                "category": "Service Administration",
                "common_flags": [],
                "sample_output": "[Systemd daemon configuration reloaded]",
                "rhcsa_tips": [
                    "ALWAYS run 'systemctl daemon-reload' immediately after creating or editing any custom .service file before attempting to start it!"
                ],
                "default_run_cmd": "systemctl daemon-reload"
            },
            {
                "id": "ch11_list_units",
                "name": "systemctl list-units",
                "synopsis": "systemctl list-units [PATTERN...]",
                "short_desc": "List currently loaded and active systemd units.",
                "detailed_desc": "Displays unit names, load state, active state, substate, and description.",
                "category": "Unit Inspection",
                "common_flags": [
                    {"flag": "--type=service", "desc": "Filter only service units."},
                    {"flag": "--state=failed", "desc": "Find any crashed or failed services on the machine."}
                ],
                "sample_output": """0 loaded units listed.
Pass --all to see loaded but inactive units, too.""",
                "rhcsa_tips": ["'systemctl --failed' instantly identifies broken services when troubleshooting a server."],
                "default_run_cmd": "systemctl --failed"
            },
            {
                "id": "ch11_systemd_analyze",
                "name": "systemd-analyze",
                "synopsis": "systemd-analyze [blame | critical-chain | time]",
                "short_desc": "Profile system boot performance and identify bottlenecks.",
                "detailed_desc": "Breakdowns kernel and userspace boot duration, identifying the slowest starting services.",
                "category": "Performance Analysis",
                "common_flags": [
                    {"flag": "blame", "desc": "List all running units ordered by initialization time."},
                    {"flag": "time", "desc": "Show total boot breakdown for kernel and userspace."}
                ],
                "sample_output": """Startup finished in 1.412s (kernel) + 2.890s (userspace) = 4.302s 
multi-user.target reached after 2.850s in userspace""",
                "rhcsa_tips": ["Use 'systemd-analyze blame' to pinpoint slow boot services."],
                "default_run_cmd": "systemd-analyze time"
            }
        ]
    },

    # CHAPTER 12: Scheduling Tasks
    {
        "chapter_id": 12,
        "part_id": 2,
        "part_title": "Part II: Operating Running Systems",
        "chapter_title": "Scheduling Tasks",
        "description": "Recurring cron automation (/etc/crontab, /var/spool/cron/), one-time tasks with at, and modern systemd timer units.",
        "commands": [
            {
                "id": "ch12_crontab_l",
                "name": "crontab -l",
                "synopsis": "crontab [-u user] -l",
                "short_desc": "Display the current user's crontab entries.",
                "detailed_desc": "Lists the active cron schedule for the designated user.",
                "category": "Task Scheduling",
                "common_flags": [
                    {"flag": "-u <user>", "desc": "Display specific user's crontab (root only)."}
                ],
                "sample_output": """# minute hour day_of_month month day_of_week command
0 2 * * * /usr/local/bin/backup.sh
*/15 * * * * /usr/bin/logger "Health check running" """,
                "rhcsa_tips": ["Format: Minute (0-59), Hour (0-23), Day of Month (1-31), Month (1-12), Day of Week (0-7, 0/7=Sun)."],
                "default_run_cmd": "crontab -l"
            },
            {
                "id": "ch12_crontab_e",
                "name": "crontab -e",
                "synopsis": "crontab [-u user] -e",
                "short_desc": "Edit current user's crontab file with syntax verification.",
                "detailed_desc": "Opens user crontab in default editor (vi) and verifies syntax upon saving.",
                "category": "Task Scheduling",
                "common_flags": [
                    {"flag": "-u <user>", "desc": "Edit crontab for another user (e.g. crontab -u natasha -e)."}
                ],
                "sample_output": "crontab: installing new crontab",
                "rhcsa_tips": [
                    "RHCSA EXAM OBJECTIVE: 'Schedule a job for user natasha to run every day at 14:23': crontab -u natasha -e -> 23 14 * * * /usr/bin/logger hello."
                ],
                "default_run_cmd": "crontab --help"
            },
            {
                "id": "ch12_at",
                "name": "at",
                "synopsis": "at [-q queue] [-f file] TIME",
                "short_desc": "Queue jobs for later one-time execution.",
                "detailed_desc": "Schedules a one-off command to run at a specified future timestamp (e.g. 'at 2am tomorrow').",
                "category": "One-time Tasks",
                "common_flags": [
                    {"flag": "-f <file>", "desc": "Read commands from file instead of standard input."}
                ],
                "sample_output": """warning: commands will be executed using /bin/sh
job 1 at Wed Sep 24 18:30:00 2026""",
                "rhcsa_tips": ["Ensure 'atd' service is active: 'systemctl is-active atd'."],
                "default_run_cmd": "at -V"
            },
            {
                "id": "ch12_atq",
                "name": "atq",
                "synopsis": "atq [-q queue] [-v]",
                "short_desc": "List queued jobs pending execution with 'at'.",
                "detailed_desc": "Displays pending at job numbers, execution time, and user owner.",
                "category": "One-time Tasks",
                "common_flags": [],
                "sample_output": "1	Wed Sep 24 18:30:00 2026 a root",
                "rhcsa_tips": ["Use atq to retrieve the job number before deleting it with atrm."],
                "default_run_cmd": "atq"
            },
            {
                "id": "ch12_atrm",
                "name": "atrm",
                "synopsis": "atrm job [job...]",
                "short_desc": "Delete queued jobs scheduled with 'at'.",
                "detailed_desc": "Cancels pending one-off jobs by job ID.",
                "category": "One-time Tasks",
                "common_flags": [],
                "sample_output": "Removed job 1.",
                "rhcsa_tips": ["Only job owners or root can remove queued at jobs."],
                "default_run_cmd": "atrm --help"
            },
            {
                "id": "ch12_list_timers",
                "name": "systemctl list-timers",
                "synopsis": "systemctl list-timers [PATTERN...]",
                "short_desc": "List systemd timer units and next scheduled trigger time.",
                "detailed_desc": "Shows active systemd timers (modern alternative to cron), next trigger time, and associated target service.",
                "category": "Systemd Timers",
                "common_flags": [
                    {"flag": "--all", "desc": "Show loaded but inactive timers as well."}
                ],
                "sample_output": """NEXT                         LEFT        LAST                         PASSED    UNIT                         ACTIVATES
Wed 2026-09-24 18:00:00 EDT  4min left   Wed 2026-09-24 17:00:00 EDT  55min ago sysstat-collect.timer        sysstat-collect.service
Thu 2026-09-25 00:00:00 EDT  6h left     Wed 2026-09-24 00:00:00 EDT  17h ago   logrotate.timer              logrotate.service""",
                "rhcsa_tips": ["Systemd timers end in '.timer' and trigger matching '.service' units (e.g., backup.timer triggers backup.service)."],
                "default_run_cmd": "systemctl list-timers"
            },
            {
                "id": "ch12_systemd_run",
                "name": "systemd-run",
                "synopsis": "systemd-run [OPTIONS...] COMMAND [ARGS...]",
                "short_desc": "Run programs in transient scope or timer units.",
                "detailed_desc": "Executes commands under systemd control with cgroup resource limits and optional timer delays.",
                "category": "Transient Execution",
                "common_flags": [
                    {"flag": "--on-active=30s", "desc": "Execute 30 seconds after invoking."},
                    {"flag": "--unit=<NAME>", "desc": "Assign custom unit name."}
                ],
                "sample_output": "Running as unit: run-u124.service",
                "rhcsa_tips": ["Handy for testing one-time automated tasks under strict cgroup limits."],
                "default_run_cmd": "systemd-run --help | head -n 12"
            },
            {
                "id": "ch12_anacron",
                "name": "anacron",
                "synopsis": "anacron [-s] [-f] [-n] [-d] [job]...",
                "short_desc": "Run periodic jobs on systems that do not run continuously.",
                "detailed_desc": "Executes daily, weekly, and monthly jobs specified in /etc/anacrontab even if server was powered off during normal cron schedule.",
                "category": "Periodic Tasks",
                "common_flags": [
                    {"flag": "-u", "desc": "Update timestamps of jobs to current date without running them."}
                ],
                "sample_output": "Anacron 2.3 started on 2026-09-24\nNormal exit (0 jobs run)",
                "rhcsa_tips": ["Standard /etc/cron.daily jobs on RHEL 9 are dispatched via anacron."],
                "default_run_cmd": "cat /etc/anacrontab"
            },
            {
                "id": "ch12_sleep",
                "name": "sleep",
                "synopsis": "sleep NUMBER[SUFFIX]...",
                "short_desc": "Delay execution for a specified amount of time.",
                "detailed_desc": "Pauses shell script execution for designated seconds (s), minutes (m), hours (h), or days (d).",
                "category": "Script Automation",
                "common_flags": [],
                "sample_output": "[Execution paused for 5 seconds]",
                "rhcsa_tips": ["Useful in system startup scripts waiting for network interfaces to settle."],
                "default_run_cmd": "sleep 1"
            },
            {
                "id": "ch12_batch",
                "name": "batch",
                "synopsis": "batch [options]",
                "short_desc": "Queue commands to execute only when system load permits.",
                "detailed_desc": "Part of the 'at' package; runs queued tasks when system load average drops below 1.5.",
                "category": "One-time Tasks",
                "common_flags": [],
                "sample_output": "warning: commands will be executed using /bin/sh\njob 2 at Wed Sep 24 18:35:00 2026",
                "rhcsa_tips": ["Great for resource-heavy batch scripts that shouldn't impact foreground users."],
                "default_run_cmd": "batch -V"
            }
        ]
    },

    # CHAPTER 13: Configuring Logging
    {
        "chapter_id": 13,
        "part_id": 2,
        "part_title": "Part II: Operating Running Systems",
        "chapter_title": "Configuring Logging",
        "description": "Systemd journal inspection (journalctl), rsyslog routing, log persistence, logrotate policies, and kernel ring buffer.",
        "commands": [
            {
                "id": "ch13_journalctl",
                "name": "journalctl",
                "synopsis": "journalctl [OPTIONS...] [MATCHES...]",
                "short_desc": "Query and inspect the systemd journal logs.",
                "detailed_desc": "Main logging query tool in RHEL 9; accesses structured binary journal logs from systemd-journald.",
                "category": "System Logging",
                "common_flags": [
                    {"flag": "-u <UNIT>", "desc": "Filter logs specifically for a systemd unit (e.g., journalctl -u sshd)."},
                    {"flag": "-b", "desc": "Show logs from the current boot only (or -b -1 for previous boot)."},
                    {"flag": "-p <PRIORITY>", "desc": "Filter by priority level (e.g. -p err for errors only)."},
                    {"flag": "-e", "desc": "Jump immediately to the end of the pager."},
                    {"flag": "-f, --follow", "desc": "Live stream new log events in real time."}
                ],
                "sample_output": """Sep 24 16:30:10 rhel9-node1 systemd[1]: Starting The Apache HTTP Server...
Sep 24 16:30:11 rhel9-node1 httpd[1240]: AH00558: httpd: Could not reliably determine server's FQDN
Sep 24 16:30:11 rhel9-node1 systemd[1]: Started The Apache HTTP Server.""",
                "rhcsa_tips": [
                    "RHCSA ESSENTIAL: 'journalctl -xeu <service>' is the exact command when a service fails to start and systemctl tells you 'See journalctl -xe for details'!"
                ],
                "default_run_cmd": "journalctl -n 15 --no-pager"
            },
            {
                "id": "ch13_logger",
                "name": "logger",
                "synopsis": "logger [options] [message]",
                "short_desc": "Enter messages into the system log from command line or scripts.",
                "detailed_desc": "Sends custom log entries directly to syslog/journald with specified tag and facility priority.",
                "category": "System Logging",
                "common_flags": [
                    {"flag": "-p <FACILITY.PRIO>", "desc": "Specify log facility and priority (e.g. -p local0.err)."},
                    {"flag": "-t <TAG>", "desc": "Mark log entries with custom tag name."}
                ],
                "sample_output": "[Message logged to system journal]",
                "rhcsa_tips": ["Test rsyslog filter rules with: 'logger -p local0.info \"Test logging event\"'."],
                "default_run_cmd": "logger 'Linux Simulator Test Log' && journalctl -n 1 --no-pager"
            },
            {
                "id": "ch13_tail_messages",
                "name": "tail -f /var/log/messages",
                "synopsis": "tail -f /var/log/messages",
                "short_desc": "Live monitor general system messages handled by rsyslog.",
                "detailed_desc": "Traditional flat log file containing non-security system messages, hardware plug-in events, and daemon statuses.",
                "category": "Rsyslog Logs",
                "common_flags": [],
                "sample_output": """Sep 24 17:50:01 rhel9-node1 systemd[1]: Started Session 14 of User student.
Sep 24 17:52:10 rhel9-node1 kernel: usb 1-1: USB disconnect, device number 3""",
                "rhcsa_tips": ["General troubleshooting go-to log along with journalctl."],
                "default_run_cmd": "tail -n 10 /var/log/messages"
            },
            {
                "id": "ch13_tail_secure",
                "name": "tail -f /var/log/secure",
                "synopsis": "tail -f /var/log/secure",
                "short_desc": "Monitor authentication, sudo, and SSH security logs.",
                "detailed_desc": "Records all successful and failed PAM logins, SSH authentications, sudo command executions, and privilege escalation attempts.",
                "category": "Security Logs",
                "common_flags": [],
                "sample_output": """Sep 24 17:42:15 rhel9-node1 sshd[4135]: Accepted publickey for student from 192.168.1.100 port 52310 ssh2
Sep 24 17:42:15 rhel9-node1 sshd[4135]: pam_unix(sshd:session): session opened for user student(uid=1000)
Sep 24 17:45:00 rhel9-node1 sudo[4200]:  student : TTY=pts/0 ; PWD=/home/student ; USER=root ; COMMAND=/bin/systemctl status""",
                "rhcsa_tips": ["RHCSA TROUBLESHOOTING: When SSH key login fails or a user cannot sudo, inspect /var/log/secure immediately."],
                "default_run_cmd": "tail -n 10 /var/log/secure"
            },
            {
                "id": "ch13_rsyslogd",
                "name": "rsyslogd",
                "synopsis": "rsyslogd [options]",
                "short_desc": "Reliable and extended syslog daemon.",
                "detailed_desc": "Dispatches logs according to rules in /etc/rsyslog.conf and /etc/rsyslog.d/*.conf to local files or remote syslog collectors.",
                "category": "Syslog Daemon",
                "common_flags": [
                    {"flag": "-N 1", "desc": "Check configuration file syntax without starting the daemon."}
                ],
                "sample_output": "rsyslogd: version 8.2102.0-10.el9, config validation run... SUCCESS",
                "rhcsa_tips": ["Always test rsyslog syntax with 'rsyslogd -N 1' before restarting rsyslog service!"],
                "default_run_cmd": "rsyslogd -v"
            },
            {
                "id": "ch13_logrotate",
                "name": "logrotate",
                "synopsis": "logrotate [options] <configfile>",
                "short_desc": "Rotates, compresses, and purges system log files.",
                "detailed_desc": "Automates log retention policies configured in /etc/logrotate.conf and /etc/logrotate.d/ (daily, weekly, rotate count, compress).",
                "category": "Log Maintenance",
                "common_flags": [
                    {"flag": "-f, --force", "desc": "Force log rotation even if time period has not elapsed."},
                    {"flag": "-d, --debug", "desc": "Dry run; print what would be done without modifying files."}
                ],
                "sample_output": """reading config file /etc/logrotate.conf
Handling 12 logs
rotating pattern: /var/log/httpd/*log  after 1 days (7 rotations)
log does not need rotating (log is empty)""",
                "rhcsa_tips": ["'logrotate -d /etc/logrotate.conf' is the safe way to debug your rotation policies."],
                "default_run_cmd": "logrotate -d /etc/logrotate.conf"
            },
            {
                "id": "ch13_dmesg",
                "name": "dmesg",
                "synopsis": "dmesg [options]",
                "short_desc": "Print or control the kernel ring buffer.",
                "detailed_desc": "Displays hardware detection and kernel initialization messages.",
                "category": "Kernel Logging",
                "common_flags": [
                    {"flag": "-T, --ctime", "desc": "Print human-readable real timestamps instead of delta seconds."},
                    {"flag": "-l, --level <list>", "desc": "Filter by message level (emerg, alert, crit, err, warn)."}
                ],
                "sample_output": """[Wed Sep 24 10:00:00 2026] Linux version 5.14.0-284.11.1.el9_2.x86_64
[Wed Sep 24 10:00:01 2026] e1000: enp1s0 NIC Link is Up 1000 Mbps Full Duplex""",
                "rhcsa_tips": ["'dmesg -T | grep -i error' quickly shows disk hardware I/O errors."],
                "default_run_cmd": "dmesg -T | head -n 12"
            },
            {
                "id": "ch13_journal_persistent",
                "name": "mkdir -p /var/log/journal",
                "synopsis": "mkdir -p /var/log/journal && systemctl restart systemd-journald",
                "short_desc": "Configure persistent systemd journal storage across reboots.",
                "detailed_desc": "By default in RHEL, volatile journal logs live in RAM (/run/log/journal). Creating /var/log/journal makes them persistent on disk.",
                "category": "Log Configuration",
                "common_flags": [],
                "sample_output": "Permanent journal directory active at /var/log/journal/d4e1c278923a4bf88a6d9124fb7e0123",
                "rhcsa_tips": [
                    "RHCSA OBJECTIVE: 'Configure systemd-journald to store log files persistently': set 'Storage=persistent' in /etc/systemd/journald.conf and restart systemd-journald."
                ],
                "default_run_cmd": "ls -d /var/log/journal 2>/dev/null || echo 'Volatile journal'"
            },
            {
                "id": "ch13_lastlog",
                "name": "lastlog",
                "synopsis": "lastlog [options]",
                "short_desc": "Reports the most recent login of all users or specified user.",
                "detailed_desc": "Queries /var/log/lastlog and formats the last login date, terminal, and source IP.",
                "category": "User Auditing",
                "common_flags": [
                    {"flag": "-u <user>", "desc": "Display last login for specified user only."}
                ],
                "sample_output": """Username         Port     From             Latest
root             pts/0    192.168.1.100    Wed Sep 24 14:02:10 -0400 2026
student          pts/1    192.168.1.105    Wed Sep 24 16:30:00 -0400 2026
bin                                        **Never logged in**""",
                "rhcsa_tips": ["Useful to audit stale accounts that haven't logged in for months."],
                "default_run_cmd": "lastlog | head -n 10"
            },
            {
                "id": "ch13_systemd_cat",
                "name": "systemd-cat",
                "synopsis": "systemd-cat [OPTIONS...] [COMMAND...]",
                "short_desc": "Connect a pipeline or program output directly to the system journal.",
                "detailed_desc": "Executes a binary and redirects both its stdout and stderr directly into systemd-journald.",
                "category": "System Logging",
                "common_flags": [
                    {"flag": "-t <identifier>", "desc": "Set syslog identifier tag."}
                ],
                "sample_output": "[Program output piped to journal]",
                "rhcsa_tips": ["Handy in custom automated admin scripts."],
                "default_run_cmd": "systemd-cat echo 'Logged via systemd-cat'"
            }
        ]
    },

    # CHAPTER 14: Managing Storage
    {
        "chapter_id": 14,
        "part_id": 2,
        "part_title": "Part II: Operating Running Systems",
        "chapter_title": "Managing Storage",
        "description": "Partitioning (MBR/GPT), filesystem creation (XFS, Ext4), persistent mounting (/etc/fstab), UUID identification, and disk space usage.",
        "commands": [
            {
                "id": "ch14_fdisk",
                "name": "fdisk",
                "synopsis": "fdisk [options] <device>",
                "short_desc": "Manipulate disk partition table (MBR/GPT).",
                "detailed_desc": "Interactive tool to create MBR/GPT partitions: 'n' (new), 'p' (print), 'd' (delete), 't' (type), 'w' (write).",
                "category": "Partitioning",
                "common_flags": [
                    {"flag": "-l", "desc": "List partitions on all block devices."}
                ],
                "sample_output": """Disk /dev/vdb: 10 GiB, 10737418240 bytes, 20971520 sectors
Units: sectors of 1 * 512 = 512 bytes
Device       Start      End  Sectors Size Type
/dev/vdb1     2048  4196351  4194304   2G Linux filesystem""",
                "rhcsa_tips": ["After writing changes with 'w', run 'udevadm settle' or 'partprobe' to force the kernel to register the new partition."],
                "default_run_cmd": "fdisk -l /dev/vda 2>/dev/null || fdisk -l"
            },
            {
                "id": "ch14_gdisk",
                "name": "gdisk",
                "synopsis": "gdisk <device>",
                "short_desc": "Interactive GUID Partition Table (GPT) manipulator.",
                "detailed_desc": "Dedicated GPT partitioning tool for modern large drives (>2TB) or UEFI setups.",
                "category": "Partitioning",
                "common_flags": [
                    {"flag": "-l <device>", "desc": "List partition table for GPT disk."}
                ],
                "sample_output": "Partition table scan: MBR: protective, BSD: not present, GPT: present",
                "rhcsa_tips": ["Standard partition type for LVM in gdisk is '8e00'."],
                "default_run_cmd": "gdisk -l /dev/vda 2>/dev/null"
            },
            {
                "id": "ch14_parted",
                "name": "parted",
                "synopsis": "parted [options] [device [command [options...]...]]",
                "short_desc": "Partition manipulation program with command-line non-interactive support.",
                "detailed_desc": "Script-friendly partitioning tool allowing single-line commands (e.g. parted -s /dev/vdb mklabel gpt mkpart primary xfs 1MiB 2GiB).",
                "category": "Partitioning",
                "common_flags": [
                    {"flag": "-s, --script", "desc": "Never prompt for user intervention (script mode)."},
                    {"flag": "-l", "desc": "List partition layout on all block devices."}
                ],
                "sample_output": """Model: Virtio Block Device (virtblk)
Disk /dev/vdb: 10.7GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags: 
Number  Start   End     Size    File system  Name     Flags
 1      1049kB  2149MB  2147MB  xfs          primary""",
                "rhcsa_tips": ["Use 'parted -s /dev/vdb print' for fast script verification."],
                "default_run_cmd": "parted -l 2>/dev/null"
            },
            {
                "id": "ch14_mkfs_xfs",
                "name": "mkfs.xfs",
                "synopsis": "mkfs.xfs [options] device",
                "short_desc": "Format a partition with the default RHEL XFS filesystem.",
                "detailed_desc": "High-performance enterprise 64-bit journaling filesystem, default in RHEL 9.",
                "category": "Filesystem Formatting",
                "common_flags": [
                    {"flag": "-f", "desc": "Force overwrite existing filesystem on device."}
                ],
                "sample_output": """meta-data=/dev/vdb1              isize=512    agcount=4, agsize=131072 blks
         =                       sectsz=512   attr=2, projid32bit=1
data     =                       bsize=4096   blocks=524288, imaxpct=25
naming   =version 2              bsize=4096   ascii-ci=0, ftype=1
log      =internal log           bsize=4096   blocks=16384, version=2
realtime =none                   extsz=4096   blocks=0, rtextents=0""",
                "rhcsa_tips": [
                    "CRITICAL NOTE: XFS filesystems CAN BE EXTENDED (xfs_growfs), but CANNOT BE REDUCED / SHRUNK! Never attempt to shrink an XFS partition."
                ],
                "default_run_cmd": "mkfs.xfs -V"
            },
            {
                "id": "ch14_mkfs_ext4",
                "name": "mkfs.ext4",
                "synopsis": "mkfs.ext4 [options] device",
                "short_desc": "Format a partition with the Ext4 journaling filesystem.",
                "detailed_desc": "Fourth extended filesystem; supports both growing and shrinking (resize2fs).",
                "category": "Filesystem Formatting",
                "common_flags": [
                    {"flag": "-L <label>", "desc": "Set volume label."},
                    {"flag": "-m <reserved_pct>", "desc": "Set percentage of reserved blocks for superuser (default 5%)."}
                ],
                "sample_output": """Creating filesystem with 524288 4k blocks and 131072 inodes
Filesystem UUID: a1b2c3d4-e5f6-7890-abcd-ef1234567890
Superblock backups stored on blocks: 
	32768, 98304, 163840, 229376, 294912""",
                "rhcsa_tips": ["Ext4 can be reduced safely, unlike XFS. If an exam question asks to shrink storage, use Ext4!"],
                "default_run_cmd": "mkfs.ext4 -V"
            },
            {
                "id": "ch14_mount",
                "name": "mount",
                "synopsis": "mount [-t fstype] [-o options] device dir",
                "short_desc": "Mount a storage filesystem to a directory path.",
                "detailed_desc": "Attaches the filesystem on designated device to the directory tree at mountpoint.",
                "category": "Mounting",
                "common_flags": [
                    {"flag": "-a", "desc": "Mount ALL filesystems mentioned in /etc/fstab (vital for testing fstab syntax!)."},
                    {"flag": "-o <options>", "desc": "Specify mount options (e.g. -o ro,noexec,defaults)."}
                ],
                "sample_output": "/dev/vdb1 mounted on /data",
                "rhcsa_tips": [
                    "RHCSA MANDATORY GOLDEN RULE: Whenever you edit /etc/fstab, ALWAYS test it immediately with 'mount -a'! If there is a typo, mount -a will report it before you reboot and brick the server into emergency mode!"
                ],
                "default_run_cmd": "mount | grep ' / ' "
            },
            {
                "id": "ch14_umount",
                "name": "umount",
                "synopsis": "umount [-f] {dir | device}...",
                "short_desc": "Unmount filesystems.",
                "detailed_desc": "Detaches the mounted filesystem safely, flushing pending disk buffers.",
                "category": "Mounting",
                "common_flags": [
                    {"flag": "-l, --lazy", "desc": "Detach immediately and clean up all references when device is unbusy."}
                ],
                "sample_output": "umount: /data unmounted",
                "rhcsa_tips": ["If umount returns 'target is busy', use 'lsof +D /data' or 'fuser -m /data' to find which process is inside the directory."],
                "default_run_cmd": "umount --help"
            },
            {
                "id": "ch14_blkid",
                "name": "blkid",
                "synopsis": "blkid [options] [device...]",
                "short_desc": "Locate and print block device attributes (UUID, filesystem type).",
                "detailed_desc": "Identifies Universally Unique Identifiers (UUID) required for reliable persistent /etc/fstab entries.",
                "category": "Storage Query",
                "common_flags": [
                    {"flag": "-s UUID", "desc": "Show only the UUID token."}
                ],
                "sample_output": """/dev/vda1: UUID="7a8b9c0d-1234-5678-9abc-def012345678" TYPE="xfs"
/dev/vda2: UUID="f0e1d2c3-4567-89ab-cdef-0123456789ab" TYPE="LVM2_member"
/dev/vdb1: UUID="3d4e5f6a-7b8c-9d0e-1f2a-3b4c5d6e7f8a" TYPE="xfs" """,
                "rhcsa_tips": [
                    "RHCSA BEST PRACTICE: In /etc/fstab, NEVER use device nodes like /dev/vdb1 (names change on reboot!). ALWAYS use UUID=\"...\": 'UUID=3d4e5f6a... /data xfs defaults 0 0'."
                ],
                "default_run_cmd": "blkid"
            },
            {
                "id": "ch14_df",
                "name": "df",
                "synopsis": "df [OPTION]... [FILE]...",
                "short_desc": "Report filesystem disk space usage.",
                "detailed_desc": "Displays total size, used space, available space, percentage capacity, and mountpoint.",
                "category": "Storage Metrics",
                "common_flags": [
                    {"flag": "-h, --human-readable", "desc": "Print sizes in powers of 1024 (e.g., 1024M, 20G)."},
                    {"flag": "-T, --print-type", "desc": "Print filesystem type (xfs, ext4, nfs)."}
                ],
                "sample_output": """Filesystem          Type      Size  Used Avail Use% Mounted on
devtmpfs            devtmpfs  1.8G     0  1.8G   0% /dev
/dev/mapper/rhel-root xfs       35G  4.2G   31G  12% /
/dev/vda1           xfs      1014M  280M  735M  28% /boot
/dev/vdb1           xfs       2.0G   47M  2.0G   3% /data""",
                "rhcsa_tips": ["Always run 'df -hT' to verify that newly configured mounts appear correctly with expected capacity."],
                "default_run_cmd": "df -hT"
            },
            {
                "id": "ch14_du",
                "name": "du",
                "synopsis": "du [OPTION]... [FILE]...",
                "short_desc": "Estimate file space usage per directory.",
                "detailed_desc": "Traverses directories recursively to calculate disk space consumed by files and folders.",
                "category": "Storage Metrics",
                "common_flags": [
                    {"flag": "-s, --summarize", "desc": "Display only a total for each argument."},
                    {"flag": "-h, --human-readable", "desc": "Print sizes in human readable format."}
                ],
                "sample_output": "1.4G	/var/log\n450M	/var/log/audit\n820M	/var/log/journal",
                "rhcsa_tips": ["Find what is filling up a partition: 'du -sh /var/* | sort -h'."],
                "default_run_cmd": "du -sh /var/log 2>/dev/null"
            }
        ]
    },

    # CHAPTER 15: Managing Advanced Storage
    {
        "chapter_id": 15,
        "part_id": 2,
        "part_title": "Part II: Operating Running Systems",
        "chapter_title": "Managing Advanced Storage",
        "description": "Logical Volume Manager (LVM) workflow (PVs, VGs, LVs), online filesystem extension, and Stratis storage management.",
        "commands": [
            {
                "id": "ch15_pvcreate",
                "name": "pvcreate",
                "synopsis": "pvcreate [options] PhysicalVolume [PhysicalVolume...]",
                "short_desc": "Initialize physical volumes for use by LVM.",
                "detailed_desc": "Formats a partition or whole block device with LVM metadata headers so it can join a Volume Group.",
                "category": "LVM Physical Volumes",
                "common_flags": [],
                "sample_output": "Physical volume \"/dev/vdb1\" successfully created.",
                "rhcsa_tips": ["LVM Step 1: Initialize physical volumes with 'pvcreate /dev/vdb1 /dev/vdb2'."],
                "default_run_cmd": "pvs"
            },
            {
                "id": "ch15_vgcreate",
                "name": "vgcreate",
                "synopsis": "vgcreate [options] VolumeGroupName PhysicalVolumePath...",
                "short_desc": "Create a volume group pooling multiple physical volumes.",
                "detailed_desc": "Aggregates storage from PVs into a unified storage pool, divided into Physical Extents (PEs, default 4MB).",
                "category": "LVM Volume Groups",
                "common_flags": [
                    {"flag": "-s <size>", "desc": "Specify physical extent (PE) size (e.g. -s 8M or -s 16M)."}
                ],
                "sample_output": "Volume group \"research_vg\" successfully created with extent size 4.00 MiB.",
                "rhcsa_tips": [
                    "RHCSA EXAM OBJECTIVE: 'Create volume group research_vg with physical extent size of 8MB': vgcreate -s 8M research_vg /dev/vdb1."
                ],
                "default_run_cmd": "vgs"
            },
            {
                "id": "ch15_lvcreate",
                "name": "lvcreate",
                "synopsis": "lvcreate [options] -n LogicalVolume VolumeGroup",
                "short_desc": "Create a logical volume within an existing volume group.",
                "detailed_desc": "Carves out a block device of designated size or extent count from a Volume Group pool.",
                "category": "LVM Logical Volumes",
                "common_flags": [
                    {"flag": "-L <size>", "desc": "Specify exact size (e.g. -L 500M or -L 2G)."},
                    {"flag": "-l <extents>", "desc": "Specify number of extents (e.g. -l 50 or -l 100%FREE)."},
                    {"flag": "-n <name>", "desc": "Assign custom name for the logical volume."}
                ],
                "sample_output": "Logical volume \"data_lv\" created.",
                "rhcsa_tips": [
                    "RHCSA TRICK: Pay attention to capital vs lowercase L: '-L 500M' is by size (Megabytes), whereas '-l 50' is by number of Extents!"
                ],
                "default_run_cmd": "lvs"
            },
            {
                "id": "ch15_pvs",
                "name": "pvs",
                "synopsis": "pvs [options] [PhysicalVolume...]",
                "short_desc": "Display information about physical volumes in a compact format.",
                "detailed_desc": "Lists PV name, parent VG, format, total size, and free unallocated space.",
                "category": "LVM Inspection",
                "common_flags": [],
                "sample_output": """  PV         VG   Fmt  Attr PSize   PFree 
  /dev/vda2  rhel lvm2 a--  <39.00g     0 
  /dev/vdb1  vg01 lvm2 a--   <2.00g <1.50g""",
                "rhcsa_tips": ["Use 'pvdisplay' if you need verbose extent-by-extent information."],
                "default_run_cmd": "pvs"
            },
            {
                "id": "ch15_vgs",
                "name": "vgs",
                "synopsis": "vgs [options] [VolumeGroup...]",
                "short_desc": "Display information about volume groups.",
                "detailed_desc": "Reports VG name, number of PVs, number of LVs, extent size, total capacity, and free capacity.",
                "category": "LVM Inspection",
                "common_flags": [],
                "sample_output": """  VG   #PV #LV #SN Attr   VSize   VFree 
  rhel   1   2   0 wz--n- <39.00g     0 
  vg01   1   1   0 wz--n-  <2.00g <1.50g""",
                "rhcsa_tips": ["Always check 'VFree' before creating new logical volumes to ensure adequate space exists."],
                "default_run_cmd": "vgs"
            },
            {
                "id": "ch15_lvs",
                "name": "lvs",
                "synopsis": "lvs [options] [LogicalVolume...]",
                "short_desc": "Display information about logical volumes.",
                "detailed_desc": "Lists LV name, parent VG, attributes, and size.",
                "category": "LVM Inspection",
                "common_flags": [],
                "sample_output": """  LV   VG   Attr       LSize   Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
  root rhel -wi-ao---- <35.00g                                                    
  swap rhel -wi-ao----   4.00g                                                    
  data vg01 -wi-a----- 500.00m                                                    """,
                "rhcsa_tips": ["The block device path for an LV is '/dev/mapper/VG-LV' or '/dev/VG/LV'."],
                "default_run_cmd": "lvs"
            },
            {
                "id": "ch15_lvextend",
                "name": "lvextend",
                "synopsis": "lvextend [options] -L [+]size LogicalVolumePath",
                "short_desc": "Extend the size of a logical volume.",
                "detailed_desc": "Allocates additional extents to a logical volume, optionally resizing the underlying filesystem simultaneously.",
                "category": "LVM Extension",
                "common_flags": [
                    {"flag": "-r, --resizefs", "desc": "MAGIC FLAG: Automatically resizes underlying XFS/Ext4 filesystem online in the same command!"},
                    {"flag": "-L +<size>", "desc": "Increase size by amount (e.g., -L +500M)."},
                    {"flag": "-L <size>", "desc": "Grow to an absolute final size (e.g., -L 2G)."}
                ],
                "sample_output": """  Size of logical volume vg01/data changed from 500.00 MiB to 1.00 GiB.
  Logical volume vg01/data successfully resized.
meta-data=/dev/mapper/vg01-data  isize=512    agcount=4, agsize=32000 blks
data blocks changed from 128000 to 262144
xfs_growfs: filesystem successfully resized.""",
                "rhcsa_tips": [
                    "RHCSA LIFESAVER: Always include '-r' when extending: 'lvextend -r -L 1G /dev/vg01/data'. This resizes both the LV AND the filesystem in a single error-proof step!"
                ],
                "default_run_cmd": "lvextend --help | head -n 15"
            },
            {
                "id": "ch15_vgextend",
                "name": "vgextend",
                "synopsis": "vgextend VolumeGroupName PhysicalDevice...",
                "short_desc": "Add new physical volumes to an existing volume group.",
                "detailed_desc": "Expands the available storage pool of an existing Volume Group by assimilating new PVs.",
                "category": "LVM Volume Groups",
                "common_flags": [],
                "sample_output": "Volume group \"vg01\" successfully extended with /dev/vdc1.",
                "rhcsa_tips": ["If a Volume Group runs out of free space, format a new disk with pvcreate and add it via vgextend."],
                "default_run_cmd": "vgextend --help"
            },
            {
                "id": "ch15_xfs_growfs",
                "name": "xfs_growfs",
                "synopsis": "xfs_growfs [options] mountpoint",
                "short_desc": "Expand an existing XFS filesystem to fill its underlying block device.",
                "detailed_desc": "Online tool to grow an XFS filesystem after the underlying LV or partition has been enlarged.",
                "category": "Filesystem Resizing",
                "common_flags": [],
                "sample_output": "data blocks changed from 128000 to 262144",
                "rhcsa_tips": [
                    "XFS TRICK: 'xfs_growfs' takes the MOUNTPOINT as an argument (e.g. xfs_growfs /data), NOT the /dev block device!"
                ],
                "default_run_cmd": "xfs_growfs -V"
            },
            {
                "id": "ch15_stratis",
                "name": "stratis",
                "synopsis": "stratis [options] {pool | filesystem | blockdev} ...",
                "short_desc": "Manage Stratis pooled storage and thin-provisioned filesystems.",
                "detailed_desc": "Red Hat's local hybrid storage management solution combining XFS and device-mapper with thin provisioning.",
                "category": "Stratis Storage",
                "common_flags": [
                    {"flag": "pool create <pool> <dev>", "desc": "Create a Stratis storage pool."},
                    {"flag": "fs create <pool> <fs_name>", "desc": "Create a dynamically expanding filesystem in the pool."},
                    {"flag": "pool list", "desc": "List active Stratis pools and capacity."}
                ],
                "sample_output": """Name          Total Physical  Properties                                   UUID
storage_pool  10 GiB / 40 MiB ~ca,~cr                                      89e1a2b3-4c5d...""",
                "rhcsa_tips": [
                    "RHCSA OBJECTIVE: In /etc/fstab, Stratis filesystems MUST use mount options 'defaults,x-systemd.requires=stratisd.service'!"
                ],
                "default_run_cmd": "stratis --version 2>/dev/null || echo 'stratis-cli available via dnf'"
            }
        ]
    }
]
