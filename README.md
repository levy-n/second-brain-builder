# Second Brain Builder

Build a complete Obsidian second brain from your AI conversation history — Claude.ai, ChatGPT, and Google Gemini.

This Claude Code skill takes you from zero to a fully connected personal knowledge vault, built from the conversations you've already had with AI.

## What It Does

```
Phase 0: Setup          → Install Obsidian, create vault structure
Phase 1: Export         → Auto-detect + guide data export from AI platforms
Phase 2: Identity       → Analyze your conversations to build your personal profile
Phase 3: Architecture   → Create personalized folders, MOCs, and templates
Phase 4: Extraction     → Process conversations into atomic, connected notes
Phase 5: Connections    → Weave links between notes, identify knowledge gaps
Phase 6: Writer Skill   → Generate a personalized daily writing skill for YOUR vault
Phase 7: Launch         → Open vault, teach workflow, start growing
```

## Why?

You've been talking to AI for years. Claude knows your career goals. ChatGPT helped you debug code at 2am. Gemini answered your random questions. All that knowledge is sitting in export files, disconnected and forgotten.

This skill takes all of it and builds a connected knowledge graph — your second brain — that you can search, link, and grow every day.

## Supported Platforms

| Platform | Export Method | What's Extracted |
|----------|-------------|-----------------|
| **Claude.ai** | Settings → Export Data | Conversations, memories, projects, docs |
| **ChatGPT** | Settings → Data Controls → Export | Conversations (tree structure), feedback |
| **Google Gemini** | Google Takeout / AI Exporter extension | Conversations (HTML/JSON/Markdown) |

## Installation

### Option A: Add to your Claude Code skills

Copy the `SKILL.md` file to your Claude Code skills directory:

```bash
# Create the skill folder
mkdir -p ~/.claude/skills/second-brain-builder

# Copy the skill file
cp SKILL.md ~/.claude/skills/second-brain-builder/
```

### Option B: Add to a specific project

Copy to your project's `.claude/skills/` directory:

```bash
mkdir -p .claude/skills/second-brain-builder
cp SKILL.md .claude/skills/second-brain-builder/
```

## Usage

Just tell Claude Code:

```
/second-brain-builder
```

Or say any of these:
- "build my second brain"
- "import my AI conversations to Obsidian"
- "create a vault from my chat history"

The skill will guide you through the entire process interactively.

## What You Get

After running the skill, you'll have:

- An **Obsidian vault** with personalized folder structure
- **Maps of Content (MOCs)** organized around YOUR life domains
- **Atomic notes** extracted from your most valuable AI conversations
- **Templates** for daily notes, insights, decisions, ideas, people
- **A personalized `obsidian-writer` skill** that auto-triggers when you share thoughts with Claude Code
- **Connected knowledge graph** — every note linked to related notes and MOCs

## Key Features

- **Auto-detects existing exports** — scans Downloads/Desktop before asking you to export
- **Direct links** to export pages (skip the menu clicking)
- **Automated ZIP extraction and validation** — you just drop the file, CLI does the rest
- **Python scripts** for processing large conversation files (ChatGPT tree traversal, Claude metadata extraction)
- **Cross-platform deduplication** — merges insights discussed across multiple AI platforms
- **Language detection** — writes notes in YOUR language (Hebrew, English, etc.)

## The Daily Workflow (After Setup)

```
Morning (2 min):
  → Open today's Daily Note
  → Write what's on your mind

During the day:
  → Share an insight with Claude Code → auto-captured to vault
  → Make a decision → documented
  → Meet someone → quick person note

Weekly (15 min):
  → Review the week's notes
  → Check Graph View for unconnected ideas
  → Update MOCs
```

## Credits

- Built on top of [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) — the official Obsidian agent skills by Steph Ango (CEO of Obsidian)
- Obsidian Flavored Markdown references (callouts, embeds, properties) from the official spec

## License

MIT
