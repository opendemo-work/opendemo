---
title: Iterative Refinement
category: skills
tags: [ai, coding, iteration, vibe-coding]
sources: [/Users/allengaller/Documents/GitHub/opendemo-work/opendemo/vibe-coding/VIBE-CODING-PLAN.md]
summary: A vibe-coding technique that builds software incrementally through multiple AI-assisted iterations rather than attempting complete solutions in one prompt.
provenance:
  extracted: 0.6
  inferred: 0.4
  ambiguous: 0.0
base_confidence: 0.55
lifecycle: draft
lifecycle_changed: 2026-06-03
tier: supporting
created: 2026-06-03T05:33:46Z
updated: 2026-06-03T05:33:46Z
---

# Iterative Refinement

Iterative refinement is a core [[vibe-coding]] technique that builds software incrementally through multiple AI-assisted iterations.

## Core Approach

Rather than asking AI to build a complete system in one prompt, iterative refinement:

1. **Skeleton First** — Get the basic structure and interfaces
2. **Fill Incrementally** — Add features one at a time
3. **Test Each Iteration** — Verify before proceeding
4. **Refine Based on Feedback** — Use AI errors and test failures to guide next steps

## Why It Works

AI coding tools perform better on focused, incremental tasks than on large, complex requests. Each iteration provides context that improves subsequent responses. ^[inferred]

## Iteration Patterns

### Basic Pattern
```
Round 1: Basic structure → Review → Issues
Round 2: Fix issues → More features → Test
Round 3: Refine → Polish → Complete
```

### Test-Driven Pattern
```
1. Define test cases first
2. Ask AI to implement to pass tests
3. Run tests, collect errors
4. Prompt AI to fix specific errors
5. Repeat until tests pass
```

### Debug-Driven Pattern
```
1. Get initial implementation
2. Run tests or use the code
3. Capture errors verbatim
4. Ask AI to fix specific error
5. Repeat with new errors
```

## Common Pitfalls

- **Skipping iterations** — Trying to fix too many issues in one prompt
- **Not running tests** — Assuming AI code works without verification
- **Lost context** — Starting new conversations instead of continuing

## Learning Path Integration

Iterative refinement is taught as part of [[skills/prompt-engineering]] fundamentals and practiced in the [[concepts/vibe-coding]] challenge sessions where SOLUTION.md files document real iteration sequences.

## Related

- [[skills/prompt-engineering]] — Prompt writing techniques
- [[skills/ai-debugging]] — Debugging with AI
- [[concepts/vibe-coding]] — Learning methodology
- [[references/opendemo-project]] — Project context
