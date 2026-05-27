# Contributing

## Reporting a bug

Open a GitHub issue. Include what you typed, what the system produced, and what you expected instead. If the bug is in a session, paste the relevant JSONL lines.

## Sharing a session result

Open a GitHub Discussion. Paste the anonymized session log (replace your session UUID with a placeholder if you prefer) and describe what the session revealed — a protocol gap, an unexpected reframing, a failure mode worth documenting. Raw logs without commentary are also welcome.

## Proposing a protocol change

Use the SEP format from the standard (Section 11):

- **SEP-NNN: Title**
- **Motivation:** What problem does this address? What evidence or session log surfaces it?
- **Proposal:** The specific change — new rule, modified threshold, revised template.
- **Test:** How would you know if the change worked? What session result would validate it?

Open a GitHub Discussion with the SEP label. Changes to the core protocol require at least one supporting session log demonstrating the failure mode the change addresses.
