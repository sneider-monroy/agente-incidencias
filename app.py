"""
APP.PY - Servidor Flask para sistema de incidencias
Accede a http://localhost:5000
"""

import json
from flask import Flask, render_template, request, jsonify
from database import get_all_tasks, add_task, update_task, increment_next_id, delete_task
from charts import get_all_charts
from functions import get_statistics
from datetime import datetime

from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("OPENROUTER_API_KEY")
print(f"API Key cargada: {api_key[:20] if api_key else 'NONE'}...")

client = None
try:
    from openai import OpenAI
    if api_key:
        client = OpenAI(api_key=api_key, base_url="https://opencode.ai/zen/v1")
        print("Cliente OpenAI: OK (OpenCode)")
    else:
        print("Cliente OpenAI: No hay API key")
except Exception as e:
    client = None
    print(f"Error cliente: {e}")


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
        "title": f"[{data.get('title', 'Sin titulo')}]",
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
    
    if 'deleted' in data and data['deleted']:
        if delete_task(issue_id):
            return jsonify({"status": "success", "message": f"Incidencia {issue_id} eliminada"})
        return jsonify({"status": "error", "message": f"Incidencia {issue_id} no encontrada"}), 404
    
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
# API - AGENTE IA (MINIMAX via OpenRouter)
# ==========================================

agent_tools = [
    {
        "type": "function",
        "function": {
            "name": "create_issue",
            "description": "Crear una nueva incidencia",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "priority": {"type": "string", "enum": ["Alta", "Media", "Baja"]}
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_issues",
            "description": "Listar incidencias",
            "parameters": {
                "type": "object",
                "properties": {
                    "filter": {"type": "string", "enum": ["todas", "alta", "media", "baja", "resueltas", "pendientes"]}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "resolve_issue",
            "description": "Marcar incidencia como resuelta",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer"}
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_statistics",
            "description": "Obtener estadisticas",
            "parameters": {"type": "object", "properties": {}}
        }
    }
]


def execute_tool(tool_name, tool_input):
    from functions import create_issue, list_issues, resolve_issue
    
    if tool_name == "create_issue":
        return create_issue(
            tool_input["title"],
            tool_input.get("description", ""),
            tool_input.get("priority", "Media")
        )
    elif tool_name == "list_issues":
        return list_issues(tool_input.get("filter", "todas"))
    elif tool_name == "resolve_issue":
        return resolve_issue(tool_input["task_id"])
    elif tool_name == "get_statistics":
        return get_statistics()
    else:
        return {"error": f"Herramienta desconocida: {tool_name}"}


@app.route('/api/agent/chat', methods=['POST'])
def agent_chat():
    """Chat con el agente Minimax M2.5"""
    if not client:
        return jsonify({"error": "Agente no disponible. Configura OPENROUTER_API_KEY."}), 500
    
    data = request.json
    user_message = data.get("message", "")
    
    system_prompt = """Eres un asistente de gestión de incidencias. Responde de forma clara y simple, sin usar asteriscos ni negritas. Solo texto normal."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]
    
    try:
        response = client.chat.completions.create(
            model="minimax-m2.5-free",
            messages=messages,
            max_tokens=1024,
            tools=agent_tools
        )
        
        choice = response.choices[0]
        
        if choice.finish_reason == "tool_calls" and choice.message.tool_calls:
            tool_calls = choice.message.tool_calls
            results = []
            
            for tool_call in tool_calls:
                func_name = tool_call.function.name
                func_args = json.loads(tool_call.function.arguments)
                result = execute_tool(func_name, func_args)
                results.append(f"[{func_name}]: {json.dumps(result, ensure_ascii=False)}")
                
                messages.append({
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [{
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments
                        }
                    }]
                })
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result, ensure_ascii=False)
                })
            
            second_response = client.chat.completions.create(
                model="minimax-m2.5-free",
                messages=messages,
                max_tokens=1024
            )
            
            final_text = second_response.choices[0].message.content
            return jsonify({"response": final_text})
        else:
            return jsonify({"response": choice.message.content})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
    print("SERVIDOR DE INCIDENCIAS INICIADO")
    print("="*70)
    print("\nAbre tu navegador en: http://127.0.0.1:8080")
    print("\nPara detener: Ctrl+C\n")
    print("="*70 + "\n")
    
    app.run(debug=False, host='127.0.0.1', port=8080, threaded=True)
