"""
APP.PY - Servidor Flask para sistema de incidencias
Accede a http://localhost:5000
"""

from flask import Flask, render_template, request, jsonify
from database import get_all_tasks, add_task, update_task, increment_next_id
from charts import get_all_charts
from functions import get_statistics
from datetime import datetime

app = Flask(__name__)

# ==========================================
# RUTAS PRINCIPALES
# ==========================================

@app.route('/')
def index():
    """Página principal"""
    issues = get_all_tasks()
    stats = get_statistics()
    charts = get_all_charts()
    
    return render_template('index.html', 
                         tasks=issues, 
                         stats=stats, 
                         charts=charts)


# ==========================================
# API - INCIDENCIAS
# ==========================================

@app.route('/api/issues', methods=['GET'])
def get_issues():
    """Obtener todas las incidencias"""
    return jsonify(get_all_tasks())


@app.route('/api/issues', methods=['POST'])
def create_issue_api():
    """Crear nueva incidencia"""
    data = request.json
    
    issue_id = increment_next_id()
    new_issue = {
        "id": issue_id,
        "title": f"🐛 {data.get('title', 'Sin título')}",
        "description": data.get('description', ''),
        "priority": data.get('priority', 'Media'),
        "completed": False,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    add_task(new_issue)
    return jsonify({"status": "success", "issue": new_issue}), 201


@app.route('/api/issues/<int:issue_id>', methods=['PUT'])
def update_issue(issue_id):
    """Actualizar incidencia"""
    data = request.json
    
    if update_task(issue_id, data):
        return jsonify({"status": "success", "message": f"Incidencia {issue_id} actualizada"})
    else:
        return jsonify({"status": "error", "message": f"Incidencia {issue_id} no encontrada"}), 404


@app.route('/api/issues/<int:issue_id>/resolve', methods=['PUT'])
def resolve_issue(issue_id):
    """Marcar incidencia como resuelta"""
    if update_task(issue_id, {"completed": True}):
        return jsonify({"status": "success", "message": f"Incidencia {issue_id} resuelta"})
    else:
        return jsonify({"status": "error", "message": f"Incidencia {issue_id} no encontrada"}), 404


# ==========================================
# API - ESTADÍSTICAS
# ==========================================

@app.route('/api/statistics', methods=['GET'])
def get_stats():
    """Obtener estadísticas"""
    return jsonify(get_statistics())


@app.route('/api/charts', methods=['GET'])
def get_charts():
    """Obtener gráficos"""
    return jsonify(get_all_charts())


# ==========================================
# ERRORES
# ==========================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "No encontrado"}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Error interno del servidor"}), 500


# ==========================================
# MAIN
# ==========================================

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🚀 SERVIDOR DE INCIDENCIAS INICIADO")
    print("="*70)
    print("\n📱 Abre tu navegador en: http://localhost:5000")
    print("\n⌨️  Para detener: Ctrl+C\n")
    print("="*70 + "\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
