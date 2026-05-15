# Find-Window.ps1
# Find, focus, list, or move windows by title.

param(
    [Parameter(ParameterSetName = 'Focus')]
    [string]$Focus,

    [Parameter(ParameterSetName = 'List')]
    [switch]$List,

    [Parameter(ParameterSetName = 'Move')]
    [switch]$Move,

    [Parameter(ParameterSetName = 'Move')]
    [int]$X = 0,

    [Parameter(ParameterSetName = 'Move')]
    [int]$Y = 0,

    [Parameter(ParameterSetName = 'Move')]
    [int]$Width = 800,

    [Parameter(ParameterSetName = 'Move')]
    [int]$Height = 600
)

Add-Type @"
using System;
using System.Runtime.InteropServices;
using System.Text;

public class WindowHelper {
    [DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]
    public static extern int GetWindowText(IntPtr hWnd, StringBuilder lpString, int nMaxCount);

    [DllImport("user32.dll")]
    public static extern bool IsWindowVisible(IntPtr hWnd);

    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();

    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);

    [DllImport("user32.dll")]
    public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);

    [DllImport("user32.dll")]
    public static extern bool MoveWindow(IntPtr hWnd, int X, int Y, int nWidth, int nHeight, bool bRepaint);

    [DllImport("user32.dll")]
    public static extern bool EnumWindows(EnumWindowsProc enumProc, IntPtr lParam);

    public delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr lParam);

    public static IntPtr FindWindowByTitle(string titleMatch) {
        IntPtr found = IntPtr.Zero;
        EnumWindows((hWnd, lParam) => {
            if (IsWindowVisible(hWnd)) {
                StringBuilder sb = new StringBuilder(256);
                GetWindowText(hWnd, sb, sb.Capacity);
                if (sb.ToString().IndexOf(titleMatch, StringComparison.OrdinalIgnoreCase) >= 0) {
                    found = hWnd;
                    return false;
                }
            }
            return true;
        }, IntPtr.Zero);
        return found;
    }

    public static string[] ListVisibleWindows() {
        var windows = new System.Collections.Generic.List<string>();
        EnumWindows((hWnd, lParam) => {
            if (IsWindowVisible(hWnd)) {
                StringBuilder sb = new StringBuilder(256);
                GetWindowText(hWnd, sb, sb.Capacity);
                string title = sb.ToString().Trim();
                if (title.Length > 0) {
                    windows.Add($"0x{hWnd:X8} - {title}");
                }
            }
            return true;
        }, IntPtr.Zero);
        return windows.ToArray();
    }
}
"@

switch ($PSCmdlet.ParameterSetName) {
    'List' {
        Write-Host "=== Visible Windows ===" -ForegroundColor Cyan
        $windows = [WindowHelper]::ListVisibleWindows()
        foreach ($w in $windows) {
            Write-Host "  $w"
        }
        Write-Host "=== Total: $($windows.Count) windows ===" -ForegroundColor Cyan
    }

    'Focus' {
        Write-Host "Searching for window: $Focus" -ForegroundColor Yellow
        $hwnd = [WindowHelper]::FindWindowByTitle($Focus)
        if ($hwnd -ne [IntPtr]::Zero) {
            # Restore if minimized
            [WindowHelper]::ShowWindow($hwnd, 9)  # SW_RESTORE
            Start-Sleep -Milliseconds 200
            [WindowHelper]::SetForegroundWindow($hwnd)
            Write-Host "Focused window: $Focus (0x$($hwnd.ToString('X8')))" -ForegroundColor Green
        } else {
            Write-Error "No window found matching: $Focus"
        }
    }

    'Move' {
        Write-Host "Searching for window to resize..." -ForegroundColor Yellow
        # If Focus not specified, use foreground window
        if (-not $Focus) {
            $hwnd = [WindowHelper]::GetForegroundWindow()
            Write-Host "Using foreground window: 0x$($hwnd.ToString('X8'))" -ForegroundColor Gray
        } else {
            $hwnd = [WindowHelper]::FindWindowByTitle($Focus)
        }

        if ($hwnd -ne [IntPtr]::Zero) {
            [WindowHelper]::MoveWindow($hwnd, $X, $Y, $Width, $Height, $true)
            Write-Host "Window moved to ($X, $Y) size ${Width}x${Height}" -ForegroundColor Green
        } else {
            Write-Error "No window found to move."
        }
    }

    default {
        # If Focus is provided without -Focus flag, treat as focus
        if ($Focus) {
            Write-Host "Searching for window: $Focus" -ForegroundColor Yellow
            $hwnd = [WindowHelper]::FindWindowByTitle($Focus)
            if ($hwnd -ne [IntPtr]::Zero) {
                [WindowHelper]::ShowWindow($hwnd, 9)
                Start-Sleep -Milliseconds 200
                [WindowHelper]::SetForegroundWindow($hwnd)
                Write-Host "Focused window: $Focus" -ForegroundColor Green
            } else {
                Write-Error "No window found matching: $Focus"
            }
        } else {
            Write-Host @"
Usage:
  .\find-window.ps1 -List                    # List all visible windows
  .\find-window.ps1 -Focus "绐楀彛鏍囬"         # Focus a window by title
  .\find-window.ps1 -Move -X 0 -Y 0 -Width 800 -Height 600   # Move/resize window
"@
        }
    }
}
