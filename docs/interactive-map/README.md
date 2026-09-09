# Interactive Project Mind Map

This folder contains an interactive mind map created as a visual walkthrough of the **Coffee-Driven Development** project.

The map is implemented as a standalone HTML page. After opening it in a browser, you can click the four main tiles to expand individual sections of the presentation.

The map includes:

- an overview of the application and its main features,
- repository organization,
- engineering quality principles and AI-assisted development practices,
- the lifecycle of a single Pull Request,
- screenshots showing the CLI in action.

It is intended primarily as a lightweight visual aid for presenting the project during a technical interview or a quick repository walkthrough.

## How to run the mind map

### Option 1 — Open it directly in a browser

Open:

```text
docs/interactive-map/index.html
```

You can simply double-click the file or use **Open with → Browser**.

### Option 2 — Run a local HTTP server

From the repository root, run:

```powershell
python -m http.server 8000 -d docs/interactive-map
```

Then open:

```text
http://localhost:8000
```

This option is recommended when presenting the project.

## How to use it

- Click one of the four main tiles to expand its content.
- Click the same tile again to collapse it.
- Selecting another tile replaces the currently expanded section.
- Use **Presentation Mode** to simplify the view for presenting.
- Press `F11` in the browser to enter fullscreen mode.

## Files

```text
docs/interactive-map/
├── index.html   # interactive mind map
└── README.md    # usage and launch instructions
```

The mind map does not require any additional frontend frameworks or dependencies.
