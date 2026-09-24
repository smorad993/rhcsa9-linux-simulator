"""
Linux Command Simulator - Comprehensive RHCSA 9 Command Catalog
Aggregates all 26 Chapters and 260 Curated Commands across Parts I, II, III, and IV.
Based on Red Hat RHCSA 9 Cert Guide: EX200.
"""

from data.chapters_part1 import PART_1_CHAPTERS
from data.chapters_part2 import PART_2_CHAPTERS
from data.chapters_part3 import PART_3_CHAPTERS
from data.chapters_part4 import PART_4_CHAPTERS

# Master list of all 26 chapters
CHAPTERS = PART_1_CHAPTERS + PART_2_CHAPTERS + PART_3_CHAPTERS + PART_4_CHAPTERS

# Fast lookup indexes
_COMMAND_INDEX = {}
_CHAPTER_INDEX = {}

for ch in CHAPTERS:
    _CHAPTER_INDEX[ch["chapter_id"]] = ch
    for cmd in ch["commands"]:
        _COMMAND_INDEX[cmd["id"]] = (cmd, ch)

def get_all_chapters():
    """Return all 26 chapters with metadata and commands."""
    return CHAPTERS

def get_chapter_by_id(cid):
    """Retrieve chapter dictionary by numeric ID (1-26)."""
    return _CHAPTER_INDEX.get(cid)

def find_command_by_id(cmd_id):
    """Lookup command and its parent chapter by command ID slug."""
    return _COMMAND_INDEX.get(cmd_id, (None, None))

def search_catalog(query):
    """Search catalog by command name, synopsis, description, or category."""
    if not query:
        return []
    q = query.lower().strip()
    results = []
    for ch in CHAPTERS:
        for cmd in ch["commands"]:
            if (q in cmd["name"].lower() or 
                q in cmd["short_desc"].lower() or 
                q in cmd["category"].lower() or 
                q in cmd["detailed_desc"].lower() or
                q in cmd["id"].lower()):
                results.append({
                    "command": cmd,
                    "chapter_id": ch["chapter_id"],
                    "chapter_title": ch["chapter_title"],
                    "part_title": ch["part_title"]
                })
    return results

def get_summary_stats():
    """Return summary statistics of curriculum."""
    total_commands = sum(len(ch["commands"]) for ch in CHAPTERS)
    return {
        "total_chapters": len(CHAPTERS),
        "total_commands": total_commands,
        "parts": [
            {"id": 1, "title": "Part I: Performing Basic System Management Tasks", "chapters": 8},
            {"id": 2, "title": "Part II: Operating Running Systems", "chapters": 7},
            {"id": 3, "title": "Part III: Performing Advanced System Administration Tasks", "chapters": 4},
            {"id": 4, "title": "Part IV: Managing Network Services", "chapters": 7},
        ]
    }
