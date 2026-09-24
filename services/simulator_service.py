"""
Virtual Shell Simulation Engine
Simulates realistic RHEL 9 terminal command execution, stateful virtual filesystem navigation,
and command-matching against the RHCSA 9 catalog.
"""

import re
import shlex
import time
from data.commands_data import CHAPTERS, _COMMAND_INDEX

# Default Mock Virtual Filesystem structure
DEFAULT_VFS = {
    "/": ["bin", "boot", "dev", "etc", "home", "lib64", "mnt", "opt", "proc", "root", "run", "sbin", "sys", "tmp", "usr", "var"],
    "/root": ["anaconda-ks.cfg", "initial-setup-ks.cfg", "rhcsa-lab"],
    "/root/.ssh": ["id_rsa", "id_rsa.pub", "authorized_keys", "known_hosts"],
    "/home": ["student"],
    "/home/student": ["Desktop", "Documents", "Downloads", "lab-workspace", "Containerfile"],
    "/home/student/.ssh": ["authorized_keys"],
    "/etc": ["hosts", "passwd", "shadow", "group", "fstab", "hostname", "locale.conf", "resolv.conf", "os-release", "systemd", "chrony.conf", "sudoers"],
    "/etc/systemd/system": ["default.target", "multi-user.target.wants"],
    "/var/log": ["messages", "secure", "audit", "journal", "httpd", "cron", "dmesg"],
    "/var/log/httpd": ["access_log", "error_log"],
    "/var/www/html": ["index.html"],
    "/mnt": ["nfs", "storage"]
}

# Pre-populated virtual file contents
VIRTUAL_FILES = {
    "/etc/hosts": """127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
192.168.1.50 rhel9-node1.example.com node1
192.168.1.60 rhel9-node2.example.com node2""",

    "/etc/os-release": """NAME="Red Hat Enterprise Linux"
VERSION="9.2 (Plow)"
ID="rhel"
ID_LIKE="fedora"
VERSION_ID="9.2"
PLATFORM_ID="platform:el9"
PRETTY_NAME="Red Hat Enterprise Linux 9.2 (Plow)"
ANSI_COLOR="0;31"
CPE_NAME="cpe:/o:redhat:enterprise_linux:9::baseos"
HOME_URL="https://www.redhat.com/" """,

    "/etc/hostname": "rhel9-node1.example.com",

    "/etc/fstab": """#
# /etc/fstab
# Created by anaconda on Wed Sep 20 10:15:20 2026
#
/dev/mapper/rhel-root               /                       xfs     defaults        0 0
UUID=7a8b9c0d-1234-5678-9abc-def012345678 /boot                   xfs     defaults        0 0
/dev/mapper/rhel-swap               none                    swap    defaults        0 0
UUID=3d4e5f6a-7b8c-9d0e-1f2a-3b4c5d6e7f8a /data                   xfs     defaults        0 0""",

    "/etc/passwd": """root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
adm:x:3:4:adm:/var/adm:/sbin/nologin
lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
student:x:1000:1000:Student User:/home/student:/bin/bash
natasha:x:2005:2005::/home/natasha:/bin/bash
sarah:x:2006:2006::/home/sarah:/bin/bash
apache:x:48:48:Apache:/usr/share/httpd:/sbin/nologin
sshd:x:74:74:Privilege-separated SSH:/usr/share/empty.sshd:/sbin/nologin
chrony:x:998:996:Chronyd user:/var/lib/chrony:/sbin/nologin""",

    "/var/www/html/index.html": """<!DOCTYPE html>
<html>
<head><title>RHEL 9 Web Server</title></head>
<body>
<h1>Red Hat Enterprise Linux 9 - Apache HTTP Server</h1>
<p>Test page configured for RHCSA Exercise.</p>
</body>
</html>""",

    "/etc/chrony.conf": """# Use public servers from pool.ntp.org
server time.example.com iburst
driftfile /var/lib/chrony/drift
makestep 1.0 3
rtcsync
logdir /var/log/chrony"""
}

class TerminalSession:
    """Represents a virtual shell state for a user session."""
    def __init__(self, username="root", hostname="rhel9-node1"):
        self.username = username
        self.hostname = hostname
        self.cwd = "/root" if username == "root" else f"/home/{username}"
        self.history = []
        self.env = {
            "USER": username,
            "HOME": self.cwd,
            "SHELL": "/bin/bash",
            "TERM": "xterm-256color",
            "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin"
        }
        self.custom_files = {}

    def get_prompt(self):
        symbol = "#" if self.username == "root" else "$"
        display_cwd = "~" if self.cwd == self.env["HOME"] else self.cwd
        return f"[{self.username}@{self.hostname} {display_cwd}]{symbol}"


class VirtualShell:
    """Executes commands and maps them to catalog examples or virtual responses."""

    def __init__(self):
        self.session = TerminalSession()
        self._build_command_map()

    def _build_command_map(self):
        """Map common command keywords and invocation prefixes to catalog outputs."""
        self.exact_map = {}
        self.prefix_map = {}

        for ch in CHAPTERS:
            for c in ch["commands"]:
                # Map default run command
                def_cmd = c.get("default_run_cmd", "").strip()
                if def_cmd:
                    self.exact_map[def_cmd] = (c["sample_output"], 0)

                # Map command name itself
                name = c["name"].strip()
                self.exact_map[name] = (c["sample_output"], 0)

                # Prefix matching
                base_token = name.split()[0]
                if base_token not in self.prefix_map:
                    self.prefix_map[base_token] = []
                self.prefix_map[base_token].append(c)

    def execute(self, raw_input):
        """Execute or simulate a raw command string."""
        raw_cmd = raw_input.strip()
        if not raw_cmd:
            return {
                "stdout": "",
                "stderr": "",
                "exit_code": 0,
                "cwd": self.session.cwd,
                "prompt": self.session.get_prompt()
            }

        self.session.history.append(raw_cmd)
        start_time = time.time()

        # Handle built-in filesystem / navigation commands
        result = self._handle_builtin(raw_cmd)
        if result is not None:
            exec_time = round(time.time() - start_time, 3)
            result["execution_time"] = f"{exec_time}s"
            result["prompt"] = self.session.get_prompt()
            return result

        # Check exact catalog match
        if raw_cmd in self.exact_map:
            out, code = self.exact_map[raw_cmd]
            return self._format_result(out, "", code, start_time)

        # Check if user typed command with typical arguments
        tokens = raw_cmd.split()
        binary = tokens[0]

        # Check catalog prefix matching
        if binary in self.prefix_map:
            for c in self.prefix_map[binary]:
                # If command matches name or default run
                if raw_cmd.startswith(c["name"]) or c.get("default_run_cmd", "").startswith(raw_cmd):
                    return self._format_result(c["sample_output"], "", 0, start_time)
            # Default to first sample output of that binary
            sample = self.prefix_map[binary][0]["sample_output"]
            return self._format_result(sample, "", 0, start_time)

        # Handle unknown commands
        stderr = f"bash: {binary}: command not found..."
        return self._format_result("", stderr, 127, start_time)

    def _handle_builtin(self, raw_cmd):
        """Process local built-in commands like cd, pwd, ls, cat, echo, clear, history."""
        tokens = raw_cmd.split()
        cmd = tokens[0]

        if cmd == "clear":
            return {"stdout": "\033[2J\033[H", "stderr": "", "exit_code": 0, "clear": True, "cwd": self.session.cwd}

        if cmd == "pwd":
            return {"stdout": self.session.cwd, "stderr": "", "exit_code": 0, "cwd": self.session.cwd}

        if cmd == "history":
            lines = [f"  {idx+1}  {c}" for idx, c in enumerate(self.session.history[-30:])]
            return {"stdout": "\n".join(lines), "stderr": "", "exit_code": 0, "cwd": self.session.cwd}

        if cmd == "cd":
            target = tokens[1] if len(tokens) > 1 else self.session.env["HOME"]
            if target == "~":
                self.session.cwd = self.session.env["HOME"]
            elif target == "..":
                if self.session.cwd != "/":
                    parts = self.session.cwd.rstrip("/").split("/")
                    self.session.cwd = "/".join(parts[:-1]) or "/"
            elif target.startswith("/"):
                # Simulated path
                self.session.cwd = target.rstrip("/") or "/"
            else:
                new_path = (self.session.cwd.rstrip("/") + "/" + target).rstrip("/")
                self.session.cwd = new_path
            return {"stdout": "", "stderr": "", "exit_code": 0, "cwd": self.session.cwd}

        if cmd == "ls":
            curr = self.session.cwd
            items = DEFAULT_VFS.get(curr, ["file1.txt", "notes.log", "config.yml"])
            if "-l" in raw_cmd or "-lah" in raw_cmd:
                formatted = [f"total {len(items)*4}"]
                for item in items:
                    is_dir = "." not in item
                    mode = "drwxr-xr-x. 2" if is_dir else "-rw-r--r--. 1"
                    size = "4096" if is_dir else "1024"
                    formatted.append(f"{mode} root root {size:>6} Sep 24 18:00 {item}")
                return {"stdout": "\n".join(formatted), "stderr": "", "exit_code": 0, "cwd": self.session.cwd}
            return {"stdout": "  ".join(items), "stderr": "", "exit_code": 0, "cwd": self.session.cwd}

        if cmd == "cat":
            if len(tokens) < 2:
                return {"stdout": "", "stderr": "cat: missing file operand", "exit_code": 1, "cwd": self.session.cwd}
            filepath = tokens[1]
            # Resolve relative
            if not filepath.startswith("/"):
                filepath = (self.session.cwd.rstrip("/") + "/" + filepath)

            if filepath in VIRTUAL_FILES:
                return {"stdout": VIRTUAL_FILES[filepath], "stderr": "", "exit_code": 0, "cwd": self.session.cwd}
            elif filepath in self.session.custom_files:
                return {"stdout": self.session.custom_files[filepath], "stderr": "", "exit_code": 0, "cwd": self.session.cwd}
            else:
                return {"stdout": "", "stderr": f"cat: {filepath}: No such file or directory", "exit_code": 1, "cwd": self.session.cwd}

        if cmd == "echo":
            content = " ".join(tokens[1:])
            # Handle redirection
            if ">" in content:
                parts = content.split(">")
                text = parts[0].strip().strip("\"'")
                dest = parts[1].strip()
                if not dest.startswith("/"):
                    dest = (self.session.cwd.rstrip("/") + "/" + dest)
                self.session.custom_files[dest] = text
                return {"stdout": "", "stderr": "", "exit_code": 0, "cwd": self.session.cwd}
            # Variable substitution
            if content.startswith("$"):
                var_name = content[1:]
                return {"stdout": self.session.env.get(var_name, ""), "stderr": "", "exit_code": 0, "cwd": self.session.cwd}
            return {"stdout": content.strip("\"'"), "stderr": "", "exit_code": 0, "cwd": self.session.cwd}

        if cmd == "whoami":
            return {"stdout": self.session.username, "stderr": "", "exit_code": 0, "cwd": self.session.cwd}

        if cmd == "hostname":
            return {"stdout": self.session.hostname, "stderr": "", "exit_code": 0, "cwd": self.session.cwd}

        return None

    def _format_result(self, stdout, stderr, code, start_time):
        exec_time = round(time.time() - start_time, 3)
        return {
            "stdout": stdout,
            "stderr": stderr,
            "exit_code": code,
            "execution_time": f"{exec_time}s",
            "cwd": self.session.cwd,
            "prompt": self.session.get_prompt()
        }

# Global singleton simulator engine for session
simulator_engine = VirtualShell()
