---
title: Vibe Coding Learning Path
category: references
tags: [learning, vibe-coding, ai, tutorial]
relationships:
  - target: "[[references/opendemo-project]]"
    type: related_to
  - target: "[[concepts/vibe-coding]]"
    type: related_to
sources: [/Users/allengaller/Documents/GitHub/opendemo-work/opendemo/vibe-coding/README.md]
summary: A structured learning path for mastering AI-assisted coding, progressing from tool selection through fundamentals to hands-on practice across Go, Python, Node.js, and Kubernetes.
provenance:
  extracted: 0.8
  inferred: 0.2
  ambiguous: 0.0
base_confidence: 0.65
lifecycle: draft
lifecycle_changed: 2026-06-03
tier: supporting
created: 2026-06-03T05:33:46Z
updated: 2026-06-03T05:33:46Z
---

# Vibe Coding Learning Path

A structured progression for learning AI-assisted coding using OpenDemo's challenge framework.

## Learning Progression

```
getting-started/ → fundamentals/ → practices/ → advanced/
   ↑                                                        ↓
   └──────────── getting-started/ ←─────────────────────────┘
```

## Stage 1: Tool Selection (getting-started/)

Choose an AI coding tool based on your workflow:

| Tool | Strength | Best For |
|------|----------|----------|
| Cursor | IDE integration | Daily development |
| Claude Code | CLI autonomy | Terminal-focused workflows |
| Copilot | Inline completions | VS Code users |
| Cline | Autonomous execution | Complex multi-step tasks |
| Windsurf | Cascade reasoning | Large refactoring projects |

## Stage 2: Fundamentals (fundamentals/)

Five core techniques:

1. **Prompt Engineering** — Writing effective prompts for code generation
2. **Iterative Refinement** — Building incrementally with AI feedback
3. **AI Debugging** — Using AI to diagnose and fix errors
4. **Testing with AI** — Generating test cases automatically
5. **Code Review with AI** — Using AI to review code quality

## Stage 3: Practices (practices/)

### Challenge Stack Overview

| Stack | Challenges | Skills Practiced |
|-------|------------|------------------|
| Go | 4 | CLI, REST API, gRPC, DevOps |
| Python | 3 | OOP, Async, FastAPI |
| Node.js | 2 | Closures, Circuit Breaker |
| Kubernetes | 1 | Production deployment |

### Challenge Levels

- **Beginner** (20-25 min): OOP, Closures
- **Intermediate** (20-35 min): CLI, REST API, Async, FastAPI, n8n
- **Advanced** (35-45 min): gRPC, Docker SDK, Circuit Breaker

## Stage 4: Advanced (advanced/)

Four advanced topics:

- **MCP Integration** — Connect AI to external systems
- **Multi-file Refactoring** — Large-scale changes
- **Cross-stack Project** — Full-stack development
- **Legacy Migration** — Modernizing old codebases

## Usage Modes

### Follow-Along Mode (Beginners)
1. Open CHALLENGE.md
2. Code with AI tool
3. Check hints if stuck
4. Compare with SOLUTION.md

### Challenge Mode (Experienced)
1. Read only objectives and constraints
2. Complete independently
3. Compare approach with SOLUTION.md

### Problem-Setting Mode (Advanced)
1. Select an OpenDemo demo
2. Create CHALLENGE.md
3. Complete with AI, record in SOLUTION.md
4. Submit as PR

## Related

- [[references/opendemo-project]] — OpenDemo project context
- [[concepts/vibe-coding]] — Vibe coding concept and methodology
- [[skills/prompt-engineering]] — Prompt techniques
- [[skills/ai-debugging]] — Debugging with AI
- [[entities/tech-stacks]] — Technology stacks covered
