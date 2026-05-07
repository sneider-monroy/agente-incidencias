"""
PASO 5: LOOP PRINCIPAL DEL AGENTE
Adaptado a sistema de incidencias de software
"""

import json
from dotenv import load_dotenv
from anthropic import Anthropic
from tools import tools
from functions import create_issue, list_issues, resolve_issue, get_statistics

# Cargar variables de entorno
load_dotenv()

# Inicializar cliente
client = Anthropic()

# ==========================================
# Ejecutar herramienta
# ==========================================
def execute_tool(tool_name, tool_input):

    if tool_name == "create_issue":
        return create_issue(
            tool_input["title"],
            tool_input.get("description", ""),
            tool_input["priority"]
        )

    elif tool_name == "list_issues":
        return list_issues(tool_input["filter"])

    elif tool_name == "resolve_issue":
        return resolve_issue(tool_input["task_id"])

    elif tool_name == "get_statistics":
        return get_statistics()

    else:
        return {"error": f"Herramienta desconocida: {tool_name}"}


# ==========================================
# LOOP PRINCIPAL DEL AGENTE
# ==========================================
def run_task_agent(user_message):

    print("\n" + "="*60)
    print("🐛 AGENTE DE INCIDENCIAS INICIADO")
    print("="*60)
    print(f"📝 Tú: {user_message}\n")

    messages = [
        {"role": "user", "content": user_message}
    ]

    continue_loop = True
    iteration = 0

    while continue_loop:
        iteration += 1
        print(f"\n--- Iteración {iteration} ---")
        print("🧠 Claude está pensando...")

        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )

        messages.append({"role": "assistant", "content": response.content})

        tool_used = False

        for block in response.content:

            if block.type == "text":
                print(f"\n💬 Claude: {block.text}")

            elif block.type == "tool_use":
                tool_used = True

                print(f"\n🔧 Claude quiere usar: {block.name}")
                print(f"   Parámetros: {json.dumps(block.input, ensure_ascii=False)}")

                result = execute_tool(block.name, block.input)

                print(f"   ✅ Resultado: {json.dumps(result, ensure_ascii=False)}\n")

                messages.append({
                    "role": "user",
                    "content": [{
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result, ensure_ascii=False)
                    }]
                })

        if not tool_used or response.stop_reason == "end_turn":
            continue_loop = False

    print("\n" + "="*60)
    print("✅ AGENTE COMPLETADO")
    print("="*60 + "\n")


# ==========================================
# MÚLTIPLES CONSULTAS
# ==========================================
def run_multiple_tasks(queries):

    for query in queries:
        run_task_agent(query)
        print("\n")


# ==========================================
# PRUEBA
# ==========================================
if __name__ == "__main__":
    run_multiple_tasks([
        "Registra un bug crítico en login",
        "Muéstrame todas las incidencias pendientes",
        "Resuelve la incidencia 1 y dame estadísticas"
    ])
