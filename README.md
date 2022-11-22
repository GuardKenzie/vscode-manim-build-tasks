# Manim build tasks

A small script to manage rendering Manim projects.

## Requirements:
*Tasks shell input* is used to allow picking which scenes from the file to render. *Sty* is used for coloring output.

| Visual studio code | Python |
|--------------------|--------|
| [Tasks Shell Input](https://marketplace.visualstudio.com/items?itemName=augustocdias.tasks-shell-input) |  [sty](https://pypi.org/project/sty/) |

## Setup
Your Manim project structure should look like this
```
Project/
├─ .vscode/
│  └─ tasks.json
├─ scripts/
│  └─ renderer.py
└─ manim_project.py
```

## Tasks
### Render all scenes
Renders all `Scene`, `ThreeDScene`, `Slide` and `ThreeDSlide` classes in the current file. Scenes are rendered in parallel, with render pool size of 5. Errors are reported in the `logs` directory.

### Render scene
Gives a choice of which scene to render and in what quality

### Preview current scene
Renders the scene at the currently selected line number with the `-s` flag

### Render current scene (high/medium) quality
Same as **Preview current scene** but uses flags `-qp` and `-qm` respectively

## Renderer.py
### Syntax
```
python renderer.py <manim_file.py> [-n line_number_inside_scene] [-m manim_args] [-c class_name_to_render] [-l]
```

| Option | Long | Description |
| ------ | ----- | ----------- |
| `-n`   | `--line_number` | Render the scene class containing the given line number. |
| `-m`   | `--manim_args`  | The rendering args to pass to manim e.g. `pqm`. |
| `-c`   | `--class_name`  | The class to render. If specified, `-n` will be ignored. |
| `-l`   | `--list_classes` | Flag which lists all renderable classes in the file instead of rendering anything. |

---

**Have fun!**
:heart:
