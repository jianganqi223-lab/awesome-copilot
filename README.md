# 🖥️ Desktop Control — Windows PC Automation Skill for VS Code Copilot

> Control your Windows PC entirely through natural language — launch apps, move/click mouse, type text, press keys, take screenshots, scroll, drag, and automate workflows directly from VS Code Copilot Chat.

[![VS Code](https://img.shields.io/badge/VS_Code-1.96+-0098FF?logo=visualstudiocode)](https://code.visualstudio.com)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python)](https://python.org)
[![PowerShell](https://img.shields.io/badge/PowerShell-5.1+-5391FE?logo=powershell)](https://learn.microsoft.com/powershell)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## ✨ What You Can Do

| Category | Examples |
|----------|---------|
| 🚀 **Launch Apps** | "打开哔哩哔哩", "启动计算器", "打开 Chrome", "运行 WeGame" |
| 🖱️ **Mouse Control** | "点击屏幕中央", "右键单击(500,300)", "双击那个位置", "向下滚动" |
| ⌨️ **Keyboard** | "输入你好世界", "按回车键", "按 Ctrl+C 复制", "按 Alt+F4 关闭" |
| 📸 **Screenshot** | "截个屏", "截图保存到桌面" |
| 🔍 **Window Management** | "列出所有窗口", "聚焦哔哩哔哩窗口", "把记事本切换到前台" |
| 🎮 **Gaming** | "打开 WeGame 启动游戏", "全屏模式", "录制精彩片段" |

## 🚀 Quick Start

### 1. Install as a VS Code Agent Skill

Clone this repo into your workspace's `.agents/skills/` directory:

```powershell
# In your VS Code workspace root
git clone https://github.com/YOUR_USERNAME/desktop-control-skill.git .agents/skills/desktop-control
```

Or manually copy the `scripts/` folder and `SKILL.md` into:
- `.agents/skills/desktop-control/` (workspace-level), or
- `$env:USERPROFILE\.agents\skills\desktop-control\` (user-level, works across all projects)

### 2. Requirements

- **Windows OS** (uses Win32 API via `user32.dll`)
- **Python 3.x** with `ctypes` (built-in) and optionally `Pillow` for screenshots
- **PowerShell 5.1+** (ships with Windows 10/11)

### 3. Try It!

Open VS Code Copilot Chat and say:

> "帮我打开计算器"
> "把鼠标移到屏幕中央"
> "输入 Hello World"

## 📁 Repository Structure

```
desktop-control-skill/
├── SKILL.md                    # Agent skill definition (auto-loaded by Copilot)
├── README.md                   # This file
├── LICENSE                     # MIT License
├── .gitignore
├── scripts/
│   ├── desktop-control.py      # 🖱️⌨️ Mouse/keyboard automation engine (Win32 API)
│   ├── launch-app.ps1          # 🚀 Intelligent application launcher
│   └── find-window.ps1         # 🔍 Window finder/focus/mover
```

## 🛠️ How It Works

### Architecture

```
You (natural language)
  → VS Code Copilot loads this skill
    → [PowerShell] launch-app.ps1       — Searches Start Menu & common paths
    → [PowerShell] find-window.ps1      — Enumerates/focuses/manages windows
    → [Python]     desktop-control.py   — Sends Win32 API input events
```

### Technical Stack

- **Python + ctypes**: Direct Win32 API calls (`SendInput`, `EnumWindows`, `SetForegroundWindow`, etc.) — zero external Python dependencies for mouse/keyboard control
- **PowerShell**: Application discovery via Start Menu database, `where.exe`, and known-path lookup table
- **Pillow** (optional): Screen capture for screenshots

## 📖 Script Reference

### `desktop-control.py`

```powershell
python desktop-control.py click --x 500 --y 300
python desktop-control.py click --x 500 --y 300 --button right --double
python desktop-control.py move --x 960 --y 540
python desktop-control.py scroll --clicks -3          # negative = scroll down
python desktop-control.py drag --x1 200 --y1 200 --x2 600 --y2 400
python desktop-control.py type --text "你好世界"
python desktop-control.py key --key enter
python desktop-control.py hotkey --keys "ctrl+c"      # Ctrl+C to copy
python desktop-control.py hotkey --keys "alt+f4"      # Close window
python desktop-control.py hotkey --keys "win+d"       # Show desktop
python desktop-control.py pos                          # Get cursor position
python desktop-control.py screenshot                   # Take screenshot
python desktop-control.py windows                      # List all windows
python desktop-control.py focus --title "记事本"        # Focus window
python desktop-control.py wait --seconds 3
```

### `launch-app.ps1`

```powershell
.\launch-app.ps1 -AppName "哔哩哔哩"          # Search by name
.\launch-app.ps1 -AppPath "C:\path\to\app.exe"  # Launch by direct path
.\launch-app.ps1 -List                           # Show known apps
```

### `find-window.ps1`

```powershell
.\find-window.ps1 -List                         # List all visible windows
.\find-window.ps1 -Focus "哔哩哔哩"              # Focus a window
.\find-window.ps1 -Move -X 0 -Y 0 -Width 800 -Height 600  # Move/resize
```

## 🌟 Example Workflows

### 🎬 Open Bilibili and Play a Video

```powershell
# 1. Launch Bilibili
.\launch-app.ps1 -AppName "哔哩哔哩"

# 2. Wait for app to load
python desktop-control.py wait --seconds 4

# 3. Click search bar, type, and search
python desktop-control.py click --x 400 --y 100
python desktop-control.py type --text "AI 编程教学"
python desktop-control.py key --key enter

# 4. Click first video and go fullscreen
python desktop-control.py wait --seconds 2
python desktop-control.py click --x 500 --y 300
python desktop-control.py key --key f
```

### 📝 Open Notepad, Type, and Save

```powershell
.\launch-app.ps1 -AppName "notepad"
python desktop-control.py wait --seconds 2
python desktop-control.py type --text "Hello from AI!"
python desktop-control.py hotkey --keys "ctrl+s"
python desktop-control.py wait --seconds 1
python desktop-control.py type --text "test.txt"
python desktop-control.py key --key enter
```

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Add more app entries to `launch-app.ps1`'s known-apps database
- Improve the Python automation engine
- Add support for more complex workflows
- Translate the skill description for other languages

## 📄 License

[MIT](LICENSE) — feel free to use, modify, and share.

## 🙏 Credits

Built as a [VS Code Agent Skill](https://code.visualstudio.com/docs/copilot/customization/agent-skills) for the [DeepSeek V4 for Copilot](https://github.com) extension.
