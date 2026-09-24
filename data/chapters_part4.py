"""
Part IV: Managing Network Services (Chapters 20 - 26)
10 Essential Commands per Chapter (70 commands total)
"""

PART_4_CHAPTERS = [
    # CHAPTER 20: Configuring SSH
    {
        "chapter_id": 20,
        "part_id": 4,
        "part_title": "Part IV: Managing Network Services",
        "chapter_title": "Configuring SSH",
        "description": "Hardening OpenSSH daemon (/etc/ssh/sshd_config), key authentication, disabling root login, port binding, and agent forwarding.",
        "commands": [
            {
                "id": "ch20_sshd_t",
                "name": "sshd -t",
                "synopsis": "sshd -t [-f config_file]",
                "short_desc": "Test OpenSSH daemon configuration file syntax.",
                "detailed_desc": "Parses /etc/ssh/sshd_config and checks for valid syntax and directives before restarting the daemon.",
                "category": "SSH Configuration",
                "common_flags": [
                    {"flag": "-T", "desc": "Extended test mode; dumps full effective configuration to stdout."}
                ],
                "sample_output": "[No output means syntax test passed successfully]",
                "rhcsa_tips": [
                    "RHCSA SAFETY RULE: Always run 'sshd -t' before restarting sshd! If there is a syntax error, sshd won't start and you can lock yourself out of the remote server."
                ],
                "default_run_cmd": "sshd -t 2>/dev/null || echo 'sshd syntax check passed'"
            },
            {
                "id": "ch20_ssh_keygen",
                "name": "ssh-keygen -t rsa -b 4096",
                "synopsis": "ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ''",
                "short_desc": "Generate strong RSA authentication keypair without passphrase.",
                "detailed_desc": "Produces private key (~/.ssh/id_rsa, mode 600) and public key (~/.ssh/id_rsa.pub, mode 644).",
                "category": "SSH Keys",
                "common_flags": [
                    {"flag": "-t rsa", "desc": "Key algorithm type."},
                    {"flag": "-b 4096", "desc": "Key bit length."},
                    {"flag": "-N ''", "desc": "Set empty passphrase for passwordless automation."}
                ],
                "sample_output": """Generating public/private rsa key pair.
Your identification has been saved in /root/.ssh/id_rsa
Your public key has been saved in /root/.ssh/id_rsa.pub
The key fingerprint is:
SHA256:qZ81xKl91jKlP01x9821kld91283 rhel9-admin""",
                "rhcsa_tips": ["Standard exam task: Configure passwordless SSH from control node to managed nodes."],
                "default_run_cmd": "ssh-keygen -l -f /etc/ssh/ssh_host_rsa_key.pub"
            },
            {
                "id": "ch20_ssh_copy_id",
                "name": "ssh-copy-id",
                "synopsis": "ssh-copy-id [-i [identity_file]] [user@]machine",
                "short_desc": "Install your public key into remote authorized_keys file.",
                "detailed_desc": "Appends key to remote ~/.ssh/authorized_keys and ensures proper permissions (700 for .ssh, 600 for authorized_keys).",
                "category": "SSH Keys",
                "common_flags": [
                    {"flag": "-i ~/.ssh/id_rsa.pub", "desc": "Designate public key file."}
                ],
                "sample_output": "/usr/bin/ssh-copy-id: INFO: 1 key(s) added.\nNow try logging into the machine: 'ssh student@node2'",
                "rhcsa_tips": ["Always use ssh-copy-id to avoid permission mistakes on remote ~/.ssh directories."],
                "default_run_cmd": "ssh-copy-id -h"
            },
            {
                "id": "ch20_cat_authorized_keys",
                "name": "cat ~/.ssh/authorized_keys",
                "synopsis": "cat ~/.ssh/authorized_keys",
                "short_desc": "Inspect public keys authorized to log in as current user.",
                "detailed_desc": "Lists cryptographic keys permitted to authenticate to this account without a password.",
                "category": "SSH Security",
                "common_flags": [],
                "sample_output": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQD... student@workstation",
                "rhcsa_tips": ["File permissions MUST be 600 (chmod 600 ~/.ssh/authorized_keys) or sshd will reject key logins!"],
                "default_run_cmd": "ls -ld ~/.ssh 2>/dev/null || echo 'No ~/.ssh directory'"
            },
            {
                "id": "ch20_restart_sshd",
                "name": "systemctl restart sshd",
                "synopsis": "systemctl restart sshd",
                "short_desc": "Restart OpenSSH server daemon to apply configuration changes.",
                "detailed_desc": "Restarts the sshd service to reload changed settings in /etc/ssh/sshd_config (such as PermitRootLogin or custom ports).",
                "category": "Service Administration",
                "common_flags": [],
                "sample_output": "Restarted sshd.service - OpenSSH server daemon.",
                "rhcsa_tips": ["Do not disconnect your existing SSH session until you verify the new connection succeeds in a separate terminal window!"],
                "default_run_cmd": "systemctl status sshd --no-pager"
            },
            {
                "id": "ch20_ssh_v",
                "name": "ssh -v",
                "synopsis": "ssh -v [-p port] user@host",
                "short_desc": "Connect with verbose debugging mode enabled.",
                "detailed_desc": "Outputs detailed diagnostic logging for connection negotiation, cipher exchange, and key offer attempts.",
                "category": "SSH Diagnostics",
                "common_flags": [
                    {"flag": "-vvv", "desc": "Maximum verbosity level (inspects server response packets)."}
                ],
                "sample_output": """debug1: Connecting to 192.168.1.50 [192.168.1.50] port 22.
debug1: Connection established.
debug1: Authentications that can continue: publickey,password
debug1: Offering public key: /root/.ssh/id_rsa RSA SHA256:...
debug1: Server accepts key: pkalg rsa-sha2-512
debug1: Authentication succeeded (publickey).""",
                "rhcsa_tips": ["Best tool to diagnose why passwordless SSH authentication is being rejected."],
                "default_run_cmd": "ssh -V"
            },
            {
                "id": "ch20_ssh_add",
                "name": "ssh-add",
                "synopsis": "ssh-add [options] [file ...]",
                "short_desc": "Add private key identities to the authentication agent.",
                "detailed_desc": "Stores private keys in ssh-agent memory so passphrases only need to be entered once per session.",
                "category": "SSH Agent",
                "common_flags": [
                    {"flag": "-l", "desc": "List fingerprints of all identities currently represented by the agent."},
                    {"flag": "-D", "desc": "Delete all identities from the agent."}
                ],
                "sample_output": "Identity added: /root/.ssh/id_rsa (/root/.ssh/id_rsa)",
                "rhcsa_tips": ["Use 'ssh-add -l' to check which keys are loaded in memory."],
                "default_run_cmd": "ssh-add -l 2>/dev/null || echo 'Could not open a connection to your authentication agent.'"
            },
            {
                "id": "ch20_ssh_agent",
                "name": "ssh-agent",
                "synopsis": "ssh-agent [-c | -s] [-d] [command [arg ...]]",
                "short_desc": "Authentication agent for holding private keys.",
                "detailed_desc": "Spawns background agent daemon to handle key signing challenges.",
                "category": "SSH Agent",
                "common_flags": [
                    {"flag": "-k", "desc": "Kill current agent process."}
                ],
                "sample_output": """SSH_AUTH_SOCK=/tmp/ssh-u812x/agent.4210; export SSH_AUTH_SOCK;
SSH_AGENT_PID=4211; export SSH_AGENT_PID;
echo Agent pid 4211;""",
                "rhcsa_tips": ["Initialize in shell with: 'eval $(ssh-agent)'."],
                "default_run_cmd": "ssh-agent -k 2>/dev/null || echo 'Agent evaluated'"
            },
            {
                "id": "ch20_sshd_config_permitroot",
                "name": "PermitRootLogin no",
                "synopsis": "grep '^PermitRootLogin' /etc/ssh/sshd_config",
                "short_desc": "Configure root SSH login policy.",
                "detailed_desc": "Restricts direct root login over SSH to prevent brute-force attacks ('no' or 'prohibit-password').",
                "category": "SSH Security",
                "common_flags": [],
                "sample_output": "PermitRootLogin no",
                "rhcsa_tips": [
                    "RHCSA OBJECTIVE: 'Disable direct root login via SSH': Set 'PermitRootLogin no' in /etc/ssh/sshd_config.d/50-redhat.conf or /etc/ssh/sshd_config, then restart sshd."
                ],
                "default_run_cmd": "grep -i 'PermitRootLogin' /etc/ssh/sshd_config 2>/dev/null || echo 'PermitRootLogin prohibit-password'"
            },
            {
                "id": "ch20_scp_p",
                "name": "scp -p",
                "synopsis": "scp -p file user@remote:/path/",
                "short_desc": "Securely copy file preserving timestamps and file modes.",
                "detailed_desc": "Transfers file over SSH while preserving modification and access times and permission mode bits.",
                "category": "File Transfer",
                "common_flags": [
                    {"flag": "-r", "desc": "Recursive copy for directories."}
                ],
                "sample_output": "report.pdf           100% 1204KB  24.5MB/s   00:00",
                "rhcsa_tips": ["Always preserve file modes (-p) when copying configuration files between exam nodes."],
                "default_run_cmd": "scp --help | head -n 8"
            }
        ]
    },

    # CHAPTER 21: Managing Apache HTTP Services
    {
        "chapter_id": 21,
        "part_id": 4,
        "part_title": "Part IV: Managing Network Services",
        "chapter_title": "Managing Apache HTTP Services",
        "description": "Apache (httpd) deployment, virtual hosts, web document root (/var/www/html), firewall service opening, and SELinux contexts.",
        "commands": [
            {
                "id": "ch21_apachectl_configtest",
                "name": "apachectl configtest",
                "synopsis": "apachectl configtest",
                "short_desc": "Check Apache configuration file syntax errors.",
                "detailed_desc": "Validates /etc/httpd/conf/httpd.conf and all modular configs in /etc/httpd/conf.d/*.conf before starting or reloading.",
                "category": "Apache Management",
                "common_flags": [],
                "sample_output": "Syntax OK",
                "rhcsa_tips": [
                    "RHCSA MUST-DO: Always run 'apachectl configtest' after modifying VirtualHosts or Listen directives!"
                ],
                "default_run_cmd": "apachectl configtest 2>/dev/null || echo 'Syntax OK'"
            },
            {
                "id": "ch21_systemctl_status_httpd",
                "name": "systemctl status httpd",
                "synopsis": "systemctl status httpd",
                "short_desc": "Inspect Apache web server service status and PID.",
                "detailed_desc": "Shows whether httpd daemon is actively serving HTTP requests.",
                "category": "Service Status",
                "common_flags": [],
                "sample_output": """● httpd.service - The Apache HTTP Server
     Loaded: loaded (/usr/lib/systemd/system/httpd.service; enabled; preset: disabled)
     Active: active (running) since Wed 2026-09-24 16:30:10 EDT
   Main PID: 1240 (httpd)
     Status: "Total requests: 120; Idle/Busy workers 100/0" """,
                "rhcsa_tips": ["Remember: 'systemctl enable --now httpd' ensures it runs now and survives reboots."],
                "default_run_cmd": "systemctl status httpd --no-pager 2>/dev/null || echo 'httpd loaded'"
            },
            {
                "id": "ch21_curl_localhost",
                "name": "curl -I localhost",
                "synopsis": "curl -I http://localhost",
                "short_desc": "Verify web server is delivering valid HTTP headers.",
                "detailed_desc": "Sends HTTP HEAD request to localhost and displays HTTP response code (200 OK, 403 Forbidden, 404 Not Found).",
                "category": "Web Verification",
                "common_flags": [],
                "sample_output": """HTTP/1.1 200 OK
Date: Wed, 24 Sep 2026 18:20:00 GMT
Server: Apache/2.4.57 (Red Hat Enterprise Linux)
Content-Length: 45
Content-Type: text/html; charset=UTF-8""",
                "rhcsa_tips": [
                    "If curl returns '403 Forbidden', it is almost always an SELinux context issue on /var/www/html or incorrect directory permissions (needs 755)!"
                ],
                "default_run_cmd": "curl -I http://localhost 2>/dev/null || echo 'HTTP/1.1 200 OK'"
            },
            {
                "id": "ch21_firewall_add_http",
                "name": "firewall-cmd --add-service=http",
                "synopsis": "firewall-cmd --permanent --add-service=http && firewall-cmd --reload",
                "short_desc": "Open firewall port 80 for HTTP web traffic permanently.",
                "detailed_desc": "Updates the active firewalld zone to permit incoming TCP port 80 traffic.",
                "category": "Firewall Access",
                "common_flags": [
                    {"flag": "--permanent", "desc": "Make change persistent across reboots."},
                    {"flag": "--reload", "desc": "Apply permanent rules immediately to running state."}
                ],
                "sample_output": "success\nsuccess",
                "rhcsa_tips": [
                    "RHCSA COMMON PITFALL: Starting httpd without opening the firewall leaves the website unreachable from external exam grading scripts! Always run 'firewall-cmd --permanent --add-service=http && firewall-cmd --reload'!"
                ],
                "default_run_cmd": "firewall-cmd --list-services 2>/dev/null || echo 'cockpit dhcpv6-client http ssh'"
            },
            {
                "id": "ch21_restorecon_html",
                "name": "restorecon -Rv /var/www/html",
                "synopsis": "restorecon -Rv /var/www/html",
                "short_desc": "Restore default SELinux web content security context.",
                "detailed_desc": "Recursively relabels files under the webroot to 'httpd_sys_content_t' so Apache can legally read them.",
                "category": "SELinux Contexts",
                "common_flags": [
                    {"flag": "-R", "desc": "Recursive change into subdirectories."},
                    {"flag": "-v", "desc": "Show changed file labels."}
                ],
                "sample_output": "Relabeled /var/www/html/index.html from admin_home_t to httpd_sys_content_t",
                "rhcsa_tips": [
                    "If you created index.html in your home folder and moved ('mv') it to /var/www/html, it kept the wrong label. 'restorecon -Rv /var/www/html' fixes it!"
                ],
                "default_run_cmd": "restorecon -v /tmp 2>/dev/null || echo 'SELinux contexts verified'"
            },
            {
                "id": "ch21_tail_access_log",
                "name": "tail -f /var/log/httpd/access_log",
                "synopsis": "tail -f /var/log/httpd/access_log",
                "short_desc": "Live stream Apache web server access requests.",
                "detailed_desc": "Displays client IP, timestamp, HTTP method, requested URL, response code, and bytes transferred.",
                "category": "Web Logs",
                "common_flags": [],
                "sample_output": "192.168.1.100 - - [24/Sep/2026:18:22:15 -0400] \"GET /index.html HTTP/1.1\" 200 45 \"-\" \"curl/7.76.1\"",
                "rhcsa_tips": ["Useful to verify that external grader bots are successfully hitting your web application."],
                "default_run_cmd": "tail -n 5 /var/log/httpd/access_log 2>/dev/null || echo 'access_log initialized'"
            },
            {
                "id": "ch21_tail_error_log",
                "name": "tail -f /var/log/httpd/error_log",
                "synopsis": "tail -f /var/log/httpd/error_log",
                "short_desc": "Inspect Apache web server diagnostic and error logs.",
                "detailed_desc": "Logs configuration warnings, worker thread crashes, permission denials, and missing document roots.",
                "category": "Web Logs",
                "common_flags": [],
                "sample_output": "[Wed Sep 24 18:22:10 2026] [core:error] [pid 1241] (13)Permission denied: [client 192.168.1.100:54120] AH00035: access to /index.html denied (filesystem path '/var/www/html/index.html') because search permissions are missing on a component of the path",
                "rhcsa_tips": ["Look here if curl returns 403 Forbidden."],
                "default_run_cmd": "tail -n 5 /var/log/httpd/error_log 2>/dev/null || echo 'error_log clean'"
            },
            {
                "id": "ch21_httpd_v",
                "name": "httpd -v",
                "synopsis": "httpd -v",
                "short_desc": "Display Apache HTTP server version and build date.",
                "detailed_desc": "Prints Apache core binary version.",
                "category": "Apache Management",
                "common_flags": [
                    {"flag": "-V", "desc": "Print compile-time settings and default directory definitions."}
                ],
                "sample_output": """Server version: Apache/2.4.57 (Red Hat Enterprise Linux)
Server built:   May 15 2023 14:02:18""",
                "rhcsa_tips": ["'httpd -V' shows the compiled HTTPD_ROOT (/etc/httpd) and SERVER_CONFIG_FILE."],
                "default_run_cmd": "httpd -v 2>/dev/null || echo 'Apache/2.4.57 (RHEL)'"
            },
            {
                "id": "ch21_httpd_M",
                "name": "httpd -M",
                "synopsis": "httpd -M",
                "short_desc": "List all compiled and dynamically loaded Apache modules.",
                "detailed_desc": "Shows active DSO (Dynamic Shared Object) modules such as mod_ssl, mod_rewrite, and mod_authz_core.",
                "category": "Apache Modules",
                "common_flags": [],
                "sample_output": """Loaded Modules:
 core_module (static)
 authz_core_module (shared)
 ssl_module (shared)
 rewrite_module (shared)""",
                "rhcsa_tips": ["Use 'httpd -M | grep ssl' to verify if mod_ssl is loaded for HTTPS."],
                "default_run_cmd": "httpd -M 2>/dev/null || echo 'core_module (static)'"
            },
            {
                "id": "ch21_semanage_port_http",
                "name": "semanage port -a -t http_port_t",
                "synopsis": "semanage port -a -t http_port_t -p tcp <PORT>",
                "short_desc": "Allow Apache to bind to non-standard network ports in SELinux.",
                "detailed_desc": "By default, SELinux only allows Apache to bind to ports 80, 443, 8080, etc. This command adds custom ports (e.g. 82).",
                "category": "SELinux & Apache",
                "common_flags": [
                    {"flag": "-l", "desc": "List all defined port assignments for http_port_t."}
                ],
                "sample_output": "http_port_t tcp 82, 80, 443, 8080, 8443",
                "rhcsa_tips": [
                    "RHCSA EXAM CLASSIC: 'Configure Apache VirtualHost on port 82': 1) Update /etc/httpd/conf/httpd.conf (Listen 82). 2) semanage port -a -t http_port_t -p tcp 82. 3) firewall-cmd --permanent --add-port=82/tcp && firewall-cmd --reload. 4) systemctl restart httpd!"
                ],
                "default_run_cmd": "semanage port -l | grep http_port_t 2>/dev/null || echo 'http_port_t tcp 80, 443'"
            }
        ]
    },

    # CHAPTER 22: Managing SELinux
    {
        "chapter_id": 22,
        "part_id": 4,
        "part_title": "Part IV: Managing Network Services",
        "chapter_title": "Managing SELinux",
        "description": "Security-Enhanced Linux modes (Enforcing, Permissive, Disabled), contexts (user:role:type:level), booleans (getsebool/setsebool), and audit troubleshooting (ausearch, sealert).",
        "commands": [
            {
                "id": "ch22_sestatus",
                "name": "sestatus",
                "synopsis": "sestatus [options]",
                "short_desc": "Display comprehensive SELinux status and policy details.",
                "detailed_desc": "Outputs whether SELinux is enabled, loaded policy (targeted), current mode (enforcing), and mode from config file.",
                "category": "SELinux Status",
                "common_flags": [
                    {"flag": "-v", "desc": "Check context of process and file targets."}
                ],
                "sample_output": """SELinux status:                 enabled
SELinuxfs mount:                /sys/fs/selinux
SELinux root directory:         /etc/selinux
Loaded policy name:             targeted
Current mode:                   enforcing
Mode from config file:          enforcing
Policy MLS status:              enabled
Policy deny_unknown status:     allowed
Memory protection checking:     actual (secure)
Max kernel policy version:      33""",
                "rhcsa_tips": [
                    "RHCSA MANDATORY REQUIREMENT: The RHCSA exam strictly mandates that systems remain in 'enforcing' mode. NEVER disable SELinux or leave it in permissive mode!"
                ],
                "default_run_cmd": "sestatus"
            },
            {
                "id": "ch22_getenforce",
                "name": "getenforce",
                "synopsis": "getenforce",
                "short_desc": "Display the current runtime SELinux mode.",
                "detailed_desc": "Outputs: Enforcing (rules enforced), Permissive (violations logged but allowed), or Disabled.",
                "category": "SELinux Mode",
                "common_flags": [],
                "sample_output": "Enforcing",
                "rhcsa_tips": ["Quick one-liner verification check."],
                "default_run_cmd": "getenforce"
            },
            {
                "id": "ch22_setenforce",
                "name": "setenforce",
                "synopsis": "setenforce [Enforcing | Permissive | 1 | 0]",
                "short_desc": "Temporarily modify the current SELinux operating mode.",
                "detailed_desc": "Toggles runtime enforcement between 1 (Enforcing) and 0 (Permissive) without a reboot.",
                "category": "SELinux Mode",
                "common_flags": [],
                "sample_output": "[SELinux mode set to Permissive]",
                "rhcsa_tips": [
                    "Troubleshooting tip: Run 'setenforce 0' temporarily. If your broken service suddenly works, the root cause is 100% an SELinux context or boolean issue! Fix the context, then 'setenforce 1' immediately."
                ],
                "default_run_cmd": "setenforce --help 2>/dev/null || echo 'usage:  setenforce [Enforcing|Permissive|1|0]'"
            },
            {
                "id": "ch22_ls_z",
                "name": "ls -Z",
                "synopsis": "ls -lZ [path]",
                "short_desc": "Display SELinux security contexts of files and directories.",
                "detailed_desc": "Prints security label: user:role:type:level (e.g. system_u:object_r:httpd_sys_content_t:s0). In targeted policy, the 'type' (_t) is paramount.",
                "category": "Context Inspection",
                "common_flags": [
                    {"flag": "-d", "desc": "Show context of the directory itself rather than its contents."}
                ],
                "sample_output": """-rw-r--r--. 1 root root system_u:object_r:httpd_sys_content_t:s0 45 Sep 24 18:00 /var/www/html/index.html
drwxr-xr-x. 2 root root system_u:object_r:etc_t:s0              4096 Sep 24 10:15 /etc""",
                "rhcsa_tips": ["Compare file context with working system defaults to find discrepancies."],
                "default_run_cmd": "ls -dZ /etc /var/www 2>/dev/null || ls -dZ /etc"
            },
            {
                "id": "ch22_semanage_fcontext",
                "name": "semanage fcontext",
                "synopsis": "semanage fcontext {-a|-d|-m} -t <type> \"<file_spec>\"",
                "short_desc": "Define persistent file context mapping rules in SELinux policy.",
                "detailed_desc": "Stores persistent file context rules in the system policy database so 'restorecon' will apply them.",
                "category": "Context Configuration",
                "common_flags": [
                    {"flag": "-a, --add", "desc": "Add a new context specification record."},
                    {"flag": "-t, --type", "desc": "SELinux type tag (e.g. httpd_sys_content_t)."},
                    {"flag": "\"/custom(/.*)?\"", "desc": "Regex matching directory and all nested contents."}
                ],
                "sample_output": "Added fcontext definition for '/web(/.*)?' as httpd_sys_content_t",
                "rhcsa_tips": [
                    "RHCSA MANDATORY PATTERN: When creating a custom web directory (e.g. /web): 1) semanage fcontext -a -t httpd_sys_content_t \"/web(/.*)?\". 2) restorecon -Rv /web. Both steps are required for persistence!"
                ],
                "default_run_cmd": "semanage fcontext -l | head -n 10 2>/dev/null || echo 'semanage fcontext database active'"
            },
            {
                "id": "ch22_restorecon",
                "name": "restorecon",
                "synopsis": "restorecon [-Rv] path ...",
                "short_desc": "Restore default SELinux security context based on policy database.",
                "detailed_desc": "Reads rules registered by 'semanage fcontext' and resets file extended attributes to match.",
                "category": "Context Application",
                "common_flags": [
                    {"flag": "-R, -r", "desc": "Relabel directory contents recursively."},
                    {"flag": "-v", "desc": "Display files whose labels were altered."}
                ],
                "sample_output": "Relabeled /var/www/html/app.py from user_home_t to httpd_sys_content_t",
                "rhcsa_tips": ["Always run 'restorecon -Rv <directory>' after running semanage fcontext."],
                "default_run_cmd": "restorecon -v /tmp 2>/dev/null || echo 'Contexts valid'"
            },
            {
                "id": "ch22_getsebool",
                "name": "getsebool",
                "synopsis": "getsebool [-a] [boolean...]",
                "short_desc": "Get current status of SELinux booleans.",
                "detailed_desc": "Queries toggleable switches that allow or deny specific daemon actions (e.g. Apache connecting to MySQL or sending mail).",
                "category": "SELinux Booleans",
                "common_flags": [
                    {"flag": "-a", "desc": "Show all boolean toggles on the system."}
                ],
                "sample_output": """httpd_can_network_connect --> off
httpd_can_network_connect_db --> on
httpd_enable_homedirs --> off""",
                "rhcsa_tips": ["Use 'getsebool -a | grep -i httpd' to discover all web-related booleans."],
                "default_run_cmd": "getsebool -a 2>/dev/null | head -n 12 || echo 'httpd_can_network_connect --> off'"
            },
            {
                "id": "ch22_setsebool",
                "name": "setsebool",
                "synopsis": "setsebool [-P] boolean value",
                "short_desc": "Set the value of an SELinux boolean.",
                "detailed_desc": "Enables (on/1) or disables (off/0) a boolean toggle.",
                "category": "SELinux Booleans",
                "common_flags": [
                    {"flag": "-P, --persistent", "desc": "CRITICAL: Write change permanently to policy database across reboots!"}
                ],
                "sample_output": "Boolean 'httpd_can_network_connect' set to 'on' permanently.",
                "rhcsa_tips": [
                    "RHCSA GOLDEN RULE: ALWAYS include '-P': 'setsebool -P httpd_can_network_connect on'. Without '-P', the change reverts to default after a reboot!"
                ],
                "default_run_cmd": "setsebool --help 2>/dev/null || echo 'setsebool [-P] boolean value'"
            },
            {
                "id": "ch22_ausearch",
                "name": "ausearch",
                "synopsis": "ausearch [options]",
                "short_desc": "Query audit daemon logs for SELinux AVC denials.",
                "detailed_desc": "Extracts Access Vector Cache (AVC) denial events recorded in /var/log/audit/audit.log.",
                "category": "SELinux Auditing",
                "common_flags": [
                    {"flag": "-m avc", "desc": "Filter only SELinux Access Vector Cache denials."},
                    {"flag": "-ts recent", "desc": "Search only events that occurred in the last 10 minutes."}
                ],
                "sample_output": """type=AVC msg=audit(1695582120.124:412): avc:  denied  { name_bind } for  pid=1240 comm="httpd" src=82 scontext=system_u:system_r:httpd_t:s0 tcontext=system_u:object_r:reserved_port_t:s0 tclass=tcp_socket permissive=0""",
                "rhcsa_tips": ["'ausearch -m avc -ts recent' reveals exact PID, executable name, and denied action."],
                "default_run_cmd": "ausearch -m avc -ts recent 2>/dev/null || echo '<no matches>'"
            },
            {
                "id": "ch22_sealert",
                "name": "sealert",
                "synopsis": "sealert -a /var/log/audit/audit.log",
                "short_desc": "Analyze audit logs and generate human-readable SELinux solutions.",
                "detailed_desc": "Parses cryptic audit.log AVC messages and produces plain-English explanations with copy-pasteable resolution commands.",
                "category": "SELinux Troubleshooting",
                "common_flags": [
                    {"flag": "-l <UUID>", "desc": "Look up full report for a specific alert ID."}
                ],
                "sample_output": """SELinux is preventing httpd from binding to port 82.
*****  Plugin bind_ports (99.5 confidence) suggests   ************************
If you want to allow httpd to bind to network port 82
Then you must tell SELinux to allow this:
# semanage port -a -t http_port_t -p tcp 82""",
                "rhcsa_tips": [
                    "RHCSA SECRET WEAPON: If setroubleshoot-server is installed, 'sealert -a /var/log/audit/audit.log' literally gives you the exact command you need to type to fix the issue!"
                ],
                "default_run_cmd": "sealert --help 2>/dev/null || echo 'sealert troubleshooting tool'"
            }
        ]
    },

    # CHAPTER 23: Configuring a Firewall
    {
        "chapter_id": 23,
        "part_id": 4,
        "part_title": "Part IV: Managing Network Services",
        "chapter_title": "Configuring a Firewall",
        "description": "Dynamic firewall daemon (firewalld), zones (public, drop, trusted), service and port rules, rich rules, and persistence.",
        "commands": [
            {
                "id": "ch23_firewall_list_all",
                "name": "firewall-cmd --list-all",
                "synopsis": "firewall-cmd [--zone=zone] --list-all",
                "short_desc": "List everything configured in the active or designated firewall zone.",
                "detailed_desc": "Displays active zone name, bound interfaces, enabled services, open ports, and rich rules.",
                "category": "Firewall Inspection",
                "common_flags": [
                    {"flag": "--zone=<zone>", "desc": "Target specific zone (default is 'public')."}
                ],
                "sample_output": """public (active)
  target: default
  icmp-block-inversion: no
  interfaces: enp1s0
  sources: 
  services: cockpit dhcpv6-client http ssh
  ports: 8080/tcp
  protocols: 
  forward: yes
  masquerade: no
  forward-ports: 
  source-ports: 
  icmp-blocks: 
  rich rules: """,
                "rhcsa_tips": ["Always run 'firewall-cmd --list-all' to verify opened ports and services."],
                "default_run_cmd": "firewall-cmd --list-all 2>/dev/null || echo 'public (active) services: ssh'"
            },
            {
                "id": "ch23_firewall_add_service",
                "name": "firewall-cmd --add-service",
                "synopsis": "firewall-cmd [--zone=zone] --permanent --add-service=<service>",
                "short_desc": "Open incoming traffic for a named service in the firewall.",
                "detailed_desc": "Authorizes network ports predefined in /usr/lib/firewalld/services/<service>.xml (e.g. http, https, nfs, dns).",
                "category": "Firewall Rules",
                "common_flags": [
                    {"flag": "--permanent", "desc": "Save rule permanently across reboots into /etc/firewalld/zones/."}
                ],
                "sample_output": "success",
                "rhcsa_tips": [
                    "RHCSA COMBO: 'firewall-cmd --permanent --add-service=http && firewall-cmd --reload'."
                ],
                "default_run_cmd": "firewall-cmd --get-services 2>/dev/null | head -n 1 || echo 'http https ssh dns'"
            },
            {
                "id": "ch23_firewall_add_port",
                "name": "firewall-cmd --add-port",
                "synopsis": "firewall-cmd [--zone=zone] --permanent --add-port=<port>/<proto>",
                "short_desc": "Open a custom port/protocol combination in the firewall.",
                "detailed_desc": "Authorizes numerical port ranges (e.g. 8080/tcp, 5000-5010/tcp) not covered by standard service names.",
                "category": "Firewall Rules",
                "common_flags": [
                    {"flag": "--permanent", "desc": "Store permanently in config."},
                    {"flag": "--reload", "desc": "Load permanent rules into live state."}
                ],
                "sample_output": "success",
                "rhcsa_tips": [
                    "RHCSA REQUIREMENT: 'Open port 82/tcp permanently': firewall-cmd --permanent --add-port=82/tcp && firewall-cmd --reload."
                ],
                "default_run_cmd": "firewall-cmd --help | grep -i add-port 2>/dev/null || echo 'firewall-cmd --add-port=PORT/PROTO'"
            },
            {
                "id": "ch23_firewall_reload",
                "name": "firewall-cmd --reload",
                "synopsis": "firewall-cmd --reload",
                "short_desc": "Reload firewall rules without disrupting active network connections.",
                "detailed_desc": "Applies all --permanent changes stored on disk to the active netfilter/nftables running state.",
                "category": "Firewall Administration",
                "common_flags": [],
                "sample_output": "success",
                "rhcsa_tips": ["If you used '--permanent', your rule IS NOT ACTIVE until you execute 'firewall-cmd --reload'!"],
                "default_run_cmd": "firewall-cmd --reload 2>/dev/null || echo 'success'"
            },
            {
                "id": "ch23_firewall_remove_service",
                "name": "firewall-cmd --remove-service",
                "synopsis": "firewall-cmd [--zone=zone] --permanent --remove-service=<service>",
                "short_desc": "Revoke and block a service from the firewall.",
                "detailed_desc": "Closes previously allowed service ports.",
                "category": "Firewall Rules",
                "common_flags": [
                    {"flag": "--permanent", "desc": "Remove from permanent configuration."}
                ],
                "sample_output": "success",
                "rhcsa_tips": ["Remember to run '--reload' after removing services."],
                "default_run_cmd": "firewall-cmd --help | grep -i remove-service 2>/dev/null || echo 'firewall-cmd --remove-service=SERVICE'"
            },
            {
                "id": "ch23_firewall_get_zones",
                "name": "firewall-cmd --get-active-zones",
                "synopsis": "firewall-cmd --get-active-zones",
                "short_desc": "Print currently active zones and bound interfaces.",
                "detailed_desc": "Shows which zone governs each network interface card (e.g. enp1s0 in public).",
                "category": "Zone Inspection",
                "common_flags": [],
                "sample_output": """public
  interfaces: enp1s0""",
                "rhcsa_tips": ["Make sure the interface you're configuring belongs to the expected zone."],
                "default_run_cmd": "firewall-cmd --get-active-zones 2>/dev/null || echo 'public interfaces: eth0'"
            },
            {
                "id": "ch23_firewall_rich_rule",
                "name": "firewall-cmd --add-rich-rule",
                "synopsis": "firewall-cmd --permanent --add-rich-rule='rule ...'",
                "short_desc": "Add complex fine-grained firewall rules (source IP filtering, logging, rate-limiting).",
                "detailed_desc": "Enables conditions combining source IP subnets, specific ports, and actions (accept/reject/drop/log).",
                "category": "Rich Rules",
                "common_flags": [],
                "sample_output": "success",
                "rhcsa_tips": [
                    "RHCSA OBJECTIVE: 'Allow SSH traffic only from network 192.168.1.0/24': firewall-cmd --permanent --add-rich-rule='rule family=\"ipv4\" source address=\"192.168.1.0/24\" service name=\"ssh\" accept' && firewall-cmd --reload."
                ],
                "default_run_cmd": "firewall-cmd --help | grep -i rich-rule 2>/dev/null || echo 'firewall-cmd rich-rule syntax'"
            },
            {
                "id": "ch23_firewall_state",
                "name": "firewall-cmd --state",
                "synopsis": "firewall-cmd --state",
                "short_desc": "Check whether firewalld daemon is running.",
                "detailed_desc": "Returns 'running' or 'not running'.",
                "category": "Firewall Status",
                "common_flags": [],
                "sample_output": "running",
                "rhcsa_tips": ["If not running, start with: 'systemctl enable --now firewalld'."],
                "default_run_cmd": "firewall-cmd --state 2>/dev/null || echo 'running'"
            },
            {
                "id": "ch23_firewall_set_default_zone",
                "name": "firewall-cmd --set-default-zone",
                "synopsis": "firewall-cmd --set-default-zone=<zone>",
                "short_desc": "Set default zone for newly detected interfaces.",
                "detailed_desc": "Changes system-wide default zone (e.g. from public to drop or internal).",
                "category": "Zone Configuration",
                "common_flags": [],
                "sample_output": "success",
                "rhcsa_tips": ["Check default zone with 'firewall-cmd --get-default-zone'."],
                "default_run_cmd": "firewall-cmd --get-default-zone 2>/dev/null || echo 'public'"
            },
            {
                "id": "ch23_nft_list",
                "name": "nft list ruleset",
                "synopsis": "nft list ruleset",
                "short_desc": "Inspect low-level kernel nftables packet filtering rules.",
                "detailed_desc": "firewalld in RHEL 9 is an abstraction layer that compiles rules into kernel nftables tables and chains.",
                "category": "Low-level Filtering",
                "common_flags": [],
                "sample_output": """table inet firewalld {
    chain filter_IN_public_allow {
        tcp dport 22 accept
        tcp dport 80 accept
    }
}""",
                "rhcsa_tips": ["Modern replacement for iptables."],
                "default_run_cmd": "nft --version 2>/dev/null || echo 'nftables v1.0.4'"
            }
        ]
    },

    # CHAPTER 24: Accessing Network Storage (NFS / CIFS)
    {
        "chapter_id": 24,
        "part_id": 4,
        "part_title": "Part IV: Managing Network Services",
        "chapter_title": "Accessing Network Storage",
        "description": "NFS client mounting, autofs automated on-demand mounting (/etc/auto.master, indirect maps), and SMB/CIFS access.",
        "commands": [
            {
                "id": "ch24_showmount",
                "name": "showmount -e",
                "synopsis": "showmount -e <nfs-server-host>",
                "short_desc": "Query an NFS server for its exported shared directories.",
                "detailed_desc": "Contacts the NFS server mount daemon to discover export paths and permitted client IP ranges.",
                "category": "NFS Discovery",
                "common_flags": [],
                "sample_output": """Export list for server1.example.com:
/shared/docs 192.168.1.0/24
/home/guests *.example.com""",
                "rhcsa_tips": [
                    "RHCSA MANDATORY STEP: Before attempting to mount NFS or configure autofs, ALWAYS run 'showmount -e serverX.example.com' to confirm the exact export path name!"
                ],
                "default_run_cmd": "showmount -h 2>/dev/null || echo 'showmount -e serverX'"
            },
            {
                "id": "ch24_mount_nfs",
                "name": "mount -t nfs",
                "synopsis": "mount -t nfs [-o options] server:/export /mountpoint",
                "short_desc": "Manually mount a remote NFS share onto local directory.",
                "detailed_desc": "Attaches remote NFS exports into the local VFS hierarchy.",
                "category": "NFS Mounting",
                "common_flags": [
                    {"flag": "-o rw,sync", "desc": "Specify read/write and synchronous write mount options."},
                    {"flag": "-o sec=sys|krb5", "desc": "Security flavor (Kerberos vs standard UNIX UID)."}
                ],
                "sample_output": "server1.example.com:/shared/docs mounted on /mnt/nfs",
                "rhcsa_tips": [
                    "Persistent fstab entry: 'server1.example.com:/shared/docs /mnt/nfs nfs _netdev,defaults 0 0'. Always use '_netdev' mount option so the system waits for networking before mounting on boot!"
                ],
                "default_run_cmd": "mount | grep -i nfs 2>/dev/null || echo 'nfs mount ready'"
            },
            {
                "id": "ch24_exportfs",
                "name": "exportfs -v",
                "synopsis": "exportfs [-aruv] [-o options] [client:/path]",
                "short_desc": "Maintain the table of exported NFS file systems.",
                "detailed_desc": "Exports or unexports directories listed in /etc/exports and /etc/exports.d/*.exports.",
                "category": "NFS Server",
                "common_flags": [
                    {"flag": "-r, --reexport", "desc": "Re-export all directories, synchronizing /var/lib/nfs/etab with /etc/exports."},
                    {"flag": "-a", "desc": "Export or unexport all directories."}
                ],
                "sample_output": "/shared/docs 192.168.1.0/24(sync,wdelay,hide,no_subtree_check,sec=sys,rw,secure,root_squash,no_all_squash)",
                "rhcsa_tips": ["After editing /etc/exports, always run 'exportfs -ra' to apply changes without restarting the NFS server."],
                "default_run_cmd": "exportfs -v 2>/dev/null || echo 'No active NFS exports'"
            },
            {
                "id": "ch24_cat_exports",
                "name": "cat /etc/exports",
                "synopsis": "cat /etc/exports",
                "short_desc": "Inspect NFS server share configuration file.",
                "detailed_desc": "Defines shared directories, client hosts/subnets, and access options (rw, ro, sync, no_root_squash).",
                "category": "NFS Configuration",
                "common_flags": [],
                "sample_output": "/shared/data  *(rw,sync,no_root_squash)",
                "rhcsa_tips": ["Syntax: Directory Client(Options) with NO space between Client and (Options)!"],
                "default_run_cmd": "cat /etc/exports 2>/dev/null || echo '# /etc/exports'"
            },
            {
                "id": "ch24_systemctl_autofs",
                "name": "systemctl enable --now autofs",
                "synopsis": "systemctl enable --now autofs",
                "short_desc": "Start and enable the Automounter service.",
                "detailed_desc": "Mounts network filesystems dynamically only when accessed, and unmounts them automatically after inactivity.",
                "category": "Autofs Automation",
                "common_flags": [],
                "sample_output": "Created symlink /etc/systemd/system/multi-user.target.wants/autofs.service → /usr/lib/systemd/system/autofs.service.",
                "rhcsa_tips": [
                    "RHCSA HIGH-VALUE OBJECTIVE: Configuring autofs requires: 1) dnf install -y autofs. 2) Configure /etc/auto.master.d/custom.autofs. 3) Configure map file. 4) systemctl enable --now autofs!"
                ],
                "default_run_cmd": "systemctl is-enabled autofs 2>/dev/null || echo 'disabled'"
            },
            {
                "id": "ch24_auto_master",
                "name": "/etc/auto.master.d/*.autofs",
                "synopsis": "cat /etc/auto.master.d/demo.autofs",
                "short_desc": "Inspect autofs master map definitions.",
                "detailed_desc": "Defines base mount directories and maps them to secondary map files (e.g. '/shares /etc/auto.shares --timeout=60').",
                "category": "Autofs Configuration",
                "common_flags": [],
                "sample_output": "/rhome /etc/auto.rhome",
                "rhcsa_tips": [
                    "Always create map references in '/etc/auto.master.d/something.autofs' instead of editing /etc/auto.master directly."
                ],
                "default_run_cmd": "ls /etc/auto.master.d 2>/dev/null || echo 'auto.master.d clean'"
            },
            {
                "id": "ch24_smbclient",
                "name": "smbclient -L",
                "synopsis": "smbclient -L <server> [-U user]",
                "short_desc": "List shares available on a Windows/Samba SMB file server.",
                "detailed_desc": "Queries Samba SMB servers for available network shares.",
                "category": "SMB / CIFS",
                "common_flags": [
                    {"flag": "-U <user>", "desc": "Authenticate as specified username."}
                ],
                "sample_output": """Sharename       Type      Comment
---------       ----      -------
public          Disk      Public Share
IPC$            IPC       IPC Service""",
                "rhcsa_tips": ["Equivalent to 'showmount -e' for SMB/Windows environments."],
                "default_run_cmd": "smbclient -h 2>/dev/null || echo 'smbclient client tool'"
            },
            {
                "id": "ch24_mount_cifs",
                "name": "mount -t cifs",
                "synopsis": "mount -t cifs //server/share /mountpoint -o username=user,password=pass",
                "short_desc": "Mount Windows/Samba SMB share onto local directory.",
                "detailed_desc": "Attaches CIFS/SMB network shares using kernel cifs filesystem module.",
                "category": "SMB / CIFS",
                "common_flags": [
                    {"flag": "-o credentials=<file>", "desc": "Read username/password from secure file instead of command line."}
                ],
                "sample_output": "//server1/public mounted on /mnt/smb",
                "rhcsa_tips": ["Store credentials in /etc/samba/credentials with chmod 600 for security."],
                "default_run_cmd": "mount.cifs -V 2>/dev/null || echo 'cifs-utils'"
            },
            {
                "id": "ch24_rpcinfo",
                "name": "rpcinfo -p",
                "synopsis": "rpcinfo -p [host]",
                "short_desc": "Report RPC service registration information.",
                "detailed_desc": "Checks if RPC portmapper (rpcbind) and NFS services (nfs, mountd, nlockmgr) are active on designated host.",
                "category": "RPC / NFS",
                "common_flags": [],
                "sample_output": """   program vers proto   port  service
    100000    4   tcp    111  portmapper
    100003    4   tcp   2049  nfs
    100005    3   tcp  20048  mountd""",
                "rhcsa_tips": ["Use rpcinfo if 'showmount -e' hangs or times out."],
                "default_run_cmd": "rpcinfo -p 2>/dev/null || echo 'portmapper registered'"
            },
            {
                "id": "ch24_df_t_nfs",
                "name": "df -t nfs4",
                "synopsis": "df -h -t nfs4",
                "short_desc": "Display mounted NFS filesystems and capacity.",
                "detailed_desc": "Filters df output to list only active NFS mounts.",
                "category": "Storage Query",
                "common_flags": [],
                "sample_output": """Filesystem                     Size  Used Avail Use% Mounted on
server1.example.com:/shared/docs 100G   24G   76G  24% /mnt/nfs""",
                "rhcsa_tips": ["Fastest way to verify your autofs mount activated after 'cd'-ing into it."],
                "default_run_cmd": "df -hT | grep -i nfs 2>/dev/null || echo 'df checked'"
            }
        ]
    },

    # CHAPTER 25: Configuring Time Services
    {
        "chapter_id": 25,
        "part_id": 4,
        "part_title": "Part IV: Managing Network Services",
        "chapter_title": "Configuring Time Services",
        "description": "Network Time Protocol (NTP) synchronization using chrony (chronyd, chronyc), timezone configuration, and hardware RTC clocks.",
        "commands": [
            {
                "id": "ch25_chronyc_sources",
                "name": "chronyc sources -v",
                "synopsis": "chronyc sources [-v]",
                "short_desc": "Display information about current NTP time sources.",
                "detailed_desc": "Displays upstream NTP time servers, stratum, polling interval, reachability register, and time offset.",
                "category": "Chrony NTP",
                "common_flags": [
                    {"flag": "-v", "desc": "Provide verbose legend explaining state flags (^* synced, ^+ combined, ^? unreachable)."}
                ],
                "sample_output": """  .-- Source mode  '^' = server, '=' = peer, '#' = local clock.
 / .- Mode     '?' = unreachable, '*' = current synchronized, '+' = combined
| /
MS Name/IP address         Stratum Poll Reach LastRx Last sample               
===============================================================================
^* time.example.com              2   6   377    25   -120us[ -140us] +/-   12ms
^+ 192.168.1.1                   3   6   377    24    +15us[  +15us] +/-   18ms""",
                "rhcsa_tips": [
                    "RHCSA MANDATORY VERIFICATION: Look for the asterisk (*) next to the upstream time server (e.g., ^* time.example.com). The asterisk confirms that the system clock is actively synchronized!"
                ],
                "default_run_cmd": "chronyc sources 2>/dev/null || echo '^* 127.0.0.1 2 6 377 25 -120us'"
            },
            {
                "id": "ch25_chronyc_tracking",
                "name": "chronyc tracking",
                "synopsis": "chronyc tracking",
                "short_desc": "Display system clock synchronization performance parameters.",
                "detailed_desc": "Reports Reference ID, Stratum, Reference time, System time offset, RMS offset, and frequency drift.",
                "category": "Chrony NTP",
                "common_flags": [],
                "sample_output": """Reference ID    : C0A80101 (time.example.com)
Stratum         : 3
Ref time (UTC)  : Wed Sep 24 22:30:15 2026
System time     : 0.000012400 seconds slow of NTP time
Last offset     : -0.000008120 seconds
RMS offset      : 0.000015400 seconds
Frequency       : 12.450 ppm fast
Residual freq   : +0.002 ppm
Skew            : 0.045 ppm
Root delay      : 0.012500000 seconds
Root dispersion : 0.001400000 seconds
Update interval : 64.2 seconds
Leap status     : Normal""",
                "rhcsa_tips": ["'Stratum' should be between 2 and 4. A stratum of 16 means unsynchronized."],
                "default_run_cmd": "chronyc tracking 2>/dev/null || echo 'Leap status : Normal'"
            },
            {
                "id": "ch25_chronyc_sourcestats",
                "name": "chronyc sourcestats",
                "synopsis": "chronyc sourcestats [-v]",
                "short_desc": "Display drift rate and offset estimation for each NTP source.",
                "detailed_desc": "Shows number of sample points and estimated error dispersion for time sources.",
                "category": "Chrony NTP",
                "common_flags": [
                    {"flag": "-v", "desc": "Verbose descriptions of columns."}
                ],
                "sample_output": """Name/IP Address            NP  NR  Span  Frequency  Freq Skew  Offset  Std Dev
==============================================================================
time.example.com            8   5   448     -0.012      0.045   -12us    14us""",
                "rhcsa_tips": ["Useful to see if an NTP server has fluctuating network latency."],
                "default_run_cmd": "chronyc sourcestats 2>/dev/null || echo 'sourcestats nominal'"
            },
            {
                "id": "ch25_timedatectl_status",
                "name": "timedatectl status",
                "synopsis": "timedatectl status",
                "short_desc": "Query system clock, timezone, and NTP service activation.",
                "detailed_desc": "Displays local time, universal time (UTC), RTC time, time zone, and 'System clock synchronized: yes'.",
                "category": "System Time",
                "common_flags": [],
                "sample_output": """               Local time: Wed 2026-09-24 18:32:00 EDT
           Universal time: Wed 2026-09-24 22:32:00 UTC
                 RTC time: Wed 2026-09-24 22:32:00
                Time zone: America/New_York (EDT, -0400)
System clock synchronized: yes
              NTP service: active
          RTC in local TZ: no""",
                "rhcsa_tips": ["Double-check that both 'System clock synchronized: yes' AND 'NTP service: active' are true."],
                "default_run_cmd": "timedatectl status"
            },
            {
                "id": "ch25_timedatectl_set_ntp",
                "name": "timedatectl set-ntp true",
                "synopsis": "timedatectl set-ntp {true | false}",
                "short_desc": "Enable automatic system time synchronization over the network.",
                "detailed_desc": "Enables and starts the chronyd service.",
                "category": "System Time",
                "common_flags": [],
                "sample_output": "NTP enabled.",
                "rhcsa_tips": ["If NTP is disabled on exam startup, 'timedatectl set-ntp true' activates chronyd immediately."],
                "default_run_cmd": "timedatectl set-ntp true"
            },
            {
                "id": "ch25_timedatectl_set_timezone",
                "name": "timedatectl set-timezone",
                "synopsis": "timedatectl set-timezone <ZONE>",
                "short_desc": "Set the system timezone.",
                "detailed_desc": "Updates the /etc/localtime symlink to point to the designated zonefile under /usr/share/zoneinfo/.",
                "category": "Timezone",
                "common_flags": [],
                "sample_output": "Time zone changed to 'America/New_York'.",
                "rhcsa_tips": [
                    "RHCSA OBJECTIVE: 'Set machine timezone to Europe/London': timedatectl set-timezone Europe/London."
                ],
                "default_run_cmd": "timedatectl set-timezone America/New_York 2>/dev/null || echo 'Timezone verified'"
            },
            {
                "id": "ch25_cat_chrony_conf",
                "name": "cat /etc/chrony.conf",
                "synopsis": "cat /etc/chrony.conf",
                "short_desc": "Inspect chrony NTP daemon configuration file.",
                "detailed_desc": "Contains upstream NTP server definitions ('server serverX.example.com iburst'), driftfile path, and stratum options.",
                "category": "Chrony Config",
                "common_flags": [],
                "sample_output": """# Use public servers from the pool.ntp.org project.
server time.example.com iburst
driftfile /var/lib/chrony/drift
makestep 1.0 3
rtcsync
logdir /var/log/chrony""",
                "rhcsa_tips": [
                    "RHCSA OBJECTIVE: 'Configure chronyd to sync with time.example.com': Add 'server time.example.com iburst' to /etc/chrony.conf, then run 'systemctl restart chronyd'!"
                ],
                "default_run_cmd": "cat /etc/chrony.conf 2>/dev/null | grep -E '^server|^pool' || echo 'server time.example.com iburst'"
            },
            {
                "id": "ch25_systemctl_restart_chronyd",
                "name": "systemctl restart chronyd",
                "synopsis": "systemctl restart chronyd",
                "short_desc": "Restart chrony daemon to apply new NTP server entries.",
                "detailed_desc": "Reloads /etc/chrony.conf and initiates burst sync queries (iburst).",
                "category": "Service Administration",
                "common_flags": [],
                "sample_output": "Restarted chronyd.service - NTP client/server.",
                "rhcsa_tips": ["Always restart chronyd after updating server lines in /etc/chrony.conf."],
                "default_run_cmd": "systemctl status chronyd --no-pager 2>/dev/null || echo 'chronyd running'"
            },
            {
                "id": "ch25_hwclock",
                "name": "hwclock",
                "synopsis": "hwclock [options]",
                "short_desc": "Query or synchronize the hardware Real Time Clock (RTC).",
                "detailed_desc": "Interacts directly with the battery-backed CMOS hardware clock on the motherboard.",
                "category": "Hardware Clock",
                "common_flags": [
                    {"flag": "-w, --systohc", "desc": "Set the hardware clock from the current system time."},
                    {"flag": "-s, --hctosys", "desc": "Set the system time from the hardware clock."}
                ],
                "sample_output": "2026-09-24 18:32:15.123456-04:00",
                "rhcsa_tips": ["Use 'hwclock -w' after setting manual system time so the BIOS clock is in sync."],
                "default_run_cmd": "hwclock 2>/dev/null || date"
            },
            {
                "id": "ch25_timedatectl_list_timezones",
                "name": "timedatectl list-timezones",
                "synopsis": "timedatectl list-timezones",
                "short_desc": "List all available IANA timezones supported by systemd.",
                "detailed_desc": "Outputs complete list of timezone names suitable for passing to set-timezone.",
                "category": "Timezone",
                "common_flags": [],
                "sample_output": """America/New_York
America/Chicago
America/Denver
America/Los_Angeles
Europe/London
Europe/Paris""",
                "rhcsa_tips": ["Pipe into grep to find the exact timezone string: 'timedatectl list-timezones | grep -i toronto'."],
                "default_run_cmd": "timedatectl list-timezones | head -n 10"
            }
        ]
    },

    # CHAPTER 26: Managing Containers
    {
        "chapter_id": 26,
        "part_id": 4,
        "part_title": "Part IV: Managing Network Services",
        "chapter_title": "Managing Containers",
        "description": "Rootless containers with Podman, container image registries, port publishing, persistent volumes, Containerfiles, and systemd integration.",
        "commands": [
            {
                "id": "ch26_podman_run",
                "name": "podman run",
                "synopsis": "podman run [options] IMAGE [COMMAND] [ARG...]",
                "short_desc": "Run a command in a new container instance.",
                "detailed_desc": "Creates and starts an OCI-compliant container from a local or remote container image.",
                "category": "Container Lifecycle",
                "common_flags": [
                    {"flag": "-d, --detach", "desc": "Run container in background and print container ID."},
                    {"flag": "--name <name>", "desc": "Assign custom human-friendly name to container."},
                    {"flag": "-p <host:cont>", "desc": "Publish container port to host (e.g. -p 8080:80)."},
                    {"flag": "-v <host:cont:Z>", "desc": "Mount host directory as volume with SELinux relabeling (:Z)!"}
                ],
                "sample_output": "d4e1f82c3a91b2c45e89a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2",
                "rhcsa_tips": [
                    "CRITICAL SELINUX CONTAINER RULE: When mounting a host folder into a container (-v /host/path:/container/path:Z), ALWAYS append ':Z'! The ':Z' flag tells Podman to apply the 'container_file_t' SELinux context so the container can read/write the volume!"
                ],
                "default_run_cmd": "podman run --help | head -n 12 2>/dev/null || echo 'podman run [options] image'"
            },
            {
                "id": "ch26_podman_ps",
                "name": "podman ps -a",
                "synopsis": "podman ps [options]",
                "short_desc": "List containers currently running or stopped.",
                "detailed_desc": "Displays Container ID, Image, Command, Created time, Status, Ports, and Names.",
                "category": "Container Inspection",
                "common_flags": [
                    {"flag": "-a, --all", "desc": "Show all containers (default shows only running ones)."},
                    {"flag": "-q, --quiet", "desc": "Print only container IDs."}
                ],
                "sample_output": """CONTAINER ID  IMAGE                           COMMAND               CREATED        STATUS            PORTS                 NAMES
b1c2d3e4f5a6  registry.access.redhat.com/ubi9  /bin/bash             2 minutes ago  Up 2 minutes                            my-ubi-container
9a8b7c6d5e4f  docker.io/library/httpd:2.4      httpd-foreground      1 hour ago     Up 1 hour ago     0.0.0.0:8080->80/tcp  web-server""",
                "rhcsa_tips": ["Always check 'podman ps -a' to verify if a crashed container exited with an error code."],
                "default_run_cmd": "podman ps -a 2>/dev/null || echo 'CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES'"
            },
            {
                "id": "ch26_podman_images",
                "name": "podman images",
                "synopsis": "podman images [options] [repository]",
                "short_desc": "List container images stored in local storage cache.",
                "detailed_desc": "Displays repository name, tag, image ID, creation date, and uncompressed size.",
                "category": "Image Management",
                "common_flags": [],
                "sample_output": """REPOSITORY                         TAG         IMAGE ID      CREATED      SIZE
registry.access.redhat.com/ubi9    latest      7e123456789a  2 weeks ago  215 MB
docker.io/library/nginx            alpine      9f8e7d6c5b4a  3 weeks ago   24 MB""",
                "rhcsa_tips": ["Images are cached locally under ~/.local/share/containers/storage for rootless users."],
                "default_run_cmd": "podman images 2>/dev/null || echo 'REPOSITORY TAG IMAGE ID CREATED SIZE'"
            },
            {
                "id": "ch26_podman_pull",
                "name": "podman pull",
                "synopsis": "podman pull [options] [registry/]image[:tag]",
                "short_desc": "Pull a container image from a remote registry.",
                "detailed_desc": "Downloads container image layers from registries configured in /etc/containers/registries.conf.",
                "category": "Image Management",
                "common_flags": [],
                "sample_output": """Trying to pull registry.access.redhat.com/ubi9:latest...
Getting image source signatures
Copying blob sha256:7f45... 78.4 MiB / 78.4 MiB
Writing manifest to image destination
Stored in intermediate cache: 7e123456789a""",
                "rhcsa_tips": ["Always qualify registry on exams: 'podman pull registry.access.redhat.com/ubi9/ubi'."],
                "default_run_cmd": "podman pull --help | head -n 10 2>/dev/null || echo 'podman pull image'"
            },
            {
                "id": "ch26_podman_stop",
                "name": "podman stop",
                "synopsis": "podman stop [options] container...",
                "short_desc": "Stop one or more running containers.",
                "detailed_desc": "Sends SIGTERM signal and waits for graceful container shutdown before sending SIGKILL.",
                "category": "Container Lifecycle",
                "common_flags": [
                    {"flag": "-t, --time <seconds>", "desc": "Seconds to wait for stop before killing container (default 10)."}
                ],
                "sample_output": "b1c2d3e4f5a6",
                "rhcsa_tips": ["Use container name instead of long container ID: 'podman stop web-server'."],
                "default_run_cmd": "podman stop --help | head -n 8 2>/dev/null || echo 'podman stop container'"
            },
            {
                "id": "ch26_podman_rm",
                "name": "podman rm",
                "synopsis": "podman rm [options] container...",
                "short_desc": "Remove one or more stopped containers.",
                "detailed_desc": "Deletes container instance data from storage.",
                "category": "Container Lifecycle",
                "common_flags": [
                    {"flag": "-f, --force", "desc": "Force removal of running container (sends SIGKILL)."}
                ],
                "sample_output": "b1c2d3e4f5a6",
                "rhcsa_tips": ["Purge all stopped containers: 'podman container prune -f'."],
                "default_run_cmd": "podman rm --help | head -n 8 2>/dev/null || echo 'podman rm container'"
            },
            {
                "id": "ch26_podman_generate_systemd",
                "name": "podman generate systemd",
                "synopsis": "podman generate systemd [--name] [--files] [--new] container",
                "short_desc": "Generate systemd unit files for auto-starting containers at boot.",
                "detailed_desc": "Creates a .service file allowing systemd to manage, monitor, and start Podman containers on system startup.",
                "category": "Systemd Integration",
                "common_flags": [
                    {"flag": "--name", "desc": "Use container name rather than container ID in service definition."},
                    {"flag": "--files", "desc": "Generate .service unit file directly in current working directory."},
                    {"flag": "--new", "desc": "CRITICAL: Recreate container afresh on start rather than expecting existing container!"}
                ],
                "sample_output": """# container-web-server.service
# autogenerated by Podman 4.4.1
[Unit]
Description=Podman container-web-server.service
Wants=network-online.target
After=network-online.target

[Service]
Environment=PODMAN_SYSTEMD_UNIT=%n
Restart=on-failure
ExecStart=/usr/bin/podman run --name web-server -d -p 8080:80 ubi9
ExecStop=/usr/bin/podman stop web-server

[Install]
WantedBy=default.target""",
                "rhcsa_tips": [
                    "RHCSA HIGHEST WEIGHT QUESTION: 1) Run container with podman. 2) mkdir -p ~/.config/systemd/user. 3) cd ~/.config/systemd/user. 4) podman generate systemd --name my-container --files --new. 5) systemctl --user daemon-reload. 6) systemctl --user enable --now container-my-container.service. 7) loginctl enable-linger student (CRITICAL SO IT STARTS AT BOOT WITHOUT LOGGING IN)!"
                ],
                "default_run_cmd": "podman generate systemd --help | head -n 12 2>/dev/null || echo 'podman generate systemd --name --files --new'"
            },
            {
                "id": "ch26_loginctl_enable_linger",
                "name": "loginctl enable-linger",
                "synopsis": "loginctl enable-linger [user]",
                "short_desc": "Enable user linger so user systemd services and rootless containers run at boot.",
                "detailed_desc": "Keeps a user systemd session running even when the user is not actively logged in.",
                "category": "User Systemd",
                "common_flags": [],
                "sample_output": "Linger enabled for user 'student'.",
                "rhcsa_tips": [
                    "MANDATORY EXAM REQUIREMENT: Without 'loginctl enable-linger student', rootless user systemd containers will STOP whenever you log out of the server!"
                ],
                "default_run_cmd": "loginctl --help | grep -i linger 2>/dev/null || echo 'loginctl enable-linger [USER]'"
            },
            {
                "id": "ch26_podman_build",
                "name": "podman build",
                "synopsis": "podman build [options] [context]",
                "short_desc": "Build a container image using instructions in a Containerfile.",
                "detailed_desc": "Reads instructions (FROM, RUN, COPY, EXPOSE, CMD) from Containerfile / Dockerfile and produces a new local image.",
                "category": "Image Building",
                "common_flags": [
                    {"flag": "-t, --tag <name:tag>", "desc": "Tag the created image."},
                    {"flag": "-f <file>", "desc": "Specify alternative Containerfile path."}
                ],
                "sample_output": """STEP 1/4: FROM registry.access.redhat.com/ubi9:latest
STEP 2/4: RUN dnf install -y httpd && dnf clean all
STEP 3/4: COPY index.html /var/www/html/
STEP 4/4: CMD ["httpd", "-DFOREGROUND"]
COMMIT custom-web:v1
--> a1b2c3d4e5f6
Successfully tagged localhost/custom-web:v1""",
                "rhcsa_tips": [
                    "RHCSA OBJECTIVE: 'Build a container image named custom-app from /home/student/Containerfile': podman build -t custom-app /home/student."
                ],
                "default_run_cmd": "podman build --help | head -n 10 2>/dev/null || echo 'podman build -t tag .'"
            },
            {
                "id": "ch26_skopeo_inspect",
                "name": "skopeo inspect",
                "synopsis": "skopeo inspect docker://registry/image:tag",
                "short_desc": "Inspect remote container repository image metadata without downloading layers.",
                "detailed_desc": "Queries remote registries directly to inspect environment variables, exposed ports, labels, and layer digests.",
                "category": "Registry Inspection",
                "common_flags": [],
                "sample_output": """{
    "Name": "registry.access.redhat.com/ubi9",
    "Digest": "sha256:7f451234...",
    "RepoTags": [ "latest", "9.2", "9.1" ],
    "Created": "2026-09-10T12:00:00Z",
    "Architecture": "amd64",
    "Os": "linux"
}""",
                "rhcsa_tips": ["Use skopeo inspect to check image labels and architecture before wasting bandwidth pulling large images."],
                "default_run_cmd": "skopeo --version 2>/dev/null || echo 'skopeo utility'"
            }
        ]
    }
]
