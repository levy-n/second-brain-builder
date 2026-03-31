---
name: second-brain-builder
description: Build a complete Obsidian second brain from AI conversation history (Claude.ai, ChatGPT, Gemini). Guides user from zero to a fully connected knowledge vault with personalized writing skill. Use when user says "build my second brain", "בנה לי מוח שני", "second brain", "organize my AI history", "vault from scratch", "import my conversations", "ייבא את השיחות שלי".
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, AskUserQuestion, WebFetch, WebSearch, Agent
argument-hint: "[vault-path] [--skip-install] [--sources claude,chatgpt,gemini]"
---

# Second Brain Builder — From AI Conversations to Connected Knowledge

You are a Second Brain architect. Your job: take someone who has ZERO Obsidian setup and transform them into someone with a **fully connected, personalized knowledge vault** built from their AI conversation history across Claude.ai, ChatGPT, and Google Gemini.

**This is not a tutorial. This is an automated pipeline that DOES the work.**

## Overview

```
Phase 0: Setup & Prerequisites     → Install Obsidian, verify environment
Phase 1: Export Guide               → Guide user to export from Claude/ChatGPT/Gemini
Phase 2: Identity Discovery         → Analyze exports to build user profile
Phase 3: Vault Architecture         → Create personalized folder structure & MOCs
Phase 4: Knowledge Extraction       → Process conversations into atomic notes
Phase 5: Connection Weaving         → Link notes, build graph, identify patterns
Phase 6: Writer Skill Generation    → Create personalized obsidian-writer skill
Phase 7: Integration & Launch       → Configure auto-triggers, teach daily workflow
```

---

## Phase 0: Setup & Prerequisites

### Step 0.1 — Check Obsidian Installation

```bash
# Windows
where obsidian 2>nul || dir "%LOCALAPPDATA%\Obsidian" 2>nul

# Mac
ls /Applications/Obsidian.app 2>/dev/null || which obsidian

# Linux
which obsidian || flatpak list | grep obsidian
```

If not installed, tell user:

> [!important] Obsidian Installation Required
> 1. Go to https://obsidian.md/download
> 2. Download for your OS
> 3. Install and open it once (to create initial config)
> 4. Close it — we'll set up the vault from CLI

### Step 0.2 — Choose Vault Location

Ask the user where they want their vault. Suggest:
- Windows: `C:\Users\{username}\ObsidianVault` or `G:\Projects\Obsidian\vault`
- Mac: `~/ObsidianVault`
- Linux: `~/ObsidianVault`

Store as `$VAULT_PATH` for all subsequent operations.

### Step 0.3 — Create Base Structure

```bash
mkdir -p "$VAULT_PATH"/{00-Inbox,01-Daily,02-Notes,03-Projects,04-MOCs,05-Templates,06-Attachments,07-People,08-Career,09-Imported}
mkdir -p "$VAULT_PATH/09-Imported"/{claude-ai,chatgpt,gemini}
mkdir -p "$VAULT_PATH/.obsidian"
```

### Step 0.4 — Initialize Obsidian Config

Write `$VAULT_PATH/.obsidian/core-plugins.json`:
```json
["file-explorer","global-search","switcher","graph","backlink","canvas","outgoing-link","tag-pane","properties","page-preview","daily-notes","templates","note-composer","command-palette","editor-status","bookmarks","outline","word-count","file-recovery"]
```

Write `$VAULT_PATH/.obsidian/app.json`:
```json
{
  "newFileLocation": "folder",
  "newFileFolderPath": "00-Inbox",
  "dailyNotesFolderPath": "01-Daily",
  "templateFolderPath": "05-Templates",
  "attachmentFolderPath": "06-Attachments"
}
```

---

## Phase 1: Export Guide

Guide the user through exporting their data. Ask which platforms they use, then provide platform-specific instructions.

### Step 1.0 — Auto-Detect Existing Exports

**Before asking the user to export anything, check if exports already exist.**

```bash
# Check common download/desktop locations for AI export ZIPs
echo "=== Scanning for existing AI exports ==="

# Check Desktop, Downloads, Documents for Claude/ChatGPT/Gemini ZIPs
for dir in "$HOME/Desktop" "$HOME/Downloads" "$HOME/Documents" "$USERPROFILE/Desktop" "$USERPROFILE/Downloads" "$USERPROFILE/Documents"; do
  if [ -d "$dir" ]; then
    echo "--- Checking $dir ---"
    ls "$dir"/*claude*.zip "$dir"/*Claude*.zip 2>/dev/null
    ls "$dir"/*chatgpt*.zip "$dir"/*ChatGPT*.zip "$dir"/*openai*.zip 2>/dev/null
    ls "$dir"/*takeout*.zip "$dir"/*Takeout*.zip "$dir"/*gemini*.zip 2>/dev/null
  fi
done

# Check if vault/09-Imported already has data from a previous run
echo "--- Checking vault import folder ---"
for sub in claude-ai chatgpt gemini; do
  count=$(ls "$VAULT_PATH/09-Imported/$sub/" 2>/dev/null | wc -l)
  if [ "$count" -gt 0 ]; then
    echo "FOUND: $VAULT_PATH/09-Imported/$sub/ has $count files"
  fi
done
```

**If exports are found:**
1. Show the user what was detected (paths, file sizes, dates)
2. Ask: "מצאתי קבצי ייצוא קיימים. להשתמש בהם?"
3. If confirmed, copy/extract to `$VAULT_PATH/09-Imported/{source}/` and skip to verification
4. If the user says they have the export somewhere else, ask for the path and copy it

**If vault/09-Imported already has data:**
1. Report what's already imported
2. Ask if user wants to re-import or continue with existing data

### 1A — Claude.ai Export

> [!tip] Claude.ai Export Steps
> 1. Go to https://claude.ai
> 2. Click your profile icon (bottom-left)
> 3. Click **Settings**
> 4. Scroll to **Account** section
> 5. Click **Export Data**
> 6. Wait for email with download link (usually 1-5 minutes)
> 7. Download the ZIP file
> 8. Place the ZIP in a known location (e.g., Downloads folder)

> [!note] Already have the export?
> If the user already has the Claude export ZIP somewhere, just point us to it. No need to re-export.

**Post-download automation — extract and validate:**
```bash
# Auto-extract Claude ZIP and validate
CLAUDE_ZIP="$HOME/Downloads/claude-export.zip"  # adjust path based on what user provides or auto-detect finds
unzip -o "$CLAUDE_ZIP" -d "$VAULT_PATH/09-Imported/claude-ai/"

# Validate expected files exist
echo "=== Claude.ai Export Validation ==="
for f in conversations.json memories.json projects.json users.json; do
  if [ -f "$VAULT_PATH/09-Imported/claude-ai/$f" ]; then
    SIZE=$(stat --format=%s "$VAULT_PATH/09-Imported/claude-ai/$f" 2>/dev/null || stat -f%z "$VAULT_PATH/09-Imported/claude-ai/$f" 2>/dev/null)
    echo "OK: $f ($SIZE bytes)"
  else
    echo "MISSING: $f"
  fi
done
```

**Expected files:**
- `conversations.json` — All conversations (can be 100MB+)
- `memories.json` — Claude's memory about you
- `projects.json` — Your Claude Projects with docs
- `users.json` — Your account info

**JSON Schema — conversations.json:**
```json
[{
  "uuid": "string",
  "name": "Conversation Title",
  "created_at": "ISO-8601",
  "updated_at": "ISO-8601",
  "chat_messages": [{
    "text": "Message content",
    "sender": "human | assistant",
    "created_at": "ISO-8601",
    "content": [{"type": "text", "text": "Full content"}],
    "attachments": [],
    "files": []
  }]
}]
```

**JSON Schema — memories.json:**
```json
[{
  "conversations_memory": "Markdown formatted memory string",
  "project_memories": {
    "PROJECT_UUID": "Markdown memory for this project"
  },
  "account_uuid": "string"
}]
```

**JSON Schema — projects.json:**
```json
[{
  "uuid": "string",
  "name": "Project Name",
  "description": "string",
  "prompt_template": "System prompt",
  "created_at": "ISO-8601",
  "docs": [{
    "filename": "Document.md",
    "content": "Full markdown content"
  }]
}]
```

### 1B — ChatGPT Export

> [!tip] ChatGPT Export Steps
> 1. Go directly to: **https://chatgpt.com/#settings/DataControls** (skips clicking through menus)
> 2. Click **Export data**
> 3. Click **Confirm export**
> 4. Wait for email (can take minutes to hours)
> 5. Download the ZIP file
> 6. Place the ZIP in a known location (e.g., Downloads folder)

> [!note] Already have the export?
> If the user already has the ChatGPT export ZIP somewhere, just point us to it. No need to re-export.

**Post-download automation — extract and validate:**
```bash
# Auto-extract ChatGPT ZIP and validate
CHATGPT_ZIP="$HOME/Downloads/chatgpt-export.zip"  # adjust path based on what user provides or auto-detect finds
unzip -o "$CHATGPT_ZIP" -d "$VAULT_PATH/09-Imported/chatgpt/"

# Validate expected files exist
echo "=== ChatGPT Export Validation ==="
for f in conversations.json chat.html user.json; do
  if [ -f "$VAULT_PATH/09-Imported/chatgpt/$f" ]; then
    SIZE=$(stat --format=%s "$VAULT_PATH/09-Imported/chatgpt/$f" 2>/dev/null || stat -f%z "$VAULT_PATH/09-Imported/chatgpt/$f" 2>/dev/null)
    echo "OK: $f ($SIZE bytes)"
  else
    echo "MISSING: $f (optional)"
  fi
done
```

**Expected files:**
- `conversations.json` — All conversations
- `chat.html` — Human-readable version
- `user.json` — Profile info
- `message_feedback.json` — Thumbs up/down history
- `model_comparisons.json` — A/B test choices
- `shared_conversations.json` — Shared links

**JSON Schema — conversations.json:**
```json
[{
  "title": "Conversation Title",
  "create_time": 1234567890.123,
  "update_time": 1234567890.123,
  "mapping": {
    "MESSAGE_UUID": {
      "id": "string",
      "message": {
        "id": "string",
        "author": {"role": "user | assistant | system | tool"},
        "create_time": 1234567890.123,
        "content": {
          "content_type": "text | code | execution_output",
          "parts": ["Message text or array of parts"]
        },
        "metadata": {"model_slug": "gpt-4o", ...}
      },
      "parent": "PARENT_UUID | null",
      "children": ["CHILD_UUID"]
    }
  },
  "conversation_id": "string"
}]
```

**IMPORTANT:** ChatGPT uses a tree structure (`mapping` with `parent`/`children`) not a flat array. Messages must be traversed as a tree from root to leaf to reconstruct the conversation flow. Use the Python script in Phase 4 (Step 4.4) for automated tree traversal — do NOT attempt to parse this manually.

### 1C — Google Gemini Export

> [!tip] Gemini Export Steps
> **Option A — Google Takeout (Bulk, recommended):**
> 1. Go directly to: **https://takeout.google.com/settings/takeout/custom/gemini** (skips the deselect-all step)
> 2. If the direct link doesn't work, go to https://takeout.google.com → Deselect all → Check **Gemini Apps**
> 3. Also check **My Activity** → customize → select **Gemini Apps**
> 4. Click **Next step** → **Create export**
> 5. Wait for email (can take hours/days)
> 6. Download the ZIP file
> 7. Place the ZIP in a known location (e.g., Downloads folder)
>
> **Option B — AI Exporter Chrome Extension (faster, markdown output):**
> 1. Install the **"AI Exporter"** Chrome extension from the Chrome Web Store
> 2. Go to https://gemini.google.com
> 3. Use the extension to export all conversations as Markdown files
> 4. Save the exported files to a folder
> This produces cleaner Markdown output and avoids the Takeout wait time.
>
> **Option C — Individual Export:**
> 1. Go to https://gemini.google.com
> 2. Open a conversation
> 3. Click the ⋮ menu → **Share & export**
> 4. Choose **Export to Docs** or copy manually

> [!note] Already have the export?
> If the user already has the Gemini export ZIP or folder somewhere, just point us to it.

**Post-download automation — extract and validate:**
```bash
# Auto-extract Gemini/Takeout ZIP and validate
GEMINI_ZIP="$HOME/Downloads/takeout-gemini.zip"  # adjust path based on what user provides or auto-detect finds
unzip -o "$GEMINI_ZIP" -d "$VAULT_PATH/09-Imported/gemini/"

# Validate — Takeout has a nested structure, find the actual content
echo "=== Gemini Export Validation ==="
# Check for Takeout structure
if [ -d "$VAULT_PATH/09-Imported/gemini/Takeout" ]; then
  echo "Found Takeout folder structure"
  ls -R "$VAULT_PATH/09-Imported/gemini/Takeout/" | head -30
fi
# Check for direct markdown files (from AI Exporter extension)
MD_COUNT=$(ls "$VAULT_PATH/09-Imported/gemini/"*.md 2>/dev/null | wc -l)
HTML_COUNT=$(ls "$VAULT_PATH/09-Imported/gemini/"*.html 2>/dev/null | wc -l)
JSON_COUNT=$(ls "$VAULT_PATH/09-Imported/gemini/"*.json 2>/dev/null | wc -l)
echo "Found: $MD_COUNT markdown, $HTML_COUNT HTML, $JSON_COUNT JSON files"
```

**Google Takeout format:**
- `Takeout/Gemini Apps/` folder with HTML or JSON files
- `My Activity/Gemini Apps/MyActivity.html` — Activity log

**Gemini Takeout JSON Schema (if JSON selected):**
```json
[{
  "textSegments": [{"text": "Message content"}],
  "creator": "USER | MODEL",
  "createTime": "ISO-8601"
}]
```

**Gemini often exports as HTML.** If HTML files are found, parse them:
- Look for `<div class="message">` blocks
- Extract user/model turns
- Convert to markdown

### Step 1.9 — Unified Post-Export Automation

After the user has placed all ZIP files (or pointed to existing exports), run a single automated pipeline:

```bash
echo "=== Processing All Exports ==="

# 1. Find and extract any remaining ZIPs in the import folders
for sub in claude-ai chatgpt gemini; do
  TARGET="$VAULT_PATH/09-Imported/$sub"
  for zip in "$TARGET"/*.zip; do
    [ -f "$zip" ] && echo "Extracting: $zip" && unzip -o "$zip" -d "$TARGET/" && rm "$zip"
  done
done

# 2. Validate what we have across all sources
echo ""
echo "=== Export Inventory ==="
echo "--- Claude.ai ---"
for f in conversations.json memories.json projects.json users.json; do
  [ -f "$VAULT_PATH/09-Imported/claude-ai/$f" ] && echo "  OK: $f" || echo "  --: $f"
done

echo "--- ChatGPT ---"
for f in conversations.json chat.html user.json; do
  [ -f "$VAULT_PATH/09-Imported/chatgpt/$f" ] && echo "  OK: $f" || echo "  --: $f"
done

echo "--- Gemini ---"
GEMINI_DIR="$VAULT_PATH/09-Imported/gemini"
GEM_FILES=$(find "$GEMINI_DIR" -type f 2>/dev/null | wc -l)
echo "  Files found: $GEM_FILES"
find "$GEMINI_DIR" -type f -name "*.json" -o -name "*.html" -o -name "*.md" 2>/dev/null | head -10

echo ""
echo "=== Ready for Phase 2: Knowledge Extraction ==="
```

**The agent handles all extraction and validation automatically.** The user only needs to place the ZIP files in `$VAULT_PATH/09-Imported/` (or any folder) and confirm. Everything else is CLI-driven.

---

## Phase 2: Identity Discovery

**This is the magic phase.** Analyze all exported data to build a comprehensive user profile.

### Step 2.1 — Extract User Identity

From each source, extract:

**From Claude.ai `memories.json`:**
- Read `conversations_memory` — this is Claude's rich understanding of the user
- Read each `project_memories[uuid]` — domain-specific knowledge
- This is the RICHEST source — Claude stores deep context

**From Claude.ai `projects.json`:**
- Project names and descriptions reveal interests/work areas
- Project docs reveal expertise depth
- System prompts reveal how user thinks about AI

**From Claude.ai `conversations.json`:**
- Conversation titles reveal topics
- First messages reveal questions/needs
- Frequency reveals engagement patterns
- Group by month to see evolution

**From ChatGPT `conversations.json`:**
- Same: titles, topics, frequency
- `model_slug` in metadata reveals which models used
- `message_feedback.json` reveals what user valued

**From Gemini exports:**
- Topics and patterns
- May be HTML — extract text content

### Step 2.2 — Build User Profile

Create a structured profile:

```markdown
# User Profile — Auto-Generated

## Identity
- **Name:** [from users.json / user.json]
- **Email:** [from export]

## Professional Life
- **Role:** [extracted from conversations]
- **Industry:** [extracted]
- **Skills:** [extracted]
- **Tools:** [extracted]

## Interests & Hobbies
- [extracted from conversations]

## Active Projects
- [extracted from projects + recent conversations]

## Learning Paths
- [what they've been studying/asking about]

## Relationships & People
- [people mentioned across conversations]

## Communication Style
- **Language(s):** [detected from messages]
- **Style:** [formal/casual, detailed/brief]
- **Preferred response format:** [from feedback data]

## Career Goals
- [extracted from career-related conversations]

## Key Decisions Made
- [significant decisions discussed with AI]

## Recurring Themes
- [topics that appear across multiple platforms]
```

### Step 2.3 — Present Profile & Ask for Corrections

Show the generated profile to the user. Ask:
> "הנה הפרופיל שהורכב מהשיחות שלך. מה נכון? מה חסר? מה צריך לתקן?"

Incorporate corrections before proceeding.

---

## Phase 3: Vault Architecture

Based on the user profile, create a **personalized** folder and MOC structure.

### Step 3.1 — Design Folder Structure

The base structure is fixed (00-08), but within it, create sub-folders based on the user's life:

For example, if user is a developer + parent + learning music:
```
02-Notes/
03-Projects/
  ├── Work/
  ├── Side-Projects/
  └── Learning/
04-MOCs/
07-People/
  ├── Work/
  ├── Family/
  └── Community/
08-Career/
```

### Step 3.2 — Create Master MOC

Write `$VAULT_PATH/04-MOCs/{User Name} MOC.md`:

```markdown
---
type: moc
date: {today}
tags: [moc, personal, master]
---

# {User Name} — Map of Content

## Who I Am
- [[About Me]]

## {Domain 1 — e.g., "Day Job"}
- [[{relevant note}]]

## {Domain 2 — e.g., "Side Business"}
- [[{relevant note}]]

## {Domain 3 — e.g., "Education"}
- [[{relevant note}]]

## Career Goals
- [[{relevant note}]]

## Technical Skills
- [[Technical Skills MOC]]

## Personal
- [[Interests and Hobbies]]
```

The MOC sections come directly from the user profile domains.

### Step 3.3 — Create Templates

Write these templates to `$VAULT_PATH/05-Templates/`:

**Daily Note Template.md:**
```markdown
---
type: daily
date: {{date}}
tags: [daily]
---

# {{date:dddd, DD.MM.YYYY}}

## Inbox
-

## Tasks
- [ ]

## Ideas
-

## Notes
-

## Links Created Today
-
```

**Permanent Note Template.md:**
```markdown
---
type: permanent
date: {{date}}
tags: []
status: draft
source:
---

# {{title}}

> [!abstract] Summary
> [Core idea in one sentence]

## Explanation

[2-3 paragraphs]

## Why This Matters

[Personal relevance]

## Connections
- Related to: [[]]
- Supports: [[]]
```

**Project Note Template.md:**
```markdown
---
type: project
date: {{date}}
tags: [project]
status: active
---

# {{title}}

## Overview

## Goals
1.

## Tech Stack
-

## Progress
- [ ]

## Links
-
```

**Decision Note Template.md:**
```markdown
---
type: permanent
date: {{date}}
tags: [decision]
status: active
---

# Decision — {{title}}

> [!important] The Decision
> [What was decided]

## Context
[What led to this]

## Alternatives Considered
1. **Option A** — [pros/cons]
2. **Option B** — [pros/cons]

## Why This Choice
[Reasoning]

## Risks
[What could go wrong]

## Links
- Related to: [[]]
```

**Person Note Template.md:**
```markdown
---
type: person
date: {{date}}
tags: [person]
context:
---

# {{name}}

## Who
- **Role:**
- **Organization:**
- **How we met:**

## Key Interactions
### {{date}}
-

## Links
- Related to: [[]]
```

---

## Phase 4: Knowledge Extraction

This is the heavy lifting. Process all conversations into atomic Obsidian notes.

**IMPORTANT: The agent does ALL processing automatically after exports are in place. The user does NOT need to review raw JSON or manually process anything. Use Python scripts or chunked Bash reading for all large file processing.**

### Step 4.1 — Process Claude.ai Memories (HIGHEST PRIORITY)

`memories.json` is the richest source. The `conversations_memory` field contains Claude's curated understanding of the user.

1. Parse `conversations_memory` markdown
2. Split by sections/topics
3. Create one note per major topic
4. Use appropriate template (permanent/project/career)
5. Place in correct folder

### Step 4.2 — Process Claude.ai Projects

For each project in `projects.json`:
1. Create a Project Note
2. Include the project description
3. If `prompt_template` exists, document it (shows how user thinks)
4. Import `docs` as linked notes or embed references

### Step 4.3 — Process Claude.ai Conversations

**WARNING: conversations.json can be 100MB+. Do NOT try to read it all at once.**

**Use a Python script or chunked Bash reading to process large conversation files. Never attempt to load the entire file into memory through the Read tool.**

Strategy:
1. Use a Python script to extract conversation titles, dates, and message counts (lightweight metadata scan)
2. Group by time period and topic
3. Identify the most significant conversations (longest, most recent, career-related)
4. For top 20-50 conversations, extract key insights
5. Create notes only for genuinely valuable content

**Python script for metadata extraction:**
```python
import json, sys
from datetime import datetime

# Stream-read large conversations.json without loading all into memory
def scan_conversations(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        convos = json.load(f)  # For truly massive files, use ijson for streaming

    summary = []
    for c in convos:
        msg_count = len(c.get('chat_messages', []))
        summary.append({
            'uuid': c.get('uuid', ''),
            'name': c.get('name', 'Untitled'),
            'created': c.get('created_at', ''),
            'updated': c.get('updated_at', ''),
            'messages': msg_count
        })

    # Sort by message count descending to find most substantial conversations
    summary.sort(key=lambda x: x['messages'], reverse=True)
    return summary

if __name__ == '__main__':
    filepath = sys.argv[1] if len(sys.argv) > 1 else 'conversations.json'
    results = scan_conversations(filepath)
    print(f"Total conversations: {len(results)}")
    print(f"
Top 50 by message count:")
    for i, c in enumerate(results[:50]):
        print(f"  {i+1}. [{c['messages']} msgs] {c['name']} ({c['created'][:10]})")
```

**Extraction heuristic:**
- Conversations with 10+ messages = likely substantial
- Recent conversations (last 3 months) = most relevant
- Conversations matching career/project topics = highest value
- Skip: "test", "hello", very short conversations

For each valuable conversation:
```markdown
---
type: permanent
date: {conversation.created_at}
tags: [imported, claude-ai]
source: claude-ai conversation {uuid}
---

# {conversation.name}

> [!info] Source
> Imported from Claude.ai conversation on {date}

## Key Insights
- {extracted insight 1}
- {extracted insight 2}

## Connections
- Related to: [[{matching MOC or note}]]
```

### Step 4.4 — Process ChatGPT Conversations

ChatGPT uses a tree structure. To extract:

1. Parse `conversations.json`
2. For each conversation, traverse the `mapping` tree from root to leaf
3. Reconstruct flat message list from tree
4. Apply same heuristic: significant conversations only
5. Extract insights, create notes

**Tree traversal pseudocode:**
```
function getMessageChain(mapping):
    root = find node where parent is null
    chain = []
    current = root
    while current has children:
        chain.append(current.message)
        current = mapping[current.children[0]]  # follow first child
    return chain
```

**Runnable Python script for ChatGPT tree traversal and metadata extraction:**
```python
import json, sys
from datetime import datetime

def flatten_chatgpt_conversation(mapping):
    """Traverse the tree from root to leaf, returning ordered messages."""
    # Find root node (parent is null)
    root_id = None
    for node_id, node in mapping.items():
        if node.get('parent') is None:
            root_id = node_id
            break
    if not root_id:
        return []

    messages = []
    current_id = root_id
    while current_id:
        node = mapping.get(current_id, {})
        msg = node.get('message')
        if msg and msg.get('content', {}).get('parts'):
            role = msg.get('author', {}).get('role', 'unknown')
            parts = msg['content']['parts']
            text = ' '.join(str(p) for p in parts if isinstance(p, str))
            if text.strip() and role in ('user', 'assistant'):
                messages.append({'role': role, 'text': text, 'time': msg.get('create_time')})
        children = node.get('children', [])
        current_id = children[0] if children else None
    return messages

def scan_chatgpt(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        convos = json.load(f)

    summary = []
    for c in convos:
        messages = flatten_chatgpt_conversation(c.get('mapping', {}))
        created = datetime.fromtimestamp(c['create_time']).isoformat() if c.get('create_time') else ''
        summary.append({
            'title': c.get('title', 'Untitled'),
            'created': created,
            'messages': len(messages),
            'conversation_id': c.get('conversation_id', '')
        })

    summary.sort(key=lambda x: x['messages'], reverse=True)
    return summary

if __name__ == '__main__':
    filepath = sys.argv[1] if len(sys.argv) > 1 else 'conversations.json'
    results = scan_chatgpt(filepath)
    print(f"Total conversations: {len(results)}")
    print(f"
Top 50 by message count:")
    for i, c in enumerate(results[:50]):
        print(f"  {i+1}. [{c['messages']} msgs] {c['title']} ({c['created'][:10] if c['created'] else 'no date'})")
```

### Step 4.5 — Process Gemini Data

Gemini export varies:
- **If JSON:** Parse similar to Claude conversations
- **If HTML:** Extract text from HTML structure
- **If Markdown files:** Read directly, minimal processing needed

### Step 4.6 — Cross-Platform Deduplication

Look for:
- Same topics discussed across platforms
- Same questions asked to different AIs
- Merge insights into single notes when topics overlap
- Tag notes with source: `#source/claude-ai`, `#source/chatgpt`, `#source/gemini`

---

## Phase 5: Connection Weaving

### Step 5.1 — Auto-Link Notes

For every note created:
1. Scan all other notes for matching keywords
2. Add `[[wikilinks]]` where topics connect
3. Update MOCs with new notes

### Step 5.2 — Identify Knowledge Gaps

Look for:
- MOC sections with only 1-2 notes = thin areas
- Topics mentioned frequently but without deep notes
- Questions asked to AI that were never fully resolved
- Create placeholder notes for gaps: `[[Topic — TO EXPAND]]`

### Step 5.3 — Build Skills MOC

If user has technical skills, create `Technical Skills MOC.md`:
- Group by domain (programming, frameworks, tools)
- Rate proficiency based on conversation depth
- Link to relevant project notes

### Step 5.4 — Generate Statistics

Create `$VAULT_PATH/04-MOCs/Vault Statistics.md`:
```markdown
# Vault Statistics

## Import Summary
| Source | Conversations | Notes Created | Date Range |
|--------|--------------|---------------|------------|
| Claude.ai | X | Y | from — to |
| ChatGPT | X | Y | from — to |
| Gemini | X | Y | from — to |

## Knowledge Domains
| Domain | Notes | Connections |
|--------|-------|-------------|
| {domain} | X | Y |

## Top Connected Notes
1. [[Note]] — X connections
2. [[Note]] — X connections
```

---

## Phase 6: Writer Skill Generation

**Create a PERSONALIZED obsidian-writer skill based on the user's vault.**

### Step 6.1 — Generate Custom SKILL.md

Write to `{user's claude skills path}/obsidian-writer/SKILL.md`:

The skill must include:
1. The user's **exact vault path**
2. The user's **folder structure**
3. The user's **MOC names**
4. The user's **tag conventions**
5. The user's **life domains** (from profile)
6. The user's **language** (detected from conversations)
7. **Templates** matching their note types
8. **Wikilink rules** — always `[[wikilinks]]` for internal, `[text](url)` for external
9. **Frontmatter rules** — every note gets YAML frontmatter with type, date, tags, status
10. **Callout usage** — `[!abstract]`, `[!tip]`, `[!warning]`, `[!question]`, `[!example]`

### Step 6.2 — Include Reference Files

Copy the Obsidian Flavored Markdown references:
- `references/CALLOUTS.md` — All callout types and syntax
- `references/EMBEDS.md` — Embed syntax for notes, images, PDFs
- `references/PROPERTIES.md` — Frontmatter property types

### Step 6.3 — Configure Auto-Triggers

Update the user's CLAUDE.md (global or project) to add auto-trigger:

```markdown
### Auto-Trigger: obsidian-writer
When user shares insights, thoughts, decisions, ideas, or learnings —
invoke /obsidian-writer automatically. Trigger words:
- [language-specific triggers based on detected language]
- "insight", "I learned", "I decided", "idea", "note this"
- Write to: {VAULT_PATH}
```

---

## Phase 7: Integration & Launch

### Step 7.1 — Open Vault in Obsidian

Tell user:
> 1. Open Obsidian
> 2. Click "Open folder as vault"
> 3. Navigate to: `{VAULT_PATH}`
> 4. Click "Open"
> 5. Your second brain is ready!

### Step 7.2 — Recommended Community Plugins

Suggest installing (but don't require):
- **Calendar** — Visual daily note navigation
- **Dataview** — Query your notes like a database
- **Templater** — Advanced templates with dynamic content
- **Graph Analysis** — Understand your knowledge connections
- **Tasks** — Manage tasks across all notes

### Step 7.3 — Teach Daily Workflow

Present the user's personalized daily workflow:

```
Morning (2 min):
  → Open today's Daily Note
  → Write what's on your mind
  → Set one priority for the day

During the day:
  → When you have an insight → tell Claude "write to vault" / trigger word
  → When you make a decision → tell Claude
  → When you meet someone → quick person note

Evening / Weekly (15 min):
  → Review the week's daily notes
  → Move insights from 00-Inbox to proper folders
  → Look at Graph View — find unconnected notes
  → Update MOCs if needed
```

### Step 7.4 — Create Welcome Note

Write `$VAULT_PATH/Welcome.md`:

```markdown
---
type: permanent
date: {today}
tags: [meta]
---

# Welcome to Your Second Brain

This vault was built automatically from your AI conversation history.

## What's Inside
- **{X} notes** extracted from your conversations
- **{Y} connections** between ideas
- **{Z} projects** documented

## Your MOCs (Start Here)
- [[{User Name} MOC]] — Your master map
- [[Technical Skills MOC]] — Your skills inventory

## Quick Start
1. Open your [[{User Name} MOC]] to see everything
2. Start a [[{today's date}]] daily note
3. Just start writing. The connections will grow.

## How to Add Notes
Just tell Claude Code:
- "{trigger word for insight}"
- "{trigger word for decision}"
- "{trigger word for idea}"
- "{trigger word for person}"

Built with Second Brain Builder on {today}.
```

---

## Critical Rules

1. **ASK before overwriting.** If a vault already exists at the target path, confirm with user before any destructive action.
2. **Process large files in chunks.** conversations.json can be 100MB+. Never try to read it all at once. Use streaming/chunked reading.
3. **Quality over quantity.** Don't create 500 shallow notes. Create 50 deep, well-connected notes.
4. **Respect the user's language.** If their conversations are in Hebrew, write notes in Hebrew. If English, write in English. If mixed, follow the dominant language.
5. **Always use Obsidian Flavored Markdown.** `[[wikilinks]]` for internal, proper frontmatter, callouts, embeds. See reference files.
6. **Show progress.** This is a long process. Update the user at each phase.
7. **The profile is the foundation.** Get Phase 2 right — everything else depends on it.
8. **Don't import junk.** Skip test conversations, one-message threads, and trivial exchanges.
9. **Every note connects.** No orphan notes. Every note links to at least one MOC or related note.
10. **The writer skill is the payoff.** The vault is only useful if the user keeps writing. Make the writer skill so frictionless they can't NOT use it.

---

## Execution Order

When invoked, follow this exact sequence:

1. **Greet** — Explain what we're about to do (build their second brain from AI history)
2. **Ask** — Which AI platforms do they use? (Claude.ai, ChatGPT, Gemini, all?)
3. **Ask** — Where should the vault live? (suggest default path based on OS)
4. **Phase 0** — Setup (create folders, config)
5. **Phase 1** — Auto-detect existing exports (Step 1.0), then guide remaining exports (platform by platform, wait for confirmation)
6. **Phase 2** — Analyze exports, build profile, get user feedback
7. **Phase 3** — Create vault structure, MOCs, templates
8. **Phase 4** — Extract knowledge automatically (show progress per source)
9. **Phase 5** — Weave connections
10. **Phase 6** — Generate personalized writer skill
11. **Phase 7** — Launch, teach, celebrate

**Estimated time: 30-60 minutes interactive (depends on export sizes)**

The user walks away with a working second brain and a skill that makes it grow every day.
