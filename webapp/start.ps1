
# Fast port helpers (scripts/PortHelpers.ps1)
$__RepoRootForPorts = Split-Path -Parent $PSScriptRoot
$__PortHelpers = Join-Path $__RepoRootForPorts 'scripts\PortHelpers.ps1'
if (Test-Path -LiteralPath $__PortHelpers) { . $__PortHelpers }
Param([switch]$Headless)  # --- SOTA Headless Standard --- if ($Headless -and ($Host.UI.RawUI.WindowTitle -notmatch 'Hidden')) {     Start-Process pwsh -ArgumentList '-NoProfile', '-File', $PSCommandPath, '-Headless' -WindowStyle Hidden     exit } $WindowStyle = if ($Headless) { 'Hidden' } else { 'Normal' } # ------------------------------  # Home Assistant MCP - SOTA startup (backend + webapp) # Ports: 10796 backend, 10797 frontend (per WEBAPP_PORTS 10700-10800)  $APP_PORT = 10796 $WEBAPP_PORT = 10797  function Clear-Port {     param([int]$Port)     $procIds = Get-PortListenerPidsFast -Port $port
