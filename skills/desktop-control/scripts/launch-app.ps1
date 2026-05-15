# Launch-App.ps1
# Generic application launcher 鈥?searches Start Menu, common paths, and direct path.

[CmdletBinding(DefaultParameterSetName = 'Help')]
param(
    [Parameter(ParameterSetName = 'ByName')]
    [string]$AppName,

    [Parameter(ParameterSetName = 'ByPath')]
    [string]$AppPath,

    [Parameter(ParameterSetName = 'List')]
    [switch]$List,

    [switch]$Wait = $false
)

# Show usage if no action specified
if ($PSCmdlet.ParameterSetName -eq 'Help') {
    Write-Host @"
Launch-App.ps1 鈥?Launch any application on Windows

Usage:
  .\launch-app.ps1 -AppName "搴旂敤鍚嶇О"     # Search and launch by name
  .\launch-app.ps1 -AppPath "C:\path\to\app.exe"  # Launch by direct path
  .\launch-app.ps1 -List                           # List known app shortcuts

Examples:
  .\launch-app.ps1 -AppName "鍝斿摡鍝斿摡"
  .\launch-app.ps1 -AppName "璁＄畻鍣?
  .\launch-app.ps1 -AppName "notepad"
  .\launch-app.ps1 -AppPath "C:\Program Files\bilibili\鍝斿摡鍝斿摡.exe"
"@
    exit 0
}

# List mode - show known apps
if ($List) {
    Write-Host "=== Known Applications ===" -ForegroundColor Cyan
    Write-Host "Use -AppName with any of these names (or part of them):" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  System:        calc, notepad, mspaint, msedge, cmd, powershell"
    Write-Host "  Browsers:      chrome, firefox, edge"
    Write-Host "  Chat:          wechat, 寰俊, qq"
    Write-Host "  Media:         bilibili, 鍝斿摡鍝斿摡, spotify"
    Write-Host "  Dev:           code, vs code, typora, obsidian"
    Write-Host "  Gaming:        steam"
    Write-Host ""
    Write-Host "For any other app, use -AppPath with the full executable path." -ForegroundColor Gray
    exit 0
}

function Launch-Process {
    param([string]$Path)
    if ($Wait) {
        Start-Process -FilePath $Path -Wait
    } else {
        Start-Process -FilePath $Path
    }
    return $true
}

# If direct path provided, use it directly
if ($AppPath) {
    if (Test-Path $AppPath) {
        Write-Host "Launching: $AppPath"
        Launch-Process -Path $AppPath
        Write-Host "Application launched successfully."
        exit 0
    } else {
        Write-Error "File not found: $AppPath"
        exit 1
    }
}

if (-not $AppName) {
    Write-Error "Specify either -AppName or -AppPath"
    exit 1
}

Write-Host "Searching for application: $AppName"

# 1. Try system commands (for built-in apps)
$systemCommands = @(
    "calc.exe", "notepad.exe", "mspaint.exe", "msedge.exe",
    "cmd.exe", "explorer.exe", "snippingtool.exe", "powershell.exe"
)

$exeName = $AppName.ToLower()
if (-not $exeName.EndsWith('.exe')) { $exeName += '.exe' }

if ($systemCommands -contains $exeName) {
    Write-Host "Launching system app: $exeName"
    Launch-Process -Path $exeName
    Write-Host "Application launched successfully."
    exit 0
}

# 2. Try common install paths
$knownApps = @{
    '鍝斿摡鍝斿摡'   = @("C:\Program Files\bilibili\鍝斿摡鍝斿摡.exe")
    'bilibili'    = @("C:\Program Files\bilibili\鍝斿摡鍝斿摡.exe")
    'chrome'      = @("$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
                       "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe")
    'firefox'     = @("$env:ProgramFiles\Mozilla Firefox\firefox.exe",
                       "${env:ProgramFiles(x86)}\Mozilla Firefox\firefox.exe")
    'code'        = @("$env:LOCALAPPDATA\Programs\Microsoft VS Code\Code.exe")
    'vs code'     = @("$env:LOCALAPPDATA\Programs\Microsoft VS Code\Code.exe")
    'spotify'     = @("$env:APPDATA\Spotify\Spotify.exe")
    ' steam'      = @("${env:ProgramFiles(x86)}\Steam\steam.exe")
    'wechat'      = @("$env:ProgramFiles\Tencent\WeChat\WeChat.exe",
                       "${env:ProgramFiles(x86)}\Tencent\WeChat\WeChat.exe")
    '寰俊'        = @("$env:ProgramFiles\Tencent\WeChat\WeChat.exe",
                       "${env:ProgramFiles(x86)}\Tencent\WeChat\WeChat.exe")
    'qq'          = @("$env:ProgramFiles\Tencent\QQ\Bin\QQ.exe",
                       "${env:ProgramFiles(x86)}\Tencent\QQ\Bin\QQ.exe")
    'typora'      = @("$env:ProgramFiles\Typora\Typora.exe")
    'obsidian'    = @("$env:LOCALAPPDATA\Obsidian\Obsidian.exe")
}

$appKey = $AppName.ToLower()
foreach ($key in $knownApps.Keys) {
    if ($appKey -eq $key -or $appKey -like "*$key*") {
        foreach ($path in $knownApps[$key]) {
            if (Test-Path $path) {
                Write-Host "Found at known path: $path"
                Launch-Process -Path $path
                Write-Host "Application launched successfully."
                exit 0
            }
        }
    }
}

# 3. Try via Get-StartApps (Start Menu database)
try {
    $startApps = Get-StartApps | Where-Object { $_.Name -like "*$AppName*" }
    if ($startApps) {
        $app = $startApps | Select-Object -First 1
        Write-Host "Found in Start Menu: $($app.Name) (AppID: $($app.AppID))"

        # Try launching via AppID using shell
        $shell = New-Object -ComObject Shell.Application
        $appsFolder = $shell.NameSpace("shell:::{4234d49b-0245-4df3-b780-3893943456e1}")
        $target = $appsFolder.Items() | Where-Object { $_.Path -eq $app.AppID } | Select-Object -First 1
        if ($target) {
            $target.InvokeVerb()
            Write-Host "Application launched successfully."
            exit 0
        }

        # Fallback: try explorer.exe shell:appsFolder\AppID
        Start-Process "shell:appsFolder\$($app.AppID)"
        Write-Host "Application launched via shell:appsFolder."
        exit 0
    }
} catch {
    Write-Warning "Start Menu search failed: $_"
}

# 4. Try via where.exe
try {
    $whereResult = where.exe "$exeName" 2>$null
    if ($whereResult) {
        $foundPath = ($whereResult | Select-Object -First 1).Trim()
        Write-Host "Found via PATH: $foundPath"
        Launch-Process -Path $foundPath
        Write-Host "Application launched successfully."
        exit 0
    }
} catch { }

Write-Error "Could not find application: $AppName"
Write-Host "Try specifying the full path with -AppPath instead."
exit 1
