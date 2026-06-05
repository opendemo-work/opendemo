---
title: Prompt Engineering
category: skills
tags: [ai, prompts, coding, vibe-coding]
sources: [/Users/allengaller/Documents/GitHub/opendemo-work/opendemo/vibe-coding/README.md, /Users/allengaller/Documents/GitHub/opendemo-work/opendemo/vibe-coding/VIBE-CODING-PLAN.md]
summary: Five effective prompt patterns for AI-assisted coding, including skeleton-first, constraint-based, test-driven, imitation, and multi-step refinement approaches.
provenance:
  extracted: 0.7
  inferred: 0.3
  ambiguous: 0.0
base_confidence: 0.6
lifecycle: draft
lifecycle_changed: 2026-06-03
tier: supporting
created: 2026-06-03T05:33:46Z
updated: 2026-06-03T05:33:46Z
---

# Prompt Engineering

Prompt engineering is a fundamental skill in [[vibe-coding]] that determines how effectively AI tools assist with coding tasks.

## Five Effective Prompt Patterns

### 1. Skeleton-First Approach
Start with a minimal structure, then progressively fill in details. This prevents AI from generating overly complex initial solutions.

**Example pattern:**
```
"Create a basic REST API structure with Express"
"Add authentication middleware"
"Add error handling"
```

### 2. Constraint-Based Prompting
Explicitly state constraints to guide AI toward the desired solution.

**Example pattern:**
```
"Implement X using only standard library"
"Make it work with Node.js 18+"
"Ensure it handles concurrent requests"
```

### 3. Test-Driven Generation
Provide test cases first, let AI implement to meet them.

**Example pattern:**
```
"Write tests for a worker pool with 5 workers"
"Then implement the worker pool to pass these tests"
```

### 4. Imitation Pattern
Show AI a similar working example to guide the new implementation.

**Example pattern:**
```
"Like the previous auth middleware we wrote, but add JWT support"
```

### 5. Multi-Step Refinement
Iterate with progressively detailed prompts rather than asking for everything at once. ^[inferred]

**Example pattern:**
```
"Create a basic structure"
"Add error handling"
"Add logging"
"Optimize performance"
```

## Anti-Patterns to Avoid

- **Vague requests** — "Write a web server" is less effective than specifying framework, ports, error handling
- **Over-specification** — Constraining too tightly can prevent AI from suggesting better approaches
- **Single massive prompt** — Breaking into smaller prompts yields better results

## Key Insight

The SOLUTION.md files in [[concepts/vibe-coding]] practices record actual prompt sequences showing what works in real coding sessions. These provide templates for effective prompt writing. ^[inferred]

## Related

- [[concepts/vibe-coding]] — Learning methodology
- [[skills/iterative-refinement]] — Iterative improvement techniques
- [[skills/ai-debugging]] — Debugging with AI
- [[references/opendemo-project]] — Project context
