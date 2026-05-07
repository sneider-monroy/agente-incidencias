#!/usr/bin/env python3
"""
AGENTE DE INCIDENCIAS INTELIGENTE CON CLAUDE
Interfaz interactiva - Conversación continua
"""

from agent import run_task_agent

def main():
    """
    Interfaz interactiva principal
    """
    
    print("\n")
    print("="*70)
    print("🐛 AGENTE INTELIGENTE DE INCIDENCIAS CON CLAUDE 🐛")
    print("="*70)
    print("\n💾 Tus incidencias se guardan automáticamente en 'incidencias.json'\n")
    print("Escribe tus comandos naturales:")
    print("  • 'Registrar incidencia: error en login' - Crear un bug")
    print("  • 'Listar incidencias' - Ver todas")
    print("  • 'Incidencias de alta prioridad' - Filtrar")
    print("  • 'Resolver incidencia 1' - Marcar como resuelta")
    print("  • 'Estadísticas' - Ver progreso")
    print("  • 'salir' o 'quit' - Terminar\n")
    print("="*70 + "\n")
    
    # Loop de conversación continua
    while True:
        try:
            user_input = input("💬 Tú: ").strip()
            
            if not user_input:
                print("❌ Escribe algo\n")
                continue
            
            if user_input.lower() in ["salir", "quit", "exit", "bye"]:
                print("\n👋 ¡Hasta luego! Tus incidencias se guardaron.\n")
                break
            
            print()
            run_task_agent(user_input)
            print()
        
        except KeyboardInterrupt:
            print("\n\n👋 Interrumpido. ¡Hasta luego!\n")
            break
        
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("   Intenta de nuevo\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        print("\n💡 Asegúrate de que:")
        print("   1. Instalaste dependencias:")
        print("      python -m pip install anthropic python-dotenv")
        print("   2. Configuraste tu API KEY:")
        print("      ANTHROPIC_API_KEY")
        print("   3. Tienes internet\n")
