# 🚀 Multiverse Fugitive

**A choice-based, text-driven adventure where you flee across parallel universes to evade the Multiverse Authority.**

---

## 🔍 Overview

**Multiverse Fugitive** is a modular, Python-powered game that drops you into a high-stakes chase through multiple universes. Every decision shapes your path—will you hide in the shadows of the Monsterverse or blend into the intrigue of Spy X Family? With an architecture designed for easy expansion, new universes are a breeze to add.

## ⚡️ Key Features

* **Choice-Based Gameplay**: Your decisions dictate the story; there’s no turning back.
* **Modular Universe System**: Each universe lives in its own folder—add, remove, or tweak with zero friction.
* **Save & Load**: Bookmark your progress and jump back in anytime.
* **Extensible Design**: Plug in new universes like WickVerse, MCU, Blade Runner, and beyond.
* **Command-Line Interface**: Dive in with a single command—no GUI bloat.

## 🚀 Getting Started

### Prerequisites

* Python 3.10 or higher
* [Poetry](https://python-poetry.org/) (optional, but recommended)

### Installation

```bash
# Clone the repo
git clone https://github.com/Slick2007/MultiverseFugitive.git
cd MultiverseFugitive

# Using Poetry
dpoetry install
poetry shell

# Or with pip
pip install -r requirements.txt
```

## 🎮 How to Play

Run the main driver:

```bash
python main.py
```

Follow the prompts to:

1. Choose your starting universe
2. Make strategic choices to evade capture
3. Save or load your game at any checkpoint

## 🛠️ Project Structure

```plaintext
├── attached_assets/       # Images, icons, and static files
├── saves/                 # Saved game states (.json)
├── universes/             # Modular universe definitions
│   ├── Monsterverse/      # Example universe folder
│   ├── SpyXFamily/        # Another universe example
│   └── ...                # Drop in more universes here
├── core.py                # Core game loop and logic
├── main.py                # Entry point and CLI handler
├── save_manager.py        # Save/load engine
├── utils.py               # Utility functions (I/O, formatting)
├── pyproject.toml         # Project metadata & dependencies
└── uv.lock                # Lockfile for dependencies
```

## 🧩 Adding a New Universe

1. **Create a folder** under `universes/`, e.g., `MyNewVerse/`.
2. **Define** a `config.json` for scenes and choices.
3. **Implement** any special logic in `MyNewVerse.py` (optional).
4. **Register** your universe in `core.py` by adding it to the loader.

*That’s it! Your universe will appear in the choice menu.*

## 🤝 Contributing

We welcome adventurers! Please:

1. Fork this repository.
2. Create a feature branch (`git checkout -b feature/my-verse`).
3. Commit your changes (`git commit -m "Add MyNewVerse module"`).
4. Push to the branch (`git push origin feature/my-verse`).
5. Open a Pull Request.

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📜 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.

---

> **Reality Check:** This README is a living document—feedback and tweaks keep the adventure sharp.
