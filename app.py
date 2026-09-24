"""
Linux Command Simulator & RHCSA 9 Learning Hub
Main Flask Application Server
"""

import os
from flask import Flask, render_template, request, jsonify
from services.catalog_service import CatalogService
from services.simulator_service import simulator_engine

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "rhcsa9-linux-sim-secret-key-2026")

@app.route("/")
def index():
    """Main Single Page Application interface."""
    chapters = CatalogService.get_curriculum()
    stats = CatalogService.get_overview_stats()
    # Default to Chapter 1
    active_chapter = CatalogService.get_chapter(1)
    return render_template(
        "index.html",
        chapters=chapters,
        stats=stats,
        active_chapter=active_chapter
    )

@app.route("/api/curriculum", methods=["GET"])
def api_curriculum():
    """Return complete 26-chapter curriculum hierarchy."""
    return jsonify({
        "status": "success",
        "data": CatalogService.get_curriculum(),
        "stats": CatalogService.get_overview_stats()
    })

@app.route("/api/chapters/<int:chapter_id>", methods=["GET"])
def api_chapter_detail(chapter_id):
    """Return specific chapter details and its 10 commands."""
    chapter = CatalogService.get_chapter(chapter_id)
    if not chapter:
        return jsonify({"status": "error", "message": f"Chapter {chapter_id} not found"}), 404
    return jsonify({
        "status": "success",
        "data": chapter
    })

@app.route("/api/commands/<command_id>", methods=["GET"])
def api_command_detail(command_id):
    """Return full details, flags, and sample output for a single command."""
    detail = CatalogService.get_command_detail(command_id)
    if not detail:
        return jsonify({"status": "error", "message": f"Command {command_id} not found"}), 404
    return jsonify({
        "status": "success",
        "data": detail
    })

@app.route("/api/search", methods=["GET"])
def api_search():
    """Search across 260 commands by keyword."""
    query = request.args.get("q", "").strip()
    results = CatalogService.search(query)
    return jsonify({
        "status": "success",
        "query": query,
        "count": len(results),
        "results": results
    })

@app.route("/api/simulate", methods=["POST"])
def api_simulate():
    """Execute a command string through the virtual simulation engine."""
    payload = request.get_json(silent=True) or {}
    raw_cmd = payload.get("command", "").strip()
    
    result = simulator_engine.execute(raw_cmd)
    return jsonify({
        "status": "success",
        "command": raw_cmd,
        "result": result
    })

@app.route("/api/stats", methods=["GET"])
def api_stats():
    """Return curriculum statistics."""
    return jsonify({
        "status": "success",
        "stats": CatalogService.get_overview_stats()
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Linux Command Simulator running on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
