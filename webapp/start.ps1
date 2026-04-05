# Home Assistant MCP - SOTA startup (backend + webapp)
# Ports: 10796 backend, 10797 frontend (per WEBAPP_PORTS 10700-10800)

$APP_PORT = 10796
$WEBAPP_PORT = 10797

function Clear-Port {
    param([int]$Port)
    $conns = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    if (-not $conns) { return $false }
    $pids = $conns | Select-Object -ExpandProperty OwningProcess -Unique
    foreach ($procId in $pids) {
        if ($procId -and $procId -ne 0) {
            try {
                Stop-Process -Id $procId -Force -ErrorAction Stop
                Write-Host "      -> PID $procId killed (port $Port)" -ForegroundColor DarkGray
            } catch {
                Write-Host "      -> PID $procId could not be killed" -ForegroundColor DarkYellow
            }
        }
    }
    Start-Sleep -Milliseconds 400
    return $true
}

Write-Host "[HA-MCP] Port safety..." -ForegroundColor Cyan
foreach ($port in @($APP_PORT, $WEBAPP_PORT)) {
    $killed = Clear-Port -Port $port
    if ($killed) { Write-Host "  Port $port cleared" -ForegroundColor Yellow }
    else { Write-Host "  Port $port clean" -ForegroundColor Green }
}

Write-Host "[HA-MCP] Syncing Python deps..." -ForegroundColor Cyan
Push-Location ..
uv sync --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] uv sync failed." -ForegroundColor Red
    exit 1
}
Pop-Location

Write-Host "[HA-MCP] Starting backend on $APP_PORT..." -ForegroundColor Green
Push-Location ..
$env:PYTHONPATH = "src"
$serverProc = Start-Process uv -ArgumentList "run", "python", "-m", "home_assistant_mcp.server", "--mode", "dual", "--port", "$APP_PORT" -NoNewWindow -PassThru
Pop-Location

if (-not (Test-Path "node_modules")) {
    Write-Host "  node_modules missing -- npm install..." -ForegroundColor Yellow
    cmd /c npm install --quiet --legacy-peer-deps
}
$dashboardProc = Start-Process cmd -ArgumentList "/c", "npm", "run", "dev" -NoNewWindow -PassThru

Write-Host ""
Write-Host "[SUCCESS] Home Assistant MCP active." -ForegroundColor Green
Write-Host "  Backend:   http://localhost:$APP_PORT  (MCP SSE + REST)"
Write-Host "  Dashboard: http://localhost:$WEBAPP_PORT"
Write-Host "  Swagger:   http://localhost:$APP_PORT/docs"
Write-Host "  Set HA_URL and HA_TOKEN for Home Assistant connection."
Write-Host "Press Ctrl+C to stop."

try {
    while ($true) { Start-Sleep -Seconds 1 }
} finally {
    Stop-Process -Id $serverProc.Id -Force -ErrorAction SilentlyContinue
    Stop-Process -Id $dashboardProc.Id -Force -ErrorAction SilentlyContinue
    Write-Host "[DONE] Cleanup complete." -ForegroundColor Green
}
