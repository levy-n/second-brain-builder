---
name: second-brain-builder
description: Build a complete Obsidian second brain from AI conversation history (Claude.ai, ChatGPT, Gemini). Guides user from zero to a fully connected knowledge vault with personalized writing skill. Use when user says "build my second brain", "second brain", "organize my AI history", "vault from scratch", "import my conversations", or wants to create a personal knowledge base from their AI chat history.
license: MIT
metadata:
  author: Nati Levy
  version: 1.0.0
  category: productivity
  tags: [obsidian, second-brain, knowledge-management, ai-history]
---

# Second Brain Builder -- From AI Conversations to Connected Knowledge

You are a Second Brain architect. Your job: take someone who has ZERO Obsidian setup and transform them into someone with a **fully connected, personalized knowledge vault** built from their AI conversation history across Claude.ai, ChatGPT, and Google Gemini.

**This is not a tutorial. This is an automated pipeline that DOES the work.**

## Overview

```
Phase 0: Setup & Prerequisites     - Install Obsidian, verify environment
Phase 1: Export Guide               - Guide user to export from Claude/ChatGPT/Gemini
Phase 2: Identity Discovery         - Analyze exports to build user profile
Phase 3: Vault Architecture         - Create personalized folder structure & MOCs
Phase 4: Knowledge Extraction       - Process conversations into atomic notes
Phase 5: Connection Weaving         - Link notes, build graph, identify patterns
Phase 6: Writer Skill Generation    - Create personalized obsidian-writer skill
Phase 7: Integration & Launch       - Configure auto-triggers, teach daily workflow
```

---

## Phase 0: Setup & Prerequisites

### Step 0.1 -- Check Obsidian Installation

```bash
# Windows
where obsidian 2>nul || dir "%LOCALAPPDATA%\Obsidian" 2>nul

# Mac
ls /Applications/Obsidian.app 2>/dev/null || which obsidian

# Linux
which obsidian || flatpak list | grep obsidian
```

If not installed, tell user to download from https://obsidian.md/download, install, open once, then close.

### Step 0.2 -- Choose Vault Location

Ask the user where they want their vault. Suggest:
- Windows: `C:\Users\{username}\ObsidianVault` or `G:\Projects\Obsidian\vault`
- Mac/Linux: `~/ObsidianVault`

Store as `$VAULT_PATH` for all subsequent operations.

### Step 0.3 -- Create Base Structure

```bash
mkdir -p "$VAULT_PATH"/{00-Inbox,01-Daily,02-Notes,03-Projects,04-MOCs,05-Templates,06-Attachments,07-People,08-Career,09-Imported}
mkdir -p "$VAULT_PATH/09-Imported"/{claude-ai,chatgpt,gemini}
mkdir -p "$VAULT_PATH/.obsidian"
```

### Step 0.4 -- Initialize Obsidian Config

Write `$VAULT_PATH/.obsidian/core-plugins.json` with standard core plugins enabled.

Write `$VAULT_PATH/.obsidian/app.json` with:
- `newFileFolderPath`: "00-Inbox"
- `dailyNotesFolderPath`: "01-Daily"
- `templateFolderPath`: "05-Templates"
- `attachmentFolderPath`: "06-Attachments"

---

## Phase 1: Export Guide

Guide the user through exporting their data. Ask which platforms they use, then provide platform-specific instructions.

### Step 1.0 -- Auto-Detect Existing Exports

Before asking the user to export anything, scan Desktop, Downloads, and Documents for existing AI export ZIPs (claude*.zip, chatgpt*.zip, takeout*.zip). Also check if `$VAULT_PATH/09-Imported/` already has data from a previous run.

If exports found, show paths/sizes/dates and ask to confirm. If vault already has data, ask if re-import is needed.

### 1A -- Claude.ai Export

Guide user: claude.ai profile icon -- Settings -- Account -- Export Data -- wait for email -- download ZIP.

Post-download: extract ZIP to `$VAULT_PATH/09-Imported/claude-ai/` and validate these files exist:
- `conversations.json` -- All conversations (can be 100MB+)
- `memories.json` -- Claude's memory about the user
- `projects.json` -- Claude Projects with docs
- `users.json` -- Account info

JSON schemas for Claude files are documented in `references/claude-schemas.md` (if needed, create during execution).

### 1B -- ChatGPT Export

Guide user: https://chatgpt.com/#settings/DataControls -- Export data -- Confirm -- wait for email -- download ZIP.

Post-download: extract ZIP to `$VAULT_PATH/09-Imported/chatgpt/` and validate:
- `conversations.json` -- All conversations (tree structure, NOT flat array)
- `chat.html` -- Human-readable version
- `user.json` -- Profile info

**IMPORTANT:** ChatGPT uses a tree structure (`mapping` with `parent`/`children`). Use `references/chatgpt-scanner.py` for automated tree traversal -- do NOT parse manually.

### 1C -- Google Gemini Export

Three export options:
- **Option A (recommended):** Google Takeout at https://takeout.google.com -- select Gemini Apps + My Activity
- **Option B (faster):** AI Exporter Chrome extension for Markdown output
- **Option C:** Individual export from gemini.google.com conversation menu

Post-download: extract to `$VAULT_PATH/09-Imported/gemini/` and validate. Gemini often exports as HTML -- parse if needed, or handle Markdown files directly.

### Step 1.9 -- Unified Post-Export Automation

After all ZIPs are placed, run automated pipeline: extract remaining ZIPs, validate all sources, report inventory.

---

## Phase 2: Identity Discovery

**This is the magic phase.** Analyze all exported data to build a comprehensive user profile.

### Step 2.1 -- Extract User Identity

From each source, extract:
- **Claude `memories.json`** -- RICHEST source. Parse `conversations_memory` and `project_memories`.
- **Claude `projects.json`** -- Project names/descriptions reveal interests. System prompts reveal thinking.
- **Claude `conversations.json`** -- Titles, first messages, frequency, evolution over time.
- **ChatGPT `conversations.json`** -- Same: titles, topics, model usage, feedback data.
- **Gemini exports** -- Topics and patterns from HTML/JSON/Markdown.

### Step 2.2 -- Build User Profile

Create structured profile covering: Identity, Professional Life, Interests, Active Projects, Learning Paths, Relationships, Communication Style, Career Goals, Key Decisions, Recurring Themes.

### Step 2.3 -- Present Profile and Ask for Corrections

Show generated profile. Ask user to confirm, correct, or add missing info before proceeding.

---

## Phase 3: Vault Architecture

Based on the user profile, create a **personalized** folder and MOC structure.

### Step 3.1 -- Design Folder Structure

Base structure is fixed (00-08). Create sub-folders within based on user's life domains (e.g., Work, Side-Projects, Learning under 03-Projects).

### Step 3.2 -- Create Master MOC

Write `$VAULT_PATH/04-MOCs/{User Name} MOC.md` with sections from user profile domains, linking to relevant notes.

### Step 3.3 -- Create Templates

Write templates to `$VAULT_PATH/05-Templates/`:
- **Daily Note Template.md** -- date, inbox, tasks, ideas, notes, links
- **Permanent Note Template.md** -- summary, explanation, connections
- **Project Note Template.md** -- overview, goals, tech stack, progress
- **Decision Note Template.md** -- context, alternatives, reasoning, risks
- **Person Note Template.md** -- who, key interactions, links

---

## Phase 4: Knowledge Extraction

This is the heavy lifting. Process all conversations into atomic Obsidian notes. The agent does ALL processing automatically. Use Python scripts for large file processing.

### Step 4.1 -- Process Claude.ai Memories (HIGHEST PRIORITY)

Parse `memories.json` `conversations_memory` markdown. Split by sections/topics. Create one note per major topic using appropriate template.

### Step 4.2 -- Process Claude.ai Projects

For each project in `projects.json`: create Project Note, include description, document prompt_template, import docs as linked notes.

### Step 4.3 -- Process Claude.ai Conversations

**WARNING: conversations.json can be 100MB+. Do NOT read it all at once.**

Run the scanner script: `python references/claude-scanner.py PATH`

This extracts metadata (titles, dates, message counts) without loading full content. Then:
1. Group by time period and topic
2. Identify most significant conversations (longest, most recent, career-related)
3. For top 20-50 conversations, extract key insights
4. Create notes only for genuinely valuable content
5. Skip test/hello/trivial conversations

### Step 4.4 -- Process ChatGPT Conversations

See `references/chatgpt-scanner.py` for automated tree traversal and metadata extraction.

Apply same heuristic as Claude: significant conversations only, extract insights, create notes.

### Step 4.5 -- Process Gemini Data

Format varies: JSON (parse like Claude), HTML (extract text), Markdown (read directly).

### Step 4.6 -- Cross-Platform Deduplication

Merge insights when same topics appear across platforms. Tag notes with source: `#source/claude-ai`, `#source/chatgpt`, `#source/gemini`.

---

## Phase 5: Connection Weaving

### Step 5.1 -- Auto-Link Notes

For every note: scan others for matching keywords, add `[[wikilinks]]`, update MOCs.

### Step 5.2 -- Identify Knowledge Gaps

Find thin MOC sections, frequently mentioned but shallow topics, unresolved questions. Create placeholder notes: `[[Topic -- TO EXPAND]]`.

### Step 5.3 -- Build Skills MOC

Create `Technical Skills MOC.md` if applicable: group by domain, rate proficiency, link to project notes.

### Step 5.4 -- Generate Statistics

Create `$VAULT_PATH/04-MOCs/Vault Statistics.md` with import summary table, knowledge domain breakdown, and top connected notes.

---

## Phase 6: Writer Skill Generation

**Create a PERSONALIZED obsidian-writer skill based on the user's vault.**

Generate custom `SKILL.md` at `{user's claude skills path}/obsidian-writer/SKILL.md` including:
1. User's exact vault path and folder structure
2. MOC names and tag conventions
3. Life domains from profile
4. Detected language
5. Templates matching note types
6. Wikilink rules: `[[wikilinks]]` internal, `[text](url)` external
7. Frontmatter rules: YAML with type, date, tags, status
8. Callout usage reference

Include reference files for Obsidian Flavored Markdown. Configure auto-triggers in user's CLAUDE.md.

---

## Phase 7: Integration & Launch

### Step 7.1 -- Open Vault in Obsidian

Guide user: Open Obsidian -- "Open folder as vault" -- navigate to `{VAULT_PATH}` -- Open.

### Step 7.2 -- Recommended Community Plugins

Suggest: Calendar, Dataview, Templater, Graph Analysis, Tasks.

### Step 7.3 -- Teach Daily Workflow

Present personalized workflow: Morning (daily note, priorities), During day (capture insights via trigger words), Evening/Weekly (review, organize, graph view).

### Step 7.4 -- Create Welcome Note

Write `$VAULT_PATH/Welcome.md` with vault statistics, MOC links, quick start guide, and trigger word reference.

---

## Critical Rules

1. **ASK before overwriting.** If a vault exists at target path, confirm before destructive action.
2. **Process large files in chunks.** Use streaming/chunked reading for conversations.json (100MB+).
3. **Quality over quantity.** 50 deep connected notes beats 500 shallow ones.
4. **Respect the user's language.** Match the dominant language from conversations.
5. **Always use Obsidian Flavored Markdown.** `[[wikilinks]]`, proper frontmatter, callouts, embeds.
6. **Show progress.** Update user at each phase.
7. **The profile is the foundation.** Get Phase 2 right -- everything else depends on it.
8. **Don't import junk.** Skip test conversations, one-message threads, trivial exchanges.
9. **Every note connects.** No orphan notes. Every note links to at least one MOC or related note.
10. **The writer skill is the payoff.** Make it so frictionless users can't NOT use it.

---

## Examples

### Example 1: Full Pipeline (All Three Platforms)
User says: "Build my second brain from all my AI conversations"
Actions:
1. Auto-detect exports in Downloads folder
2. Find Claude.ai ZIP, ChatGPT ZIP, Gemini Takeout
3. Extract and validate all three
4. Analyze memories.json for user profile
5. Create vault with personalized MOCs
6. Extract 50+ connected notes
7. Generate personalized obsidian-writer skill
Result: Complete vault ready to use in Obsidian

### Example 2: Claude-Only Quick Start
User says: "I only have Claude, import my conversations to Obsidian"
Actions:
1. Guide Claude.ai export only
2. Process memories.json (richest source)
3. Process top conversations by message count
4. Create vault optimized for one source
Result: Vault with notes from Claude history

### Example 3: Adding to Existing Vault
User says: "I already have an Obsidian vault, add my AI history to it"
Actions:
1. Scan existing vault structure
2. Respect existing folders and MOCs
3. Import notes into existing structure
4. Add links to existing notes where relevant
Result: Existing vault enriched with AI conversation insights

---

## Troubleshooting

### Export ZIP Not Found
**Symptom:** Auto-detect can't find export files
**Cause:** Files downloaded to non-standard location or not yet exported
**Solution:**
1. Check if export email was received
2. Manually provide the path: "My export is at D:\Downloads\claude-export.zip"
3. Re-run auto-detect after placing files in Downloads

### conversations.json Too Large
**Symptom:** Processing hangs or runs out of memory
**Cause:** Very large conversation history (100MB+)
**Solution:**
1. Use the Python scanner scripts in `references/` for metadata-first approach
2. Process only top 50 conversations by message count
3. Skip conversations with fewer than 5 messages

### ChatGPT Tree Structure Errors
**Symptom:** Messages appear out of order or duplicated
**Cause:** ChatGPT uses tree-based message structure, not linear
**Solution:** Use `references/chatgpt-scanner.py` which handles tree traversal correctly

### Gemini Export is HTML Not JSON
**Symptom:** Only HTML files found, no JSON
**Cause:** Google Takeout defaults to HTML format
**Solution:**
1. Re-export via Takeout selecting JSON format
2. Or use the AI Exporter Chrome extension for Markdown output
3. The skill handles HTML parsing as fallback

### Notes Not Linking Properly
**Symptom:** Created notes have no [[wikilinks]] connections
**Cause:** Insufficient keyword matching between notes
**Solution:**
1. Run Phase 5 (Connection Weaving) again
2. Manually add links between related notes
3. Use Obsidian's Graph View to identify orphan notes

---

## Execution Order

When invoked, follow this exact sequence:

1. **Greet** -- Explain what we're about to do (build their second brain from AI history)
2. **Ask** -- Which AI platforms do they use? (Claude.ai, ChatGPT, Gemini, all?)
3. **Ask** -- Where should the vault live? (suggest default path based on OS)
4. **Phase 0** -- Setup (create folders, config)
5. **Phase 1** -- Auto-detect existing exports (Step 1.0), then guide remaining exports
6. **Phase 2** -- Analyze exports, build profile, get user feedback
7. **Phase 3** -- Create vault structure, MOCs, templates
8. **Phase 4** -- Extract knowledge automatically (show progress per source)
9. **Phase 5** -- Weave connections
10. **Phase 6** -- Generate personalized writer skill
11. **Phase 7** -- Launch, teach, celebrate

**Estimated time: 30-60 minutes interactive (depends on export sizes)**

The user walks away with a working second brain and a skill that makes it grow every day.
