"""
Part III: Performing Advanced System Administration Tasks (Chapters 16 - 19)
10 Essential Commands per Chapter (40 commands total)
"""

PART_3_CHAPTERS = [
    # CHAPTER 16: Basic Kernel Management
    {
        "chapter_id": 16,
        "part_id": 3,
        "part_title": "Part III: Performing Advanced System Administration Tasks",
        "chapter_title": "Basic Kernel Management",
        "description": "Kernel modules (drivers), runtime kernel parameters (/proc/sys, sysctl), persistent configuration (/etc/sysctl.d), and initramfs generation.",
        "commands": [
            {
                "id": "ch16_lsmod",
                "name": "lsmod",
                "synopsis": "lsmod",
                "short_desc": "Show the status of modules in the Linux Kernel.",
                "detailed_desc": "Formats the contents of /proc/modules, showing currently loaded drivers, memory footprint, and dependent modules.",
                "category": "Kernel Modules",
                "common_flags": [],
                "sample_output": """Module                  Size  Used by
overlay               151552  0
kvm_intel             372736  0
kvm                  1064960  1 kvm_intel
virtio_net             61440  0
net_failover           24576  1 virtio_net""",
                "rhcsa_tips": ["Pipe with grep: 'lsmod | grep -i kvm' to verify if a virtualization or storage driver is loaded."],
                "default_run_cmd": "lsmod | head -n 12"
            },
            {
                "id": "ch16_modinfo",
                "name": "modinfo",
                "synopsis": "modinfo [options] [modulename...]",
                "short_desc": "Show information about a Linux Kernel module.",
                "detailed_desc": "Extracts author, license, description, file path (.ko.xz), dependencies, and configurable parameters of a kernel driver.",
                "category": "Kernel Modules",
                "common_flags": [
                    {"flag": "-p, --parameters", "desc": "Print module parameters and their types."},
                    {"flag": "-d, --description", "desc": "Print module description."}
                ],
                "sample_output": """filename:       /lib/modules/5.14.0-284.11.1.el9_2.x86_64/kernel/drivers/net/virtio_net.ko.xz
license:        GPL
description:    Virtio network driver
author:         Rusty Russell <rusty@rustcorp.com.au>
rhelversion:    9.2""",
                "rhcsa_tips": ["Verify module parameters before passing options in /etc/modprobe.d/."],
                "default_run_cmd": "modinfo loop"
            },
            {
                "id": "ch16_modprobe",
                "name": "modprobe",
                "synopsis": "modprobe [options] [-v] modulename",
                "short_desc": "Add and remove modules from the Linux Kernel with automatic dependency resolution.",
                "detailed_desc": "The preferred tool to load or unload kernel drivers; resolves and loads prerequisite modules automatically.",
                "category": "Kernel Modules",
                "common_flags": [
                    {"flag": "-r, --remove", "desc": "Unload specified module and its unused dependencies."},
                    {"flag": "-v, --verbose", "desc": "Print messages about what the program is doing."}
                ],
                "sample_output": "insmod /lib/modules/5.14.0-284.el9.x86_64/kernel/fs/overlayfs/overlay.ko.xz",
                "rhcsa_tips": ["Always use 'modprobe' instead of 'insmod' because modprobe automatically resolves module dependencies!"],
                "default_run_cmd": "modprobe -c | head -n 10"
            },
            {
                "id": "ch16_sysctl",
                "name": "sysctl",
                "synopsis": "sysctl [options] [variable[=value]] ...",
                "short_desc": "Configure kernel parameters at runtime.",
                "detailed_desc": "Reads and modifies live kernel parameters exposed through /proc/sys/ (networking, memory, security, IPC).",
                "category": "Kernel Tuning",
                "common_flags": [
                    {"flag": "-a", "desc": "Display all currently active kernel parameters."},
                    {"flag": "-p [file]", "desc": "Load sysctl settings from specified file (default /etc/sysctl.conf)."},
                    {"flag": "-w variable=value", "desc": "Modify a single variable temporarily in runtime memory."}
                ],
                "sample_output": """net.ipv4.ip_forward = 1
vm.swappiness = 30
fs.file-max = 9223372036854775807""",
                "rhcsa_tips": [
                    "RHCSA EXAM FAVORITE: 'Enable IP packet forwarding permanently': add 'net.ipv4.ip_forward = 1' to /etc/sysctl.d/99-custom.conf, then load it with 'sysctl --system' or 'sysctl -p /etc/sysctl.d/99-custom.conf'!"
                ],
                "default_run_cmd": "sysctl net.ipv4.ip_forward"
            },
            {
                "id": "ch16_sysctl_system",
                "name": "sysctl --system",
                "synopsis": "sysctl --system",
                "short_desc": "Load settings from all system configuration files.",
                "detailed_desc": "Rereads all sysctl configuration files in order from /usr/lib/sysctl.d/, /etc/sysctl.d/, and /etc/sysctl.conf.",
                "category": "Kernel Tuning",
                "common_flags": [],
                "sample_output": """* Applying /usr/lib/sysctl.d/50-default.conf ...
* Applying /etc/sysctl.d/99-custom.conf ...
net.ipv4.ip_forward = 1""",
                "rhcsa_tips": ["Always run 'sysctl --system' after dropping a file in /etc/sysctl.d/ to verify it parses correctly."],
                "default_run_cmd": "sysctl -n net.ipv4.ip_forward"
            },
            {
                "id": "ch16_dracut",
                "name": "dracut",
                "synopsis": "dracut [OPTION...] [<image> [<kernel-version>]]",
                "short_desc": "Low-level tool for generating an initramfs boot image.",
                "detailed_desc": "Rebuilds the initial ramdisk (initramfs) that supplies drivers needed before the root filesystem is mounted.",
                "category": "Kernel Boot Images",
                "common_flags": [
                    {"flag": "-f, --force", "desc": "Overwrite existing initramfs image file."},
                    {"flag": "-v, --verbose", "desc": "Display verbose module inclusion messages."}
                ],
                "sample_output": """Executing: /usr/bin/dracut -f -v /boot/initramfs-5.14.0-284.11.1.el9_2.x86_64.img 5.14.0-284.11.1.el9_2.x86_64
*** Creating image file '/boot/initramfs-5.14.0-284.11.1.el9_2.x86_64.img' ***
*** Creating initramfs image file done ***""",
                "rhcsa_tips": ["If you add boot-critical drivers (like storage controller modules), rebuild initramfs with 'dracut -f'."],
                "default_run_cmd": "dracut --help | head -n 12"
            },
            {
                "id": "ch16_uname_r",
                "name": "uname -r",
                "synopsis": "uname -r",
                "short_desc": "Print the running kernel release version string.",
                "detailed_desc": "Outputs the exact kernel version number currently active in memory.",
                "category": "Kernel Info",
                "common_flags": [],
                "sample_output": "5.14.0-284.11.1.el9_2.x86_64",
                "rhcsa_tips": ["Matches the directory path under '/lib/modules/$(uname -r)/'."],
                "default_run_cmd": "uname -r"
            },
            {
                "id": "ch16_rmmod",
                "name": "rmmod",
                "synopsis": "rmmod [options] modulename ...",
                "short_desc": "Simple program to remove a module from the Linux Kernel.",
                "detailed_desc": "Directly unloads a kernel module without dependency checking.",
                "category": "Kernel Modules",
                "common_flags": [
                    {"flag": "-f, --force", "desc": "Force removal (dangerous if kernel not compiled with module unloading support)."}
                ],
                "sample_output": "Module removed.",
                "rhcsa_tips": ["modprobe -r is usually safer because it removes unused dependencies as well."],
                "default_run_cmd": "rmmod --help"
            },
            {
                "id": "ch16_insmod",
                "name": "insmod",
                "synopsis": "insmod [filename] [module options...]",
                "short_desc": "Simple program to insert a module into the Linux Kernel.",
                "detailed_desc": "Inserts a compiled .ko module file directly by disk filepath.",
                "category": "Kernel Modules",
                "common_flags": [],
                "sample_output": "Module inserted.",
                "rhcsa_tips": ["Low-level utility; prefer modprobe for regular operations."],
                "default_run_cmd": "insmod --help"
            },
            {
                "id": "ch16_cat_sys",
                "name": "cat /proc/sys/net/ipv4/ip_forward",
                "synopsis": "cat /proc/sys/net/ipv4/ip_forward",
                "short_desc": "Inspect kernel variables directly through the proc pseudo-filesystem.",
                "detailed_desc": "Every sysctl variable maps directly to a file under /proc/sys/ (e.g. net.ipv4.ip_forward -> /proc/sys/net/ipv4/ip_forward).",
                "category": "Kernel Tuning",
                "common_flags": [],
                "sample_output": "1",
                "rhcsa_tips": ["Values can be modified live: 'echo 1 > /proc/sys/net/ipv4/ip_forward' (runtime only, not persistent)."],
                "default_run_cmd": "cat /proc/sys/net/ipv4/ip_forward"
            }
        ]
    },

    # CHAPTER 17: Managing and Understanding the Boot Procedure
    {
        "chapter_id": 17,
        "part_id": 3,
        "part_title": "Part III: Performing Advanced System Administration Tasks",
        "chapter_title": "Managing and Understanding the Boot Procedure",
        "description": "GRUB 2 bootloader, boot targets, emergency and rescue modes, root password reset procedures, and power state controls.",
        "commands": [
            {
                "id": "ch17_grub2_mkconfig",
                "name": "grub2-mkconfig",
                "synopsis": "grub2-mkconfig [OPTION...] -o output_file",
                "short_desc": "Generate a GRUB configuration file from templates and /etc/default/grub.",
                "detailed_desc": "Reads scripts in /etc/grub.d/ and settings in /etc/default/grub to generate bootloader config files.",
                "category": "Bootloader Configuration",
                "common_flags": [
                    {"flag": "-o /boot/grub2/grub.cfg", "desc": "Write standard BIOS/UEFI boot menu configuration in RHEL 9."}
                ],
                "sample_output": """Generating grub configuration file ...
Adding boot menu entry for UEFI Firmware Settings ...
done""",
                "rhcsa_tips": [
                    "RHCSA NOTE: On RHEL 9, /boot/grub2/grub.cfg is the universal destination for both BIOS and UEFI systems (UEFI grub.cfg in ESP is now a stub)."
                ],
                "default_run_cmd": "grub2-mkconfig --help | head -n 12"
            },
            {
                "id": "ch17_grub2_editenv",
                "name": "grub2-editenv",
                "synopsis": "grub2-editenv [options] <filename> <command> ...",
                "short_desc": "Manage the GRUB environment block (default boot kernel).",
                "detailed_desc": "Sets and lists default kernel boot index and kernel command line arguments.",
                "category": "Bootloader Configuration",
                "common_flags": [
                    {"flag": "list", "desc": "Display all stored variables in the grubenv block."},
                    {"flag": "set saved_entry=<index>", "desc": "Set default boot kernel entry."}
                ],
                "sample_output": """saved_entry=17b2f69e4f5a4358a9e701982b61cd77-5.14.0-284.11.1.el9_2.x86_64
kernelopts=root=/dev/mapper/rhel-root ro crashkernel=1G-4G:192M,4G-64G:256M,64G-:512M resume=/dev/mapper/rhel-swap rhgb quiet""",
                "rhcsa_tips": ["'grubby' and 'grub2-editenv' allow safely modifying kernelopts without regenerating grub.cfg."],
                "default_run_cmd": "grub2-editenv list 2>/dev/null || echo 'saved_entry=kernel-default'"
            },
            {
                "id": "ch17_get_default",
                "name": "systemctl get-default",
                "synopsis": "systemctl get-default",
                "short_desc": "Query the default boot target configured for the system.",
                "detailed_desc": "Inspects /etc/systemd/system/default.target to report what mode the node boots into.",
                "category": "Boot Targets",
                "common_flags": [],
                "sample_output": "multi-user.target",
                "rhcsa_tips": ["Target should be 'multi-user.target' for headless servers, or 'graphical.target' for desktop environments."],
                "default_run_cmd": "systemctl get-default"
            },
            {
                "id": "ch17_set_default",
                "name": "systemctl set-default",
                "synopsis": "systemctl set-default TARGET.target",
                "short_desc": "Set the default system boot target.",
                "detailed_desc": "Permanently changes the boot target symlink for future restarts.",
                "category": "Boot Targets",
                "common_flags": [],
                "sample_output": "Created symlink /etc/systemd/system/default.target → /usr/lib/systemd/system/multi-user.target.",
                "rhcsa_tips": ["RHCSA EXAM TASK: 'Configure the server to boot to text mode by default': systemctl set-default multi-user.target."],
                "default_run_cmd": "systemctl get-default"
            },
            {
                "id": "ch17_emergency",
                "name": "systemctl emergency",
                "synopsis": "systemctl emergency",
                "short_desc": "Enter systemd emergency mode.",
                "detailed_desc": "Drops into the most minimal maintenance shell; root filesystem mounted read-only and no system services running.",
                "category": "System Maintenance",
                "common_flags": [],
                "sample_output": "Welcome to emergency mode! After logging in, type 'journalctl -xb' to view system logs.",
                "rhcsa_tips": ["Emergency mode is used when fstab errors prevent normal or rescue boot."],
                "default_run_cmd": "systemctl is-system-running"
            },
            {
                "id": "ch17_rescue",
                "name": "systemctl rescue",
                "synopsis": "systemctl rescue",
                "short_desc": "Enter systemd rescue mode (single-user mode).",
                "detailed_desc": "Mounts all local filesystems and starts basic services, providing an administrative maintenance shell.",
                "category": "System Maintenance",
                "common_flags": [],
                "sample_output": "Welcome to rescue mode! Type 'systemctl default' to enter default mode.",
                "rhcsa_tips": ["Rescue mode mounts filesystems, unlike emergency mode."],
                "default_run_cmd": "systemctl --help | grep rescue"
            },
            {
                "id": "ch17_reboot",
                "name": "reboot",
                "synopsis": "reboot [options]",
                "short_desc": "Reboot the operating system.",
                "detailed_desc": "Instructs systemd to cleanly terminate running processes, unmount filesystems, and restart the hardware.",
                "category": "System Power",
                "common_flags": [],
                "sample_output": "[System reboot initiated]",
                "rhcsa_tips": [
                    "RHCSA GOLDEN RULE: Always reboot your exam machine with 15 minutes left on the clock to verify that all your network, storage, and service configurations persist!"
                ],
                "default_run_cmd": "uptime"
            },
            {
                "id": "ch17_poweroff",
                "name": "poweroff",
                "synopsis": "poweroff [options]",
                "short_desc": "Halt and shut down the machine power.",
                "detailed_desc": "Cleanly unmounts storage filesystems and powers down the server hardware.",
                "category": "System Power",
                "common_flags": [],
                "sample_output": "[System powering down]",
                "rhcsa_tips": ["Use 'shutdown -h +15 \"Maintenance in 15 mins\"' to broadcast warnings to connected users."],
                "default_run_cmd": "shutdown --help"
            },
            {
                "id": "ch17_rd_break",
                "name": "rd.break (Kernel Boot Parameter)",
                "synopsis": "Append 'rd.break' to the linux line in GRUB menu",
                "short_desc": "Interrupt boot process inside initramfs to reset lost root password.",
                "detailed_desc": "Breaks boot before root is mounted. Workflow: mount -o remount,rw /sysroot -> chroot /sysroot -> passwd -> touch /.autorelabel -> exit -> exit.",
                "category": "Password Recovery",
                "common_flags": [],
                "sample_output": """switch_root:/# mount -o remount,rw /sysroot
switch_root:/# chroot /sysroot
sh-5.1# passwd root
sh-5.1# touch /.autorelabel
sh-5.1# exit
switch_root:/# exit""",
                "rhcsa_tips": [
                    "RHCSA MANDATORY ROOT PASSWORD RESET: 1) Press 'e' in GRUB menu. 2) Append 'rd.break' to linux line. 3) Press Ctrl+X. 4) mount -o remount,rw /sysroot. 5) chroot /sysroot. 6) echo 'password' | passwd --stdin root. 7) touch /.autorelabel (CRITICAL FOR SELINUX!). 8) exit twice!"
                ],
                "default_run_cmd": "cat /etc/issue"
            },
            {
                "id": "ch17_journalctl_b",
                "name": "journalctl -b",
                "synopsis": "journalctl -b [OFFSET]",
                "short_desc": "Show logs from the current or previous boot sessions.",
                "detailed_desc": "Isolates journal logs by boot ID; '-b -1' accesses the complete log from the previous boot to troubleshoot crashed restarts.",
                "category": "Boot Diagnostics",
                "common_flags": [
                    {"flag": "-b 0", "desc": "Logs from current boot session (default)."},
                    {"flag": "-b -1", "desc": "Logs from previous boot session."}
                ],
                "sample_output": """-- Boot 17b2f69e4f5a4358a9e701982b61cd77 --
Sep 24 10:00:00 rhel9-node1 kernel: Linux version 5.14.0-284.11.1.el9_2.x86_64
Sep 24 10:00:01 rhel9-node1 systemd[1]: Reached target Basic System.""",
                "rhcsa_tips": ["If a server rebooted unexpectedly, run 'journalctl -b -1 -p err' to find the crash cause."],
                "default_run_cmd": "journalctl -b -n 10 --no-pager"
            }
        ]
    },

    # CHAPTER 18: Essential Troubleshooting Skills
    {
        "chapter_id": 18,
        "part_id": 3,
        "part_title": "Part III: Performing Advanced System Administration Tasks",
        "chapter_title": "Essential Troubleshooting Skills",
        "description": "System diagnostics, tracing system calls, identifying open files and network sockets, hardware error auditing, and sosreports.",
        "commands": [
            {
                "id": "ch18_journalctl_err",
                "name": "journalctl -p err",
                "synopsis": "journalctl -p [0-3 | emerg..err] [-b]",
                "short_desc": "Filter systemd logs for error, critical, alert, and emergency messages only.",
                "detailed_desc": "Immediately eliminates routine debug/info logs to isolate failures and software crashes.",
                "category": "Diagnostics",
                "common_flags": [
                    {"flag": "-p err..emerg", "desc": "Show priority level 3 (error) down to 0 (emerg)."}
                ],
                "sample_output": """Sep 24 16:30:11 rhel9-node1 httpd[1240]: AH00072: make_sock: could not bind to address 0.0.0.0:80
Sep 24 16:30:11 rhel9-node1 httpd[1240]: no listening sockets available, shutting down
Sep 24 16:30:11 rhel9-node1 systemd[1]: httpd.service: Main process exited, code=exited, status=1/FAILURE""",
                "rhcsa_tips": ["First command to run when something is broken on an RHCSA troubleshooting question."],
                "default_run_cmd": "journalctl -p err -n 10 --no-pager"
            },
            {
                "id": "ch18_lsof",
                "name": "lsof",
                "synopsis": "lsof [options] [path]",
                "short_desc": "List open files and processes holding file locks.",
                "detailed_desc": "Finds which processes have files, directories, libraries, or network sockets held open.",
                "category": "Diagnostics",
                "common_flags": [
                    {"flag": "-i :<port>", "desc": "Find process listening or connecting on a port (e.g. lsof -i :80)."},
                    {"flag": "+D <dir>", "desc": "Find all processes with open files in a directory tree."}
                ],
                "sample_output": """COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
nginx   2100 root    6u  IPv4  32014      0t0  TCP *:http (LISTEN)""",
                "rhcsa_tips": ["If 'umount /mnt' fails with 'device is busy', run 'lsof +D /mnt' to find the culprit process."],
                "default_run_cmd": "lsof -i :22 2>/dev/null || lsof -iTCP -sTCP:LISTEN -P -n"
            },
            {
                "id": "ch18_strace",
                "name": "strace",
                "synopsis": "strace [options] [-e expr] [command [arg ...]]",
                "short_desc": "Trace system calls and signals executed by a binary.",
                "detailed_desc": "Monitors interactions between a userspace process and the Linux kernel (openat, read, write, connect).",
                "category": "Low-level Diagnostics",
                "common_flags": [
                    {"flag": "-p <PID>", "desc": "Attach to an already running process ID."},
                    {"flag": "-e trace=open,openat", "desc": "Trace only file opening calls to locate missing configs."}
                ],
                "sample_output": """openat(AT_FDCWD, "/etc/app.conf", O_RDONLY) = -1 ENOENT (No such file or directory)
write(2, "Error: config file missing\\n", 28) = 28""",
                "rhcsa_tips": ["Find why a daemon silently fails on launch: 'strace -e openat <binary>'."],
                "default_run_cmd": "strace -V"
            },
            {
                "id": "ch18_vmstat",
                "name": "vmstat",
                "synopsis": "vmstat [options] [delay [count]]",
                "short_desc": "Report virtual memory statistics, CPU activity, and I/O wait.",
                "detailed_desc": "Provides concise real-time sampling of processes (r/b), swap in/out (si/so), blocks in/out (bi/bo), and CPU states.",
                "category": "System Metrics",
                "common_flags": [
                    {"flag": "1 5", "desc": "Sample 5 times with 1-second interval."}
                ],
                "sample_output": """procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 1  0      0 144400  12400 1465200    0    0     4    25   42   78  1  1 98  0  0""",
                "rhcsa_tips": ["High 'wa' (I/O wait) indicates a slow or saturated disk storage subsystem."],
                "default_run_cmd": "vmstat 1 3"
            },
            {
                "id": "ch18_iostat",
                "name": "iostat",
                "synopsis": "iostat [options] [interval [count]]",
                "short_desc": "Report CPU and input/output statistics for block devices and partitions.",
                "detailed_desc": "Part of sysstat package; monitors storage disk throughput (r/s, w/s, rkB/s, wkB/s, %util).",
                "category": "Storage Metrics",
                "common_flags": [
                    {"flag": "-x", "desc": "Display extended statistics (%util, await)."},
                    {"flag": "-h", "desc": "Human-readable units."}
                ],
                "sample_output": """Device            r/s     w/s     rkB/s     wkB/s   await  %util
vda              0.25    4.12      8.20     48.50    1.20   0.45
vdb              0.00    0.00      0.00      0.00    0.00   0.00""",
                "rhcsa_tips": ["A '%util' close to 100% means the disk device is completely saturated."],
                "default_run_cmd": "iostat 2>/dev/null || vmstat"
            },
            {
                "id": "ch18_tcpdump",
                "name": "tcpdump",
                "synopsis": "tcpdump [options] [filter-expression]",
                "short_desc": "Dump and capture network traffic packets on an interface.",
                "detailed_desc": "Captures raw packet headers and payloads matching custom filter rules (host, port, protocol).",
                "category": "Network Diagnostics",
                "common_flags": [
                    {"flag": "-i <iface>", "desc": "Listen on specified network interface."},
                    {"flag": "-n", "desc": "Do not resolve host addresses to names."},
                    {"flag": "-c <N>", "desc": "Exit after capturing N packets."}
                ],
                "sample_output": """18:10:02.124567 IP 192.168.1.100.52310 > 192.168.1.50.22: Flags [P.], seq 1:40, ack 1
18:10:02.124890 IP 192.168.1.50.22 > 192.168.1.100.52310: Flags [.], ack 40""",
                "rhcsa_tips": ["'tcpdump -i any port 80 -nn' verifies whether HTTP requests are arriving at the network interface."],
                "default_run_cmd": "tcpdump --version"
            },
            {
                "id": "ch18_sosreport",
                "name": "sosreport",
                "synopsis": "sos report [options]",
                "short_desc": "Generate diagnostic configuration and log tarball for support analysis.",
                "detailed_desc": "Collects comprehensive system configuration, logs, hardware info, and package inventory into an encrypted/compressed tarball.",
                "category": "Diagnostic Reporting",
                "common_flags": [
                    {"flag": "--batch", "desc": "Run non-interactively using default parameters without prompting for case number."}
                ],
                "sample_output": """sosreport (version 4.5.1)
This command will collect system configuration and diagnostic
information from this Red Hat Enterprise Linux system.
Creating archive: /var/tmp/sosreport-rhel9-node1-2026-09-24.tar.xz""",
                "rhcsa_tips": ["Red Hat enterprise standard for opening support cases."],
                "default_run_cmd": "sos --version 2>/dev/null || echo 'sos report utility'"
            },
            {
                "id": "ch18_dmesg_err",
                "name": "dmesg --level=err,crit",
                "synopsis": "dmesg --level=err,crit",
                "short_desc": "Filter kernel hardware buffer for critical errors only.",
                "detailed_desc": "Displays hardware fault messages, memory failures, disk read errors, or kernel panics.",
                "category": "Diagnostics",
                "common_flags": [],
                "sample_output": "[Wed Sep 24 10:00:02 2026] ACPI Error: AE_NOT_FOUND, During name lookup/catalog",
                "rhcsa_tips": ["Check dmesg errors whenever a disk drive drops offline."],
                "default_run_cmd": "dmesg --level=err 2>/dev/null || dmesg | head -n 10"
            },
            {
                "id": "ch18_systemctl_failed",
                "name": "systemctl --failed",
                "synopsis": "systemctl --failed [options]",
                "short_desc": "List all failed systemd units on the host.",
                "detailed_desc": "Shows services that terminated with exit errors during startup or runtime.",
                "category": "Service Diagnostics",
                "common_flags": [],
                "sample_output": """  UNIT          LOAD   ACTIVE SUB    DESCRIPTION
0 loaded units listed.""",
                "rhcsa_tips": ["A clean system should show '0 loaded units listed'. Run this before submitting your RHCSA exam!"],
                "default_run_cmd": "systemctl --failed"
            },
            {
                "id": "ch18_which_broken",
                "name": "ldd",
                "synopsis": "ldd [option]... file...",
                "short_desc": "Print shared library dependencies of an executable binary.",
                "detailed_desc": "Displays all dynamic shared libraries (.so) required by a binary and checks for missing dependencies.",
                "category": "Binary Diagnostics",
                "common_flags": [],
                "sample_output": """	linux-vdso.so.1 (0x00007ffd395f8000)
	libselinux.so.1 => /lib64/libselinux.so.1 (0x00007f59a84f0000)
	libc.so.6 => /lib64/libc.so.6 (0x00007f59a82e0000)
	/lib64/ld-linux-x86-64.so.2 (0x00007f59a8550000)""",
                "rhcsa_tips": ["If a command gives 'cannot open shared object file: No such file or directory', ldd identifies the missing library."],
                "default_run_cmd": "ldd /bin/ls"
            }
        ]
    },

    # CHAPTER 19: An Introduction to Automation with Bash Shell Scripting
    {
        "chapter_id": 19,
        "part_id": 3,
        "part_title": "Part III: Performing Advanced System Administration Tasks",
        "chapter_title": "An Introduction to Automation with Bash Shell Scripting",
        "description": "Script structure (shebang #!/bin/bash), variables, positional parameters ($1, $2), conditional expressions ([ -f file ]), loops (for, while), and exit statuses ($?).",
        "commands": [
            {
                "id": "ch19_bash",
                "name": "bash",
                "synopsis": "bash [options] [script-file [arguments...]]",
                "short_desc": "GNU Bourne-Again SHell script interpreter.",
                "detailed_desc": "Executes shell script files with debugging options (-x for execution tracing, -n for syntax check).",
                "category": "Shell Interpreter",
                "common_flags": [
                    {"flag": "-x", "desc": "Print commands and their arguments as they are executed (essential for debugging!)."},
                    {"flag": "-n", "desc": "Read commands without executing them (checks syntax errors)."}
                ],
                "sample_output": """+ TARGET=/var/backup
+ mkdir -p /var/backup
+ cp -a /etc/hosts /var/backup/""",
                "rhcsa_tips": ["Always debug failing bash scripts with 'bash -x script.sh'!"],
                "default_run_cmd": "bash --version"
            },
            {
                "id": "ch19_chmod_x",
                "name": "chmod +x",
                "synopsis": "chmod +x <script.sh>",
                "short_desc": "Mark a script as executable.",
                "detailed_desc": "Grants execute permissions (x) so the script can be launched directly with './script.sh'.",
                "category": "Permissions",
                "common_flags": [],
                "sample_output": "-rwxr-xr-x. 1 root root 420 Sep 24 18:15 backup.sh",
                "rhcsa_tips": ["Remember: Scripts must have '#!/bin/bash' on line 1 and execute permission ('chmod +x') to run directly."],
                "default_run_cmd": "echo '#!/bin/bash' > /tmp/demo.sh && chmod +x /tmp/demo.sh && ls -l /tmp/demo.sh"
            },
            {
                "id": "ch19_read",
                "name": "read",
                "synopsis": "read [-ers] [-p prompt] [-t timeout] [name ...]",
                "short_desc": "Read a line from standard input into shell variables.",
                "detailed_desc": "Prompts users for input or reads lines in automated while loops.",
                "category": "Shell Builtin",
                "common_flags": [
                    {"flag": "-p \"prompt\"", "desc": "Output prompt string before reading input."},
                    {"flag": "-s", "desc": "Silent mode: do not echo input (used for passwords)."},
                    {"flag": "-r", "desc": "Raw mode: do not treat backslashes as escape characters."}
                ],
                "sample_output": "Enter username: admin\nRead input: admin",
                "rhcsa_tips": ["Looping over lines in a file: 'while IFS= read -r line; do echo \"$line\"; done < /path/file'."],
                "default_run_cmd": "help read | head -n 12"
            },
            {
                "id": "ch19_test",
                "name": "test / [ ]",
                "synopsis": "test EXPRESSION or [ EXPRESSION ]",
                "short_desc": "Evaluate conditional expressions in bash scripts.",
                "detailed_desc": "Tests file types (-f, -d, -e, -s), permissions (-r, -w, -x), string equality, and numeric comparisons (-eq, -ne, -lt, -gt).",
                "category": "Conditionals",
                "common_flags": [
                    {"flag": "-f <file>", "desc": "True if file exists and is a regular file."},
                    {"flag": "-d <dir>", "desc": "True if path exists and is a directory."},
                    {"flag": "-z <str>", "desc": "True if string length is zero (empty string)."},
                    {"flag": "$? -eq 0", "desc": "Test if previous command exited with success (0)."}
                ],
                "sample_output": "File exists: YES (exit status 0)",
                "rhcsa_tips": [
                    "Always leave spaces around brackets: '[ -f /etc/hosts ]' (not '[-f /etc/hosts]')."
                ],
                "default_run_cmd": "[ -f /etc/hosts ] && echo 'File /etc/hosts exists!'"
            },
            {
                "id": "ch19_for_loop",
                "name": "for loop",
                "synopsis": "for item in list; do ... done",
                "short_desc": "Iterate over a sequence of items or files in bash.",
                "detailed_desc": "Automates repetitive tasks over user lists, IP addresses, or file patterns.",
                "category": "Control Flow",
                "common_flags": [],
                "sample_output": """Creating user user1...
Creating user user2...
Creating user user3...""",
                "rhcsa_tips": [
                    "RHCSA BASH OBJECTIVE: 'Write a script that creates users user1, user2, user3': for u in user1 user2 user3; do useradd $u; done."
                ],
                "default_run_cmd": "for i in 1 2 3; do echo \"Node $i\"; done"
            },
            {
                "id": "ch19_while_loop",
                "name": "while loop",
                "synopsis": "while condition; do ... done",
                "short_desc": "Execute commands repeatedly as long as condition evaluates to true.",
                "detailed_desc": "Great for polling service status or reading streams line by line until EOF.",
                "category": "Control Flow",
                "common_flags": [],
                "sample_output": """Count: 1
Count: 2
Count: 3""",
                "rhcsa_tips": ["'while ! ping -c 1 node2; do sleep 2; done' waits until a remote machine is online."],
                "default_run_cmd": "x=1; while [ $x -le 3 ]; do echo \"Item $x\"; x=$((x+1)); done"
            },
            {
                "id": "ch19_case",
                "name": "case statement",
                "synopsis": "case word in pattern ) ... ;; esac",
                "short_desc": "Multi-branch condition matching in bash scripts.",
                "detailed_desc": "Clean replacement for complex nested if-elif-else chains, especially for command-line flags ($1).",
                "category": "Control Flow",
                "common_flags": [],
                "sample_output": "Action: Start service",
                "rhcsa_tips": ["Ideal for init-style scripts taking start|stop|restart arguments."],
                "default_run_cmd": "ACTION='start'; case $ACTION in start) echo 'Starting service...';; *) echo 'Unknown';; esac"
            },
            {
                "id": "ch19_export",
                "name": "export",
                "synopsis": "export [-fn] [name[=word]] ...",
                "short_desc": "Export variables to child processes.",
                "detailed_desc": "Marks shell variables so they are automatically inherited by subshells and executed binaries.",
                "category": "Environment",
                "common_flags": [
                    {"flag": "-p", "desc": "Print list of all exported variables."}
                ],
                "sample_output": "export APP_ENV=\"production\"",
                "rhcsa_tips": ["Without 'export', a variable is only visible in the current shell and NOT inside scripts invoked by it!"],
                "default_run_cmd": "export TEST_VAR='RHCSA_Ready' && echo $TEST_VAR"
            },
            {
                "id": "ch19_env",
                "name": "env",
                "synopsis": "env [OPTION]... [-] [NAME=VALUE]... [COMMAND [ARG]...]",
                "short_desc": "Run a program in a modified environment or print environment variables.",
                "detailed_desc": "Displays active environment (PATH, HOME, USER, SHELL) or runs commands with specific temporary variables.",
                "category": "Environment",
                "common_flags": [
                    {"flag": "-i, --ignore-environment", "desc": "Start with an empty environment."}
                ],
                "sample_output": """USER=root
HOME=/root
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin""",
                "rhcsa_tips": ["Use 'env' to verify environment variables inside cron executions."],
                "default_run_cmd": "env | grep -E 'USER|SHELL|HOME'"
            },
            {
                "id": "ch19_exit_status",
                "name": "echo $?",
                "synopsis": "echo $?",
                "short_desc": "Print the exit status of the most recently executed foreground pipeline.",
                "detailed_desc": "0 indicates success; any non-zero value (1 to 255) represents an error.",
                "category": "Script Automation",
                "common_flags": [],
                "sample_output": "0",
                "rhcsa_tips": [
                    "RHCSA GOLDEN CHECK: Run a command, then immediately execute 'echo $?'. If it prints 0, the task succeeded!"
                ],
                "default_run_cmd": "ls /etc/hosts >/dev/null && echo $?"
            }
        ]
    }
]
