"""
Claude.ai Conversation Scanner
Extracts metadata from conversations.json without loading full message content.
Usage: python claude-scanner.py PATH_TO_CONVERSATIONS_JSON
"""

import json
import sys
from datetime import datetime


def scan_conversations(filepath):
    """Stream-read large conversations.json and extract metadata."""
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
    print(f"\nTop 50 by message count:")
    for i, c in enumerate(results[:50]):
        print(f"  {i+1}. [{c['messages']} msgs] {c['name']} ({c['created'][:10]})")
