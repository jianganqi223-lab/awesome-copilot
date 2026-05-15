---
name: desktop-control
description: 'Control your Windows PC with natural language 鈥?launch apps, move/click mouse, type text, press keys, take screenshots, scroll, drag, and automate workflows. Use when: user says "甯垜鎵撳紑XX", "鐐瑰嚮XX", "杈撳叆XX", "鎸塜X閿?, "绉诲姩榧犳爣", "鎴睆", "鎿嶄綔鐢佃剳", "鎺у埗妗岄潰", "鎵撳紑璁＄畻鍣?娴忚鍣?搴旂敤", "鎾斁瑙嗛", "鍝斿摡鍝斿摡", "鍏ㄥ睆", "澶嶅埗绮樿创".'
argument-hint: '瑕佹墽琛岀殑妗岄潰鎿嶄綔锛屽 "鎵撳紑璁＄畻鍣?銆?鐐瑰嚮鍧愭爣(500,300)"銆?杈撳叆浣犲ソ"'
---

# Desktop Control 鈥?Windows PC Automation

Control your Windows PC entirely through natural language. This skill uses:
- **PowerShell** 鈥?Launch apps, run system commands, manage windows
- **Python + Windows API (ctypes)** 鈥?Mouse/keyboard automation (no extra dependencies needed)
- **Pillow** 鈥?Screenshots for screen analysis

## Architecture

```
You (natural language)
  鈫?Agent loads this skill
    鈫?[PowerShell] ./scripts/launch-app.ps1       鈥?Launch any application
    鈫?[PowerShell] ./scripts/find-window.ps1      鈥?Find and focus windows
    鈫?[Python]     ./scripts/desktop-control.py   鈥?Mouse, keyboard, screenshot, scroll, drag
```

## Requirements

- Windows OS
- Python 3.x with `ctypes` (built-in) and optionally `Pillow` (for screenshots)
- PowerShell 5.1+

## Available Scripts

| Script | Purpose |
|--------|---------|
| `./scripts/launch-app.ps1` | Launch any installed app by name or path |
| `./scripts/find-window.ps1` | Find, focus, or list windows by title |
| `./scripts/desktop-control.py` | Full mouse/keyboard automation engine |

## Quick Reference 鈥?Common Operations

### 馃殌 Launch an App
```powershell
# By name (searches Start Menu + common paths)
& ".\scripts\launch-app.ps1" -AppName "璁＄畻鍣?
& ".\scripts\launch-app.ps1" -AppName "鍝斿摡鍝斿摡"
& ".\scripts\launch-app.ps1" -AppName "notepad"

# By direct path
& ".\scripts\launch-app.ps1" -AppPath "C:\Program Files\bilibili\鍝斿摡鍝斿摡.exe"
```

### 馃柋锔?Mouse Control
```powershell
# Move mouse to position
python scripts/desktop-control.py move --x 960 --y 540

# Click at position
python scripts/desktop-control.py click --x 500 --y 300
python scripts/desktop-control.py click --x 500 --y 300 --button right
python scripts/desktop-control.py click --x 500 --y 300 --double

# Scroll
python scripts/desktop-control.py scroll --clicks -3    # Scroll down
python scripts/desktop-control.py scroll --clicks 3     # Scroll up

# Drag from one point to another
python scripts/desktop-control.py drag --x1 200 --y1 200 --x2 600 --y2 400

# Get current position
python scripts/desktop-control.py pos
```

### 鈱笍 Keyboard Control
```powershell
# Type text
python scripts/desktop-control.py type --text "浣犲ソ涓栫晫"

# Press a key
python scripts/desktop-control.py key --key enter
python scripts/desktop-control.py key --key escape
python scripts/desktop-control.py key --key space

# Keyboard shortcuts (use + for combination)
python scripts/desktop-control.py hotkey --keys "ctrl+c"    # Copy
python scripts/desktop-control.py hotkey --keys "ctrl+v"    # Paste
python scripts/desktop-control.py hotkey --keys "alt+f4"    # Close window
python scripts/desktop-control.py hotkey --keys "win+d"     # Show desktop
python scripts/desktop-control.py hotkey --keys "win+2"     # Taskbar item 2
```

### 馃摳 Screenshot
```powershell
python scripts/desktop-control.py screenshot
python scripts/desktop-control.py screenshot --output "D:\screenshots\screen.png"
```

### 鈴憋笍 Wait
```powershell
python scripts/desktop-control.py wait --seconds 3
```

## Complete Workflow Examples

### Example 1: Open Bilibili and Search a Video
```powershell
# 1. Launch Bilibili
& ".\scripts\launch-app.ps1" -AppName "鍝斿摡鍝斿摡"

# 2. Wait for app to load
python scripts/desktop-control.py wait --seconds 4

# 3. Click search bar (top center of window, adjust as needed)
python scripts/desktop-control.py click --x 400 --y 100

# 4. Type search query
python scripts/desktop-control.py type --text "AI 缂栫▼鏁欏"

# 5. Press Enter
python scripts/desktop-control.py key --key enter

# 6. Wait for results, click first video
python scripts/desktop-control.py wait --seconds 2
python scripts/desktop-control.py click --x 500 --y 300

# 7. Toggle fullscreen (press F)
python scripts/desktop-control.py wait --seconds 1
python scripts/desktop-control.py key --key f
```

### Example 2: Open Notepad, Type, Save
```powershell
# 1. Open Notepad
& ".\scripts\launch-app.ps1" -AppName "notepad"
python scripts/desktop-control.py wait --seconds 2

# 2. Type some text
python scripts/desktop-control.py type --text "Hello, this is typed by AI!"

# 3. Save (Ctrl+S)
python scripts/desktop-control.py hotkey --keys "ctrl+s"
python scripts/desktop-control.py wait --seconds 1
python scripts/desktop-control.py type --text "test.txt"
python scripts/desktop-control.py key --key enter
```

### Example 3: Find and Focus a Window
```powershell
# 1. List all visible windows
python scripts/desktop-control.py windows

# 2. Focus a specific window by title (partial match)
python scripts/desktop-control.py focus --title "鍝斿摡鍝斿摡"
```

## Application Launch Database

Common app names and their install paths (auto-detected by `launch-app.ps1`):

| App Name | Typical Path |
|----------|-------------|
| 鍝斿摡鍝斿摡 | `C:\Program Files\bilibili\鍝斿摡鍝斿摡.exe` |
| 璁＄畻鍣?| `calc.exe` (system) |
| 璁颁簨鏈?| `notepad.exe` (system) |
| 鐢诲浘 | `mspaint.exe` (system) |
| Chrome | Various install locations |
| Edge | `msedge.exe` (system) |

## Troubleshooting

- **Click misses target**: Screen resolution or window position may differ. Use `pos` to find correct coordinates first
- **App not found**: Try specifying full path with `-AppPath`
- **Python not found**: Ensure Python is in PATH or use the venv Python
- **Permission issues**: Some operations may need administrator terminal
- **Coordinates wrong**: For 1920x1080 screens, coordinates are direct pixel positions. For other resolutions, adjust proportionally
