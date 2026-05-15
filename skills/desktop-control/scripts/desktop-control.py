"""
Desktop Control 鈥?Windows PC Automation
Mouse/keyboard automation via Windows API (user32.dll)
Supports: click, move, type, key, scroll, drag, hotkey, screenshot, window focus

Usage:
    python desktop-control.py click --x 500 --y 300
    python desktop-control.py move --x 960 --y 540
    python desktop-control.py type --text "浣犲ソ涓栫晫"
    python desktop-control.py key --key enter
    python desktop-control.py hotkey --keys "ctrl+c"
    python desktop-control.py scroll --clicks -3
    python desktop-control.py drag --x1 200 --y1 200 --x2 600 --y2 400
    python desktop-control.py pos
    python desktop-control.py screenshot
    python desktop-control.py windows
    python desktop-control.py focus --title "璁颁簨鏈?
    python desktop-control.py wait --seconds 3
"""

import argparse
import ctypes
import ctypes.wintypes
import time
import sys

# Windows API constants
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_WHEEL = 0x0800

KEYEVENTF_KEYDOWN = 0x0000
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008

INPUT_MOUSE = 0
INPUT_KEYBOARD = 1

# VK codes for common keys
VK_MAP = {
    'enter': 0x0D,
    'return': 0x0D,
    'space': 0x20,
    'spacebar': 0x20,
    'tab': 0x09,
    'escape': 0x1B,
    'esc': 0x1B,
    'backspace': 0x08,
    'delete': 0x2E,
    'up': 0x26,
    'down': 0x28,
    'left': 0x25,
    'right': 0x27,
    'home': 0x24,
    'end': 0x23,
    'pageup': 0x21,
    'pagedown': 0x22,
    'f': 0x46,       # Fullscreen toggle in many players
    'f11': 0x7A,
    'f5': 0x74,
    'ctrl': 0x11,
    'shift': 0x10,
    'alt': 0x12,
    'a': 0x41,
    'b': 0x42,
    'c': 0x43,
    'd': 0x44,
    'e': 0x45,
    'f': 0x46,
    'g': 0x47,
    'h': 0x48,
    'i': 0x49,
    'j': 0x4A,
    'k': 0x4B,
    'l': 0x4C,
    'm': 0x4D,
    'n': 0x4E,
    'o': 0x4F,
    'p': 0x50,
    'q': 0x51,
    'r': 0x52,
    's': 0x53,
    't': 0x54,
    'u': 0x55,
    'v': 0x56,
    'w': 0x57,
    'x': 0x58,
    'y': 0x59,
    'z': 0x5A,
    '0': 0x30,
    '1': 0x31,
    '2': 0x32,
    '3': 0x33,
    '4': 0x34,
    '5': 0x35,
    '6': 0x36,
    '7': 0x37,
    '8': 0x38,
    '9': 0x39,
}

# Load user32.dll
user32 = ctypes.windll.user32


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.wintypes.LONG),
        ("dy", ctypes.wintypes.LONG),
        ("mouseData", ctypes.wintypes.DWORD),
        ("dwFlags", ctypes.wintypes.DWORD),
        ("time", ctypes.wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
    ]


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.wintypes.WORD),
        ("wScan", ctypes.wintypes.WORD),
        ("dwFlags", ctypes.wintypes.DWORD),
        ("time", ctypes.wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
    ]


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg", ctypes.wintypes.DWORD),
        ("wParamL", ctypes.wintypes.WORD),
        ("wParamH", ctypes.wintypes.WORD),
    ]


class INPUT_UNION(ctypes.Union):
    _fields_ = [
        ("mi", MOUSEINPUT),
        ("ki", KEYBDINPUT),
        ("hi", HARDWAREINPUT),
    ]


class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.wintypes.DWORD),
        ("union", INPUT_UNION),
    ]


def get_screen_size():
    """Get screen dimensions."""
    width = user32.GetSystemMetrics(0)
    height = user32.GetSystemMetrics(1)
    return width, height


def get_cursor_pos():
    """Get current cursor position."""
    point = ctypes.wintypes.POINT()
    user32.GetCursorPos(ctypes.byref(point))
    return point.x, point.y


def move_mouse_absolute(x, y):
    """Move mouse to absolute screen coordinates."""
    screen_w, screen_h = get_screen_size()
    # Convert to normalized absolute coordinates (0-65535)
    norm_x = int(x * 65535 / screen_w)
    norm_y = int(y * 65535 / screen_h)

    inp = INPUT()
    inp.type = INPUT_MOUSE
    inp.union.mi.dx = norm_x
    inp.union.mi.dy = norm_y
    inp.union.mi.dwFlags = MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE
    inp.union.mi.time = 0
    inp.union.mi.dwExtraInfo = ctypes.pointer(ctypes.c_ulong(0))

    user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))


def click_mouse(x=None, y=None, button='left'):
    """Click at specified coordinates or current position."""
    if x is not None and y is not None:
        move_mouse_absolute(x, y)
        time.sleep(0.1)

    if button == 'left':
        down_flag = MOUSEEVENTF_LEFTDOWN
        up_flag = MOUSEEVENTF_LEFTUP
    elif button == 'right':
        down_flag = MOUSEEVENTF_RIGHTDOWN
        up_flag = MOUSEEVENTF_RIGHTUP
    elif button == 'middle':
        down_flag = MOUSEEVENTF_MIDDLEDOWN
        up_flag = MOUSEEVENTF_MIDDLEUP
    else:
        raise ValueError(f"Unknown button: {button}")

    # Mouse down
    inp = INPUT()
    inp.type = INPUT_MOUSE
    inp.union.mi.dwFlags = down_flag
    inp.union.mi.time = 0
    user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))

    time.sleep(0.05)

    # Mouse up
    inp2 = INPUT()
    inp2.type = INPUT_MOUSE
    inp2.union.mi.dwFlags = up_flag
    inp2.union.mi.time = 0
    user32.SendInput(1, ctypes.byref(inp2), ctypes.sizeof(inp2))


def double_click(x=None, y=None):
    """Double-click at specified coordinates."""
    if x is not None and y is not None:
        move_mouse_absolute(x, y)
        time.sleep(0.1)

    for _ in range(2):
        click_mouse(button='left')
        time.sleep(0.05)


def press_key(vk_code):
    """Press and release a key by virtual key code."""
    # Key down
    inp = INPUT()
    inp.type = INPUT_KEYBOARD
    inp.union.ki.wVk = vk_code
    inp.union.ki.wScan = 0
    inp.union.ki.dwFlags = KEYEVENTF_KEYDOWN
    inp.union.ki.time = 0
    inp.union.ki.dwExtraInfo = ctypes.pointer(ctypes.c_ulong(0))
    user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))

    time.sleep(0.05)

    # Key up
    inp2 = INPUT()
    inp2.type = INPUT_KEYBOARD
    inp2.union.ki.wVk = vk_code
    inp2.union.ki.wScan = 0
    inp2.union.ki.dwFlags = KEYEVENTF_KEYUP
    inp2.union.ki.time = 0
    inp2.union.ki.dwExtraInfo = ctypes.pointer(ctypes.c_ulong(0))
    user32.SendInput(1, ctypes.byref(inp2), ctypes.sizeof(inp2))


def type_text(text, interval=0.05):
    """Type text by sending key events for each character."""
    for char in text:
        if char.isupper() or char in '~!@#$%^&*()_+{}|:"<>?':
            # Shift + key for uppercase/symbols
            vk = VK_MAP.get('shift', 0x10)
            inp = INPUT()
            inp.type = INPUT_KEYBOARD
            inp.union.ki.wVk = vk
            inp.union.ki.dwFlags = KEYEVENTF_KEYDOWN
            user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))

            char_lower = char.lower()
            if char_lower in VK_MAP:
                press_key(VK_MAP[char_lower])

            inp2 = INPUT()
            inp2.type = INPUT_KEYBOARD
            inp2.union.ki.wVk = vk
            inp2.union.ki.dwFlags = KEYEVENTF_KEYUP
            user32.SendInput(1, ctypes.byref(inp2), ctypes.sizeof(inp2))
        else:
            char_lower = char.lower()
            if char_lower in VK_MAP:
                press_key(VK_MAP[char_lower])
            elif char == ' ':
                press_key(VK_MAP['space'])
        time.sleep(interval)


def take_screenshot(filepath=None):
    """Take a screenshot using Pillow."""
    try:
        from PIL import ImageGrab
    except ImportError:
        print("Pillow (PIL) is required for screenshots. Install with: pip install pillow")
        sys.exit(1)

    if filepath is None:
        filepath = f"desktop_screenshot_{int(time.time())}.png"

    screenshot = ImageGrab.grab()
    screenshot.save(filepath)
    print(f"Screenshot saved to: {filepath}")
    return filepath


def scroll_mouse(clicks):
    """Scroll mouse wheel. Negative = scroll down, Positive = scroll up."""
    inp = INPUT()
    inp.type = INPUT_MOUSE
    inp.union.mi.dwFlags = MOUSEEVENTF_WHEEL
    inp.union.mi.mouseData = ctypes.wintypes.DWORD(clicks * 120)  # 120 = one scroll notch
    inp.union.mi.time = 0
    user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))


def drag_mouse(x1, y1, x2, y2, button='left'):
    """Drag from (x1,y1) to (x2,y2)."""
    # Move to start
    move_mouse_absolute(x1, y1)
    time.sleep(0.1)

    # Mouse down
    btn_down = MOUSEEVENTF_LEFTDOWN if button == 'left' else MOUSEEVENTF_RIGHTDOWN
    inp = INPUT()
    inp.type = INPUT_MOUSE
    inp.union.mi.dwFlags = btn_down
    inp.union.mi.time = 0
    user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))
    time.sleep(0.1)

    # Move to end (in steps for smooth drag)
    steps = 20
    screen_w, screen_h = get_screen_size()
    for i in range(1, steps + 1):
        x = x1 + (x2 - x1) * i // steps
        y = y1 + (y2 - y1) * i // steps
        norm_x = int(x * 65535 / screen_w)
        norm_y = int(y * 65535 / screen_h)
        inp2 = INPUT()
        inp2.type = INPUT_MOUSE
        inp2.union.mi.dx = norm_x
        inp2.union.mi.dy = norm_y
        inp2.union.mi.dwFlags = MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE
        inp2.union.mi.time = 0
        user32.SendInput(1, ctypes.byref(inp2), ctypes.sizeof(inp2))
        time.sleep(0.01)

    time.sleep(0.1)

    # Mouse up
    btn_up = MOUSEEVENTF_LEFTUP if button == 'left' else MOUSEEVENTF_RIGHTUP
    inp3 = INPUT()
    inp3.type = INPUT_MOUSE
    inp3.union.mi.dwFlags = btn_up
    inp3.union.mi.time = 0
    user32.SendInput(1, ctypes.byref(inp3), ctypes.sizeof(inp3))


def press_hotkey(combination):
    """Press a key combination like 'ctrl+c', 'alt+f4', 'win+d'."""
    parts = combination.lower().split('+')
    mod_map = {
        'ctrl': 0x11, 'control': 0x11,
        'alt': 0x12,
        'shift': 0x10,
        'win': 0x5B, 'windows': 0x5B, 'cmd': 0x5B,
    }

    # Collect modifier keys and main key
    mod_keys = []
    main_key = None
    for part in parts:
        if part in mod_map:
            mod_keys.append(mod_map[part])
        else:
            main_key = part

    # Press all modifiers down
    for vk in mod_keys:
        inp = INPUT()
        inp.type = INPUT_KEYBOARD
        inp.union.ki.wVk = vk
        inp.union.ki.dwFlags = KEYEVENTF_KEYDOWN
        inp.union.ki.time = 0
        user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))
    time.sleep(0.05)

    # Press main key
    if main_key:
        if main_key in VK_MAP:
            press_key(VK_MAP[main_key])
        else:
            print(f"Unknown key in combination: {main_key}")
            # Still release modifiers
            for vk in mod_keys:
                inp = INPUT()
                inp.type = INPUT_KEYBOARD
                inp.union.ki.wVk = vk
                inp.union.ki.dwFlags = KEYEVENTF_KEYUP
                inp.union.ki.time = 0
                user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))
            return

    # Release all modifiers
    for vk in mod_keys:
        inp = INPUT()
        inp.type = INPUT_KEYBOARD
        inp.union.ki.wVk = vk
        inp.union.ki.dwFlags = KEYEVENTF_KEYUP
        inp.union.ki.time = 0
        user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))


def list_windows():
    """List all visible top-level windows."""
    EnumWindows = user32.EnumWindows
    GetWindowText = user32.GetWindowTextW
    IsWindowVisible = user32.IsWindowVisible

    windows_list = []

    def foreach_window(hwnd, lParam):
        if IsWindowVisible(hwnd):
            buf = ctypes.create_unicode_buffer(255)
            GetWindowText(hwnd, buf, 255)
            title = buf.value
            if title and title.strip():
                windows_list.append((hwnd, title))
        return True

    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    EnumWindows(WNDENUMPROC(foreach_window), 0)

    return windows_list


def focus_window(title_match):
    """Find and focus a window by partial title match."""
    EnumWindows = user32.EnumWindows
    GetWindowText = user32.GetWindowTextW
    IsWindowVisible = user32.IsWindowVisible
    ShowWindow = user32.ShowWindow
    SetForegroundWindow = user32.SetForegroundWindow
    SW_RESTORE = 9

    found_hwnd = None

    def foreach_window(hwnd, lParam):
        nonlocal found_hwnd
        if IsWindowVisible(hwnd):
            buf = ctypes.create_unicode_buffer(255)
            GetWindowText(hwnd, buf, 255)
            title = buf.value
            if title and title.strip() and title_match.lower() in title.lower():
                found_hwnd = hwnd
                return False  # Stop enumeration
        return True

    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    EnumWindows(WNDENUMPROC(foreach_window), 0)

    if found_hwnd:
        # If minimized, restore it
        ShowWindow(found_hwnd, SW_RESTORE)
        time.sleep(0.1)
        SetForegroundWindow(found_hwnd)
        print(f"Focused window matching: {title_match}")
        return True
    else:
        print(f"No visible window found matching: {title_match}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Desktop Control 鈥?Windows PC Automation')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Click command
    click_parser = subparsers.add_parser('click', help='Click mouse at position')
    click_parser.add_argument('--x', type=int, help='X coordinate')
    click_parser.add_argument('--y', type=int, help='Y coordinate')
    click_parser.add_argument('--button', choices=['left', 'right', 'middle'], default='left')
    click_parser.add_argument('--double', action='store_true', help='Double click')

    # Move command
    move_parser = subparsers.add_parser('move', help='Move mouse to position')
    move_parser.add_argument('--x', type=int, required=True)
    move_parser.add_argument('--y', type=int, required=True)

    # Type command
    type_parser = subparsers.add_parser('type', help='Type text')
    type_parser.add_argument('--text', type=str, required=True)
    type_parser.add_argument('--interval', type=float, default=0.05, help='Interval between keystrokes')

    # Key command
    key_parser = subparsers.add_parser('key', help='Press a special key')
    key_parser.add_argument('--key', type=str, required=True, help='Key name (enter, space, escape, tab, etc.)')

    # Hotkey command
    hotkey_parser = subparsers.add_parser('hotkey', help='Press a key combination (e.g. ctrl+c, alt+f4, win+d)')
    hotkey_parser.add_argument('--keys', type=str, required=True, help='Key combination using + separator')

    # Scroll command
    scroll_parser = subparsers.add_parser('scroll', help='Scroll mouse wheel')
    scroll_parser.add_argument('--clicks', type=int, required=True, help='Number of notches (negative=down, positive=up)')

    # Drag command
    drag_parser = subparsers.add_parser('drag', help='Drag from one point to another')
    drag_parser.add_argument('--x1', type=int, required=True)
    drag_parser.add_argument('--y1', type=int, required=True)
    drag_parser.add_argument('--x2', type=int, required=True)
    drag_parser.add_argument('--y2', type=int, required=True)
    drag_parser.add_argument('--button', choices=['left', 'right'], default='left')

    # Pos command
    subparsers.add_parser('pos', help='Get current cursor position')

    # Screenshot command
    screenshot_parser = subparsers.add_parser('screenshot', help='Take a screenshot')
    screenshot_parser.add_argument('--output', type=str, help='Output file path')

    # Windows command
    subparsers.add_parser('windows', help='List all visible windows')

    # Focus command
    focus_parser = subparsers.add_parser('focus', help='Focus a window by title (partial match)')
    focus_parser.add_argument('--title', type=str, required=True)

    # Wait command
    wait_parser = subparsers.add_parser('wait', help='Wait for specified seconds')
    wait_parser.add_argument('--seconds', type=float, required=True)

    args = parser.parse_args()

    if args.command == 'click':
        move_first = args.x is not None and args.y is not None
        if args.double:
            double_click(args.x, args.y)
        else:
            click_mouse(args.x, args.y, args.button)
        pos = get_cursor_pos()
        print(f"Clicked at ({pos[0]}, {pos[1]})")

    elif args.command == 'move':
        move_mouse_absolute(args.x, args.y)
        print(f"Moved mouse to ({args.x}, {args.y})")

    elif args.command == 'type':
        type_text(args.text, args.interval)
        print(f"Typed: {args.text}")

    elif args.command == 'key':
        key_lower = args.key.lower()
        if key_lower in VK_MAP:
            press_key(VK_MAP[key_lower])
            print(f"Pressed key: {args.key}")
        else:
            print(f"Unknown key: {args.key}")
            print(f"Available keys: {', '.join(sorted(VK_MAP.keys()))}")
            sys.exit(1)

    elif args.command == 'pos':
        x, y = get_cursor_pos()
        print(f"Cursor position: ({x}, {y})")

    elif args.command == 'screenshot':
        if args.output:
            take_screenshot(args.output)
        else:
            take_screenshot()

    elif args.command == 'scroll':
        scroll_mouse(args.clicks)
        direction = "down" if args.clicks < 0 else "up"
        print(f"Scrolled {direction} ({abs(args.clicks)} notches)")

    elif args.command == 'drag':
        drag_mouse(args.x1, args.y1, args.x2, args.y2, args.button)
        print(f"Dragged from ({args.x1},{args.y1}) to ({args.x2},{args.y2})")

    elif args.command == 'hotkey':
        print(f"Pressing hotkey: {args.keys}")
        press_hotkey(args.keys)

    elif args.command == 'windows':
        windows = list_windows()
        if windows:
            print(f"Found {len(windows)} visible windows:")
            for hwnd, title in sorted(windows, key=lambda w: w[1]):
                print(f"  [{hwnd}] {title}")
        else:
            print("No visible windows found.")

    elif args.command == 'focus':
        focus_window(args.title)

    elif args.command == 'wait':
        print(f"Waiting for {args.seconds} seconds...")
        time.sleep(args.seconds)
        print("Done waiting.")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
