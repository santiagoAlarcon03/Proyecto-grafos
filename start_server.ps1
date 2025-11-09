# Script para iniciar el servidor en Windows PowerShell
Write-Host "=" -NoNewline -ForegroundColor Blue
Write-Host ("=" * 59) -ForegroundColor Blue
Write-Host "🚀 NASA BURRO SPACE EXPLORER 🫏" -ForegroundColor Cyan
Write-Host "=" -NoNewline -ForegroundColor Blue
Write-Host ("=" * 59) -ForegroundColor Blue
Write-Host ""
Write-Host "Verificando dependencias..." -ForegroundColor Yellow

# Verificar si existe un entorno virtual
if (Test-Path "venv") {
    Write-Host "✓ Activando entorno virtual..." -ForegroundColor Green
    .\venv\Scripts\Activate.ps1
} else {
    Write-Host "⚠ No se encontró entorno virtual. Usando Python global..." -ForegroundColor Yellow
}

# Verificar instalación de dependencias
Write-Host "Verificando paquetes necesarios..." -ForegroundColor Yellow
$packages = @("fastapi", "uvicorn", "networkx", "pydantic")
$missing = @()

foreach ($package in $packages) {
    $installed = pip show $package 2>$null
    if (-not $installed) {
        $missing += $package
    }
}

if ($missing.Count -gt 0) {
    Write-Host "⚠ Faltan paquetes: $($missing -join ', ')" -ForegroundColor Red
    Write-Host "Instalando dependencias..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Blue
Write-Host ("=" * 59) -ForegroundColor Blue
Write-Host "🌟 Iniciando servidor..." -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Blue
Write-Host ("=" * 59) -ForegroundColor Blue
Write-Host ""
Write-Host "📍 URL: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📖 Docs API: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow
Write-Host ""

# Iniciar servidor
python app/main.py
