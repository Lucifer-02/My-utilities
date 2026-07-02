# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A grab-bag of personal Linux desktop-automation scripts, not a single application. Each top-level `.py` file (or subdirectory) is an independent, runnable tool the user invokes directly or via a `Makefile` target/keybinding. There is no shared entrypoint, web server, or build pipeline — treat each script as its own small program. Don't try to unify them into a package or add cross-script abstractions unless asked.

## Environment & running scripts

- Package/dependency management is via **uv** (`pyproject.toml` + `uv.lock`, Python >=3.11, venv already at `.venv`). Run scripts with `uv run python3 <script>.py`, or `python3 <script>.py` after activating `.venv`.
- No test suite, linter config, or CI exists in this repo. Don't invent test/lint commands — verify changes by running the relevant script.
- Most scripts assume a **Linux/XFCE desktop** with these external CLI tools on PATH: `xdotool`, `xsel`, `mpv`/`ffplay`, `notify-send`, `crow` (crow-translate), `microsoft-edge`, `ebook-viewer`/`ebook-edit`, `xfce4-terminal`. Some scripts (`read_bookworm.py`, `SpeakFasterWindows/speak_translated_faster_Windows.py`) are Windows-specific counterparts and use `pyautogui`/Windows paths instead.
- Several scripts read the `DATA_PATH` env var to locate sibling project directories (e.g. `myLib/pidHandle`-adjacent `auto_stats.py`, `Makefile` targets `pull-*`). It's expected to point at a parent folder containing sibling repos like `stats-practices`, `gopl`, `music-theory`.
- `Makefile` (root and in `auto/`, `myLib/`, `startup/`) targets are the normal way these scripts get launched (often bound to hotkeys/window managers) — check the relevant `Makefile` before assuming how a script is invoked.

## Architecture: `myLib/`

Shared helpers imported by the top-level automation scripts (`speak_translated_faster.py`, `edit_translated.py`, etc.). Each module wraps one concern as thin subprocess/API calls — keep new shared logic here rather than duplicating it per-script:

- `translate.py` — `trans(source_lang, target_lang, source_text, translator=...)` dispatches to one of three backends: `"crow"` (shells out to `crow-translate`), `"api"` (older unofficial `translate.googleapis.com` endpoint), `"google_new"` (unofficial `translate-pa.googleapis.com` endpoint with a hardcoded key). These unofficial endpoints are known-unstable by design — expect them to break and don't over-invest in hardening error handling around them.
- `TTS.py` — `MyTTS` wraps three engines selected by string: `"crow"` (gTTS), `"my_lang_tool"`/`"main.exe"`, `"new_lang_tool"` (both are compiled binaries checked into `myLib/`, invoked via `check_output`, with hardcoded Linux (`/data/IMPORTANT/My-utilities/myLib/...`) vs Windows (`D:\IMPORTANT\...`) paths chosen by `os.name`). `tts()`/`tts_process()` pipe the resulting audio bytes into `mpv` or `ffplay` over stdin; `tts_process` forks it into a separate `multiprocessing.Process` so playback doesn't block the caller.
- `pidHandle.py` — find/kill a running player process by name or PID (`pidof`/`kill`/`os.kill`), used to stop currently-playing TTS audio before starting new playback.
- `copy.py` / `xdotool.py` — clipboard read (`xsel`) and keypress/window-focus (`xdotool`) wrappers.
- `normalize_str.py` — text cleanup helpers (strip newlines/returns, word-wrap `align`) used before translation/TTS.

## Notable script groups

- **Translate-and-speak pipeline**: `speak_translated_faster.py` (CLI, clipboard → translate → TTS in one shot) and `edit_translated.py` (PySide6 GUI variant: translate clipboard text, let the user edit it, then speak/paste it back) both compose the `myLib` modules above in the same order: get clipboard → normalize → translate → TTS. When changing one of these flows, check whether the same fix applies to the other.
- **PDF tooling**: `add_outline.py` builds a `pikepdf` bookmark tree from `outline.yaml` (parts → chapters, plus `preface`/`toc` entries) and writes `output.pdf` from `book.pdf`.
- **`converter.py`**: standalone CLI (argparse) converting a folder of `.parquet`/`.csv` files to `.xlsx` via Polars, with an Excel row-limit check and optional recursion.
- **`startup/`**: hotkey-triggered pickers — `pick_random_exercise.py` samples a row from `exercises.csv` and opens the matching PDF page in Edge with a desktop notification; `open_random_book.py` opens a random book from a hardcoded Books directory. Both depend on `startup/open_doc.py` for the actual file-opening logic.
- **`auto/auto_stats.py`**: orchestrates an `xfce4-terminal` + `mdbook` translation workspace by scripting terminal tabs and window-manager keypresses via `xdotool`.
