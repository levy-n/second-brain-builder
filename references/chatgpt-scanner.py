"""
ChatGPT Conversation Scanner
Handles ChatGPT's tree-based message structure with proper traversal.
Usage: python chatgpt-scanner.py PATH_TO_CONVERSATIONS_JSON
"""

import json
import sys
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
                messages.append({
                    'role': role,
                    'text': text,
                    'time': msg.get('create_time')
                })
        children = node.get('children', [])
        current_id = children[0] if children else None
    return messages


def scan_chatgpt(filepath):
    """Scan ChatGPT conversations.json and extract metadata."""
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
    print(f"\nTop 50 by message count:")
    for i, c in enumerate(results[:50]):
        print(f"  {i+1}. [{c['messages']} msgs] {c['title']} ({c['created'][:10] if c['created'] else 'no date'})")
