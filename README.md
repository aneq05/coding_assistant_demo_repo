# Coffee-Driven Development

A deliberately small and slightly ridiculous Python CLI
used as a sandbox for experimenting with AI-assisted
software engineering workflows.

The application tracks coffee consumption and developer
activity to estimate when software engineering decisions
start becoming questionable.

## Usage

```console
cdd drink espresso
cdd status
cdd history --limit 10
cdd stats --days 7
cdd interactive
```

For example, status after a productive morning:

```text
Coffee-Driven Development
─────────────────────────
Coffees today:      ☕ ☕
Caffeine today:     200 mg
Developer state:    PRODUCTIVE
```

Statistics over the last seven local calendar days:

```text
Coffee Statistics — last 7 days

Total coffees       9
Total caffeine      1,320 mg
Average per day     189 mg
Favorite drink      Espresso

Daily caffeine

Mon  Sep 01   █████         200 mg
Tue  Sep 02   ███████       280 mg
```

An empty day has explicit status:

```text
Coffees today:      0
Caffeine today:     0 mg
Developer state:    NO SIGNAL
```
