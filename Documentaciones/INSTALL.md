# 📦 Instalación - NASA Burro Space Explorer

## 🔧 Requisitos del Sistema

### Software Necesario
- **Python 3.8+** (Recomendado: 3.10 o superior)
- **pip** (Gestor de paquetes de Python)
- **Navegador web moderno** (Chrome, Firefox, Edge)
- **PowerShell** (Para Windows)

### Verificar Instalaciones
```powershell
# Verificar Python
python --version

# Verificar pip
pip --version

# Si no tienes Python, descarga de:
# https://www.python.org/downloads/
```

## 📥 Instalación Paso a Paso

### Método 1: Instalación Básica (Recomendado)

#### 1. Navegar al directorio del proyecto
```powershell
cd C:\Users\USER\Desktop\Grafos
```

#### 2. Instalar dependencias
```powershell
pip install -r requirements.txt
```

#### 3. Iniciar el servidor
```powershell
# Opción A: Script automático
.\start_server.ps1

# Opción B: Comando directo
python app/main.py
```

#### 4. Abrir navegador
Abrir: `http://localhost:8000`

---

### Método 2: Con Entorno Virtual (Mejor práctica)

#### 1. Crear entorno virtual
```powershell
# Crear entorno
python -m venv venv

# Activar entorno (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Si hay error de permisos, ejecutar:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 2. Instalar dependencias en el entorno
```powershell
pip install -r requirements.txt
```

#### 3. Iniciar servidor
```powershell
python app/main.py
```

#### 4. Desactivar entorno (cuando termines)
```powershell
deactivate
```

---

## 📚 Dependencias Instaladas

El archivo `requirements.txt` instala:

| Paquete | Versión | Propósito |
|---------|---------|-----------|
| fastapi | 0.104.1 | Framework web backend |
| uvicorn | 0.24.0 | Servidor ASGI |
| pydantic | 2.5.0 | Validación de datos |
| networkx | 3.2.1 | Gestión de grafos |
| python-multipart | 0.0.6 | Upload de archivos |
| jinja2 | 3.1.2 | Templates HTML |
| python-dotenv | 1.0.0 | Variables de entorno |
| pytest | 7.4.3 | Tests unitarios |

**Tamaño aproximado**: ~50 MB

---

## 🔍 Verificación de Instalación

### Test 1: Verificar importaciones
```powershell
python -c "import fastapi, uvicorn, networkx, pydantic; print('✅ Todas las dependencias instaladas')"
```

### Test 2: Ejecutar tests
```powershell
python tests/test_algorithms.py
```

### Test 3: Verificar servidor
```powershell
# Iniciar servidor
python app/main.py

# Debe mostrar:
# INFO: Started server process
# INFO: Uvicorn running on http://0.0.0.0:8000
```

---

## 🚨 Solución de Problemas

### Error: "pip no reconocido"
**Solución**: Agregar Python al PATH
```powershell
# Reinstalar Python marcando "Add to PATH"
# O agregar manualmente:
# C:\Users\USER\AppData\Local\Programs\Python\Python3XX
# C:\Users\USER\AppData\Local\Programs\Python\Python3XX\Scripts
```

### Error: "ModuleNotFoundError"
**Solución**: Reinstalar dependencias
```powershell
pip install --upgrade -r requirements.txt
```

### Error: "Address already in use"
**Solución**: El puerto 8000 está ocupado
```powershell
# Opción 1: Usar otro puerto
uvicorn app.main:app --port 8080

# Opción 2: Matar proceso en puerto 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Error: "cannot be loaded because running scripts is disabled"
**Solución**: Cambiar política de ejecución
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error: Grafo no se visualiza
**Solución**: Verificar archivos estáticos
```powershell
# Verificar que existen:
ls app/static/js/
ls app/static/css/
ls app/templates/

# Si faltan, revisar que se crearon correctamente
```

---

## 🔄 Actualización

### Actualizar dependencias
```powershell
pip install --upgrade -r requirements.txt
```

### Actualizar código
```powershell
git pull origin main
```

---

## 🗑️ Desinstalación

### Método 1: Solo dependencias
```powershell
pip uninstall -r requirements.txt -y
```

### Método 2: Completo (con entorno virtual)
```powershell
# Desactivar entorno
deactivate

# Eliminar carpeta del entorno
Remove-Item -Recurse -Force venv
```

---

## 🐳 Instalación con Docker (Opcional)

Si prefieres usar Docker:

### 1. Crear Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "app/main.py"]
```

### 2. Construir imagen
```powershell
docker build -t nasa-burro-explorer .
```

### 3. Ejecutar contenedor
```powershell
docker run -p 8000:8000 nasa-burro-explorer
```

---

## 📊 Recursos del Sistema

### Requisitos Mínimos
- **RAM**: 512 MB
- **CPU**: 1 core
- **Disco**: 200 MB
- **Red**: Localhost (no requiere internet después de instalar)

### Requisitos Recomendados
- **RAM**: 2 GB
- **CPU**: 2 cores
- **Disco**: 500 MB
- **Navegador**: Chrome/Firefox actualizado

---

## ✅ Checklist de Instalación

- [ ] Python 3.8+ instalado
- [ ] pip actualizado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Servidor inicia sin errores
- [ ] Navegador abre `http://localhost:8000`
- [ ] Interfaz carga correctamente
- [ ] JSON de ejemplo carga sin errores
- [ ] Grafo se visualiza
- [ ] Algoritmos calculan rutas
- [ ] Simulación funciona

---

## 📞 Soporte

Si encuentras problemas:

1. **Revisar logs**: Consola donde corre el servidor
2. **Consola del navegador**: F12 → Console
3. **Verificar archivos**: Que todos los archivos existan
4. **Tests**: Ejecutar `python tests/test_algorithms.py`
5. **Reinstalar**: Eliminar `venv` y reinstalar

---

## 🎓 Para Instructores/Evaluadores

### Instalación Rápida para Demo
```powershell
# 1. Abrir PowerShell en la carpeta del proyecto
cd C:\Users\USER\Desktop\Grafos

# 2. Instalar (1-2 minutos)
pip install -r requirements.txt

# 3. Ejecutar
python app/main.py

# 4. Abrir navegador
start http://localhost:8000
```

### Archivo de Demo Incluido
- `data/constellations_example.json`
- 2 constelaciones
- 15 estrellas
- 1 estrella compartida
- 2 hipergigantes

---

¡Instalación completa! 🚀
