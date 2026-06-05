---
title: AI Debugging
category: skills
tags: [ai, debugging, coding, vibe-coding]
sources: [/Users/allengaller/Documents/GitHub/opendemo-work/opendemo/vibe-coding/README.md]
summary: Five debugging patterns when using AI coding tools, including error verbatim, context isolation, test-driven debugging, and meta-debugging approaches.
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

# AI Debugging

AI debugging is the practice of using AI tools to identify, understand, and fix code errors through structured interaction patterns.

## Five Debug Patterns

### 1. Error Verbatim Pattern
Copy exact error messages into the prompt rather than paraphrasing.

**Example:**
```
"The test failed with: 'panic: runtime error: index out of range [3] with length 2'"
"Fix this specific error"
```

### 2. Context Isolation Pattern
Reduce the problem to minimal reproducible code before prompting AI.

**Example:**
```
"Isolate the issue to this function: [code]. The error occurs when calling it with [input]."
```

### 3. Test-Driven Debugging
Write tests that reproduce the bug, then use AI to fix.

**Example:**
```
"Write a test that reproduces the bug: [description]. Then fix the code to pass."
```

### 4. Step-by-Step Execution
Ask AI to explain execution flow to find where behavior diverges from expectation.

**Example:**
```
"Trace through this function with input X step by step"
```

### 5. Meta-Debugging
When stuck, ask AI to critique its own approach.

**Example:**
```
"This fix didn't work. What's another approach to this problem?"
```

## Common AI Debugging Mistakes

- **Summarizing errors** — AI works best with exact error text
- **Too much context** — Isolating the bug helps AI focus
- **Vague "it doesn't work"** — Specify expected vs actual behavior
- **Fixing too many issues at once** — One issue at a time

## Key Insight

The distinction between prompting AI to write code versus debugging code requires different techniques. Debugging benefits from precision (exact errors, minimal context) while writing benefits from broader context (goals, patterns, examples). ^[inferred]

## Related

- [[skills/prompt-engineering]] — Prompt writing techniques
- [[skills/iterative-refinement]] — Iterative improvement
- [[concepts/vibe-coding]] — Learning methodology
