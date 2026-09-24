"""
Catalog Service for querying chapters, commands, and metadata.
"""

from data.commands_data import (
    get_all_chapters,
    get_chapter_by_id,
    find_command_by_id,
    search_catalog,
    get_summary_stats,
    CHAPTERS
)

class CatalogService:
    @staticmethod
    def get_curriculum():
        """Retrieve full curriculum hierarchy."""
        return get_all_chapters()

    @staticmethod
    def get_chapter(chapter_id):
        """Retrieve single chapter with its 10 commands."""
        return get_chapter_by_id(chapter_id)

    @staticmethod
    def get_command_detail(command_id):
        """Retrieve specific command and its parent chapter."""
        cmd, ch = find_command_by_id(command_id)
        if not cmd:
            return None
        return {
            "command": cmd,
            "chapter_id": ch["chapter_id"],
            "chapter_title": ch["chapter_title"],
            "part_id": ch["part_id"],
            "part_title": ch["part_title"]
        }

    @staticmethod
    def search(query):
        """Search across all 260 commands."""
        return search_catalog(query)

    @staticmethod
    def get_overview_stats():
        """Return curriculum high-level metrics."""
        return get_summary_stats()
