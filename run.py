"""
🚀 NASA Burro Space Explorer - Inicio Simple
Ejecutar: python run.py
"""
import sys
import os
import subprocess

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 NASA BURRO SPACE EXPLORER 🫏")
    print("=" * 60)
    print("\n📍 Iniciando servidor en http://localhost:8000")
    print("📖 Documentación API: http://localhost:8000/docs")
    print("\n⚠️  Presiona Ctrl+C para detener el servidor\n")
    print("=" * 60)
    print()

    try:
        # Ejecutar uvicorn como subproceso
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "app.main:app",
            "--host", "0.0.0.0",
            "--port", "8000"
        ])
        
    except KeyboardInterrupt:
        print("\n\n✅ Servidor detenido correctamente")
    except FileNotFoundError:
        print("\n❌ Error: uvicorn no está instalado")
        print("\nInstala las dependencias con:")
        print("   pip install -r requirements.txt")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
