# Ball Physics Simulator 🎱

Welcome to the most fun & modern ball physics playground on the block!

## Features
- Colorful, different-sized, real-physics balls
- Collision mode: ON/OFF
- Reset all, add/delete balls manually or randomly
- Fully modern dark UI & responsive controls
- Speed up/slow motion for animation
- Live GUI automation test mode (`tester.py`)
- Quick info for ball count & speed, always visible

## Installation
Requires Python 3.8+ with built-in tkinter (`tk` usually comes with Python).

```bash
pip install tk
```
(if needed)

## How to Use?
### 1. Classic User Interface
Launch with:
```bash
python game.py
```
- Choose **ball size**, then **color** — a ball is added
- 🎲 **10x RANDOM**: Add 10 random balls at once
- ⏪/⚡ **SLOW/BOOST**: Decrease/Increase speed instantly
- ⟳ **RESET**: Clear screen and reset speed
- 🗑 **DELETE**: Remove last-added ball
- 💥 **COLLISION**: Toggle collisions ON/OFF
- 🖵 **FULLSCREEN**: Enter/exit fullscreen

Everything is clickable, smooth and visually tasty.

### 2. Automation Test Demo (for Devs & Curious Users)
Automatically simulates all button behaviors step-by-step in the GUI (you watch, it clicks!):
```bash
python tester.py
```
- Watch every demo step as real GUI actions
- When the test ends, the window stays open – play as you like!

## Dependencies
- Only standard Python modules (`tkinter`, `math`, `random`, `time`). No extra installs for most users!

## UI Hints
- Top info bar: shows active balls and current speed
- All controls are large, accessible & easy
- Visual look/feel is sleek and modern

---
**We hope you have a ball!**

For issues: just blame gravity 😜

---
Developed by: AI & YOU
