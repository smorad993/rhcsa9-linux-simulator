/**
 * Linux Command Simulator & RHCSA 9 Hub
 * Frontend Interactive Controller
 */

document.addEventListener("DOMContentLoaded", () => {
    // State
    let currentChapterId = 1;
    let currentCommand = null;
    let commandHistory = [];
    let historyIndex = -1;
    let currentPrompt = "[root@rhel9-node1 ~]#";

    // DOM Elements
    const terminalScreen = document.getElementById("terminal-screen");
    const terminalHistoryLog = document.getElementById("terminal-history-log");
    const termInput = document.getElementById("term-input");
    const activePromptEl = document.getElementById("active-prompt");
    const clearTermBtn = document.getElementById("clear-term-btn");
    const restartTermBtn = document.getElementById("restart-term-btn");

    // Inspector Elements
    const inspectorCmdName = document.getElementById("inspector-cmd-name");
    const inspectorCategoryTag = document.getElementById("inspector-category-tag");
    const inspectorSynopsis = document.getElementById("inspector-synopsis");
    const inspectorDetailedDesc = document.getElementById("inspector-detailed-desc");
    const inspectorFlagsList = document.getElementById("inspector-flags-list");
    const inspectorTipsList = document.getElementById("inspector-tips-list");
    const inspectorOutputPreview = document.getElementById("inspector-output-preview");
    const runInSimulatorBtn = document.getElementById("run-in-simulator-btn");
    const copySynopsisBtn = document.getElementById("copy-synopsis-btn");

    // Hero Elements
    const heroPartTag = document.getElementById("hero-part-tag");
    const heroChapterPill = document.getElementById("hero-chapter-pill");
    const heroChapterTitle = document.getElementById("hero-chapter-title");
    const heroChapterDesc = document.getElementById("hero-chapter-desc");
    const commandsGrid = document.getElementById("commands-grid");

    // Search Elements
    const headerSearchInput = document.getElementById("header-search-input");
    const searchModal = document.getElementById("search-modal");
    const modalSearchInput = document.getElementById("modal-search-input");
    const modalResultsList = document.getElementById("modal-results-list");

    // =========================================================================
    // Chapter Selection & Rendering
    // =========================================================================
    window.selectChapter = async function(chapterId) {
        currentChapterId = chapterId;

        // Highlight sidebar button
        document.querySelectorAll(".chapter-item-btn").forEach(btn => {
            btn.classList.toggle("active", btn.dataset.chapterId == chapterId);
        });

        try {
            const res = await fetch(`/api/chapters/${chapterId}`);
            const data = await res.json();
            if (data.status === "success") {
                renderChapterView(data.data);
            }
        } catch (err) {
            console.error("Failed to load chapter:", err);
        }
    };

    function renderChapterView(chapter) {
        // Update hero banner
        heroPartTag.textContent = chapter.part_title;
        heroChapterPill.textContent = `Chapter ${chapter.chapter_id} of 26`;
        heroChapterTitle.textContent = chapter.chapter_title;
        heroChapterDesc.textContent = chapter.description;

        // Render Top 10 command cards
        commandsGrid.innerHTML = "";
        chapter.commands.forEach((cmd, idx) => {
            const card = document.createElement("div");
            card.className = "command-card" + (idx === 0 ? " selected" : "");
            card.dataset.cmdId = cmd.id;
            card.innerHTML = `
                <div class="cmd-card-header">
                    <span class="cmd-name">${escapeHtml(cmd.name)}</span>
                    <span class="cmd-category-tag">${escapeHtml(cmd.category)}</span>
                </div>
                <div class="cmd-short-desc">${escapeHtml(cmd.short_desc)}</div>
                <div class="cmd-card-footer">
                    <span class="cmd-click-hint">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
                        Inspect details
                    </span>
                    <span class="cmd-run-badge">▶ Run</span>
                </div>
            `;

            card.addEventListener("click", () => {
                document.querySelectorAll(".command-card").forEach(c => c.classList.remove("selected"));
                card.classList.add("selected");
                inspectCommand(cmd);
            });

            commandsGrid.appendChild(card);
        });

        // Inspect first command by default
        if (chapter.commands.length > 0) {
            inspectCommand(chapter.commands[0]);
        }
    }

    // =========================================================================
    // Command Inspection Drawer
    // =========================================================================
    function inspectCommand(cmd) {
        currentCommand = cmd;

        inspectorCmdName.textContent = cmd.name;
        inspectorCategoryTag.textContent = cmd.category;
        inspectorSynopsis.textContent = cmd.synopsis;
        inspectorDetailedDesc.textContent = cmd.detailed_desc;

        // Common Flags Table
        inspectorFlagsList.innerHTML = "";
        if (cmd.common_flags && cmd.common_flags.length > 0) {
            cmd.common_flags.forEach(f => {
                const item = document.createElement("div");
                item.className = "flag-item";
                item.innerHTML = `
                    <span class="flag-badge">${escapeHtml(f.flag)}</span>
                    <span class="flag-desc">${escapeHtml(f.desc)}</span>
                `;
                inspectorFlagsList.appendChild(item);
            });
        } else {
            inspectorFlagsList.innerHTML = `<div class="flag-desc" style="color:var(--text-muted);">Standard standalone invocation (no complex flags required).</div>`;
        }

        // RHCSA Tips Box
        inspectorTipsList.innerHTML = "";
        if (cmd.rhcsa_tips && cmd.rhcsa_tips.length > 0) {
            cmd.rhcsa_tips.forEach(tip => {
                const li = document.createElement("li");
                li.textContent = tip;
                inspectorTipsList.appendChild(li);
            });
        }

        // Output Preview
        inspectorOutputPreview.textContent = cmd.sample_output || "# No output generated";

        // Scroll inspector into view smoothly on smaller screens
        if (window.innerWidth < 1200) {
            document.querySelector(".inspector-panel").scrollIntoView({ behavior: "smooth" });
        }
    }

    // =========================================================================
    // Web Terminal Execution
    // =========================================================================
    async function executeCommand(cmdString) {
        const trimmed = cmdString.trim();
        if (!trimmed) return;

        // Add to history
        commandHistory.push(trimmed);
        historyIndex = commandHistory.length;

        // Append entry to terminal screen
        const logEntry = document.createElement("div");
        logEntry.className = "log-entry";
        logEntry.innerHTML = `
            <div class="log-command-line">
                <span class="prompt-span">${escapeHtml(currentPrompt)}</span>
                <span class="command-span">${escapeHtml(trimmed)}</span>
            </div>
            <div class="log-output-box">${escapeHtml("Executing...")}</div>
        `;
        terminalHistoryLog.appendChild(logEntry);
        terminalScreen.scrollTop = terminalScreen.scrollHeight;

        const outputBox = logEntry.querySelector(".log-output-box");

        try {
            const res = await fetch("/api/simulate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ command: trimmed })
            });
            const data = await res.json();

            if (data.status === "success") {
                const result = data.result;

                // Handle clear command
                if (result.clear) {
                    terminalHistoryLog.innerHTML = "";
                    termInput.value = "";
                    return;
                }

                // Update prompt & cwd
                if (result.prompt) {
                    currentPrompt = result.prompt;
                    activePromptEl.textContent = currentPrompt;
                }

                // Render output or errors
                if (result.stderr) {
                    outputBox.classList.add("error");
                    outputBox.textContent = result.stderr;
                } else if (result.stdout) {
                    outputBox.textContent = result.stdout;
                } else {
                    outputBox.textContent = "";
                }
            } else {
                outputBox.classList.add("error");
                outputBox.textContent = "Simulation service error";
            }
        } catch (err) {
            outputBox.classList.add("error");
            outputBox.textContent = `Execution failed: ${err.message}`;
        }

        termInput.value = "";
        terminalScreen.scrollTop = terminalScreen.scrollHeight;
    }

    // Terminal Input Listeners
    termInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            const cmd = termInput.value;
            executeCommand(cmd);
        } else if (e.key === "ArrowUp") {
            // History previous
            e.preventDefault();
            if (commandHistory.length > 0 && historyIndex > 0) {
                historyIndex--;
                termInput.value = commandHistory[historyIndex];
            }
        } else if (e.key === "ArrowDown") {
            // History next
            e.preventDefault();
            if (historyIndex < commandHistory.length - 1) {
                historyIndex++;
                termInput.value = commandHistory[historyIndex];
            } else {
                historyIndex = commandHistory.length;
                termInput.value = "";
            }
        } else if (e.key === "Tab") {
            e.preventDefault();
            // Basic auto-completion on common commands
            const val = termInput.value.toLowerCase().trim();
            const suggestions = [
                "hostnamectl status", "systemctl status", "nmcli connection show",
                "ip addr show", "firewall-cmd --list-all", "podman ps -a",
                "chronyc sources -v", "semanage port -l", "journalctl -xeu", "ls -lah"
            ];
            const match = suggestions.find(s => s.startsWith(val));
            if (match) {
                termInput.value = match;
            }
        }
    });

    // Run in Simulator Action Button
    runInSimulatorBtn.addEventListener("click", () => {
        if (currentCommand) {
            const cmdToRun = currentCommand.default_run_cmd || currentCommand.name;
            termInput.value = cmdToRun;
            termInput.focus();
            executeCommand(cmdToRun);
        }
    });

    // Clear Terminal Button
    clearTermBtn.addEventListener("click", () => {
        terminalHistoryLog.innerHTML = "";
        termInput.value = "";
        termInput.focus();
    });

    // Restart Terminal Session
    restartTermBtn.addEventListener("click", () => {
        terminalHistoryLog.innerHTML = "";
        currentPrompt = "[root@rhel9-node1 ~]#";
        activePromptEl.textContent = currentPrompt;
        termInput.value = "";
        executeCommand("clear");
    });

    // Copy Synopsis Button
    copySynopsisBtn.addEventListener("click", () => {
        if (currentCommand && currentCommand.synopsis) {
            navigator.clipboard.writeText(currentCommand.synopsis).then(() => {
                copySynopsisBtn.innerHTML = `
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>
                `;
                setTimeout(() => {
                    copySynopsisBtn.innerHTML = `
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
                    `;
                }, 1800);
            });
        }
    });

    // =========================================================================
    // Search Functionality (Header & Modal)
    // =========================================================================
    function openSearchModal(initialQuery = "") {
        searchModal.classList.add("open");
        modalSearchInput.value = initialQuery;
        modalSearchInput.focus();
        if (initialQuery) {
            performSearch(initialQuery);
        }
    }

    function closeSearchModal() {
        searchModal.classList.remove("open");
        modalSearchInput.value = "";
        modalResultsList.innerHTML = "";
    }

    headerSearchInput.addEventListener("focus", () => {
        openSearchModal(headerSearchInput.value);
        headerSearchInput.blur();
    });

    // Keyboard shortcut Ctrl+K or Cmd+K
    document.addEventListener("keydown", (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
            e.preventDefault();
            if (searchModal.classList.contains("open")) {
                closeSearchModal();
            } else {
                openSearchModal();
            }
        } else if (e.key === "Escape" && searchModal.classList.contains("open")) {
            closeSearchModal();
        }
    });

    // Close on backdrop click
    searchModal.addEventListener("click", (e) => {
        if (e.target === searchModal) {
            closeSearchModal();
        }
    });

    let searchDebounce = null;
    modalSearchInput.addEventListener("input", () => {
        clearTimeout(searchDebounce);
        searchDebounce = setTimeout(() => {
            performSearch(modalSearchInput.value);
        }, 200);
    });

    async function performSearch(query) {
        if (!query.trim()) {
            modalResultsList.innerHTML = `<div style="padding:1.5rem; text-align:center; color:var(--text-muted);">Type to search across all 260 Linux commands...</div>`;
            return;
        }

        try {
            const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
            const data = await res.json();
            modalResultsList.innerHTML = "";

            if (data.results && data.results.length > 0) {
                data.results.slice(0, 15).forEach(item => {
                    const row = document.createElement("div");
                    row.className = "search-result-item";
                    row.innerHTML = `
                        <div>
                            <div class="res-cmd-name">${escapeHtml(item.command.name)}</div>
                            <div class="res-cmd-desc">${escapeHtml(item.command.short_desc)}</div>
                        </div>
                        <div class="res-chapter-tag">Ch ${item.chapter_id}: ${escapeHtml(item.chapter_title)}</div>
                    `;
                    row.addEventListener("click", () => {
                        closeSearchModal();
                        selectChapter(item.chapter_id).then(() => {
                            // Find and select the command
                            setTimeout(() => {
                                const card = document.querySelector(`.command-card[data-cmd-id="${item.command.id}"]`);
                                if (card) card.click();
                            }, 100);
                        });
                    });
                    modalResultsList.appendChild(row);
                });
            } else {
                modalResultsList.innerHTML = `<div style="padding:1.5rem; text-align:center; color:var(--text-muted);">No matching commands found for "${escapeHtml(query)}"</div>`;
            }
        } catch (err) {
            console.error("Search failed:", err);
        }
    }

    // Helper: Escape HTML
    function escapeHtml(text) {
        if (!text) return "";
        return text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    // Initialize with Chapter 1 selected in UI
    selectChapter(1);
});
