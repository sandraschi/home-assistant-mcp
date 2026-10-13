# Per-repo fleet start config for home-assistant-mcp
# Edit ports/backend target here - start.ps1 is fleet-standard.
@{
    Name         = 'home-assistant-mcp'
    BackendPort  = 10835
    FrontendPort = 10834
    HealthPath   = '/api/v1/health'
    WebRoot      = 'web_sota'
    Backend = @{
        Kind          = 'uvicorn'
        UvicornTarget = 'home_assistant_mcp.server:app'
        SyncExtras    = @('dev')
        SyncOnStart  = $true
        Env           = @{ WEB_PORT = '10835' }
    }
    Frontend = @{
        Kind           = 'vite-npm'
        PackageManager = 'npm'
        PortEnvVar     = 'VITE_PORT'
        ApiTargetEnv   = 'VITE_API_TARGET'
    }
}
