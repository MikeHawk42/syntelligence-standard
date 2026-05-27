# Examples

## sample-session.jsonl

A complete DISCOVER-phase session on clinical triage reasoning. The session explores decision-making under uncertainty with an unreliable historian, symptom-acuity decoupling in high-risk patients, and treatment commitment when two leading diagnoses have contradictory management pathways.

The session_id has been replaced with a zero UUID. All other content is unmodified.

### Viewing the session

Print each event as formatted JSON:

```bash
python3 -c "
import json, sys
for line in open('examples/sample-session.jsonl'):
    line = line.strip()
    if line:
        print(json.dumps(json.loads(line), indent=2))
        print()
"
```

Or filter to a specific event type:

```bash
python3 -c "
import json
for line in open('examples/sample-session.jsonl'):
    line = line.strip()
    if not line:
        continue
    e = json.loads(line)
    if e['type'] == 'breadth_move':
        print(f\"--- Turn {e['turn']} | {e['move_type']} ---\")
        print(e['content'])
        print()
"
```

Or view just the reframing chain from the session end event:

```bash
python3 -c "
import json
for line in open('examples/sample-session.jsonl'):
    line = line.strip()
    if not line:
        continue
    e = json.loads(line)
    if e['type'] == 'session_end':
        for r in e['reframing_chain']:
            print(f\"Turn {r['turn']}: {r['prior_framing']}\")
            print(f\"  -> {r['new_framing']}\")
            print()
"
```
