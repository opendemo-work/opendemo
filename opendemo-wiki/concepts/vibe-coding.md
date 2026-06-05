---
title: Vibe Coding
category: concepts
tags: [ai, coding, prompt-engineering, learning]
relationships:
  - target: "[[concepts/five-star-standard]]"
    type: related_to
sources: [/Users/allengaller/Documents/GitHub/opendemo-work/opendemo/vibe-coding/README.md, /Users/allengaller/Documents/GitHub/opendemo-work/opendemo/vibe-coding/VIBE-CODING-PLAN.md]
summary: A hands-on methodology for learning AI-assisted coding by reproducing technical demos using AI tools like Cursor, Claude Code, and Copilot, structured as challenges with solutions.
provenance:
  extracted: 0.75
  inferred: 0.25
  ambiguous: 0.0
base_confidence: 0.65
lifecycle: draft
lifecycle_changed: 2026-06-03
tier: core
created: 2026-06-03T05:33:46Z
updated: 2026-06-03T05:33:46Z
---

# Vibe Coding

Vibe Coding is a hands-on learning methodology that transforms OpenDemo's 638+ technical demonstrations into practical exercises using AI coding tools.

## Core Concept

Rather than teaching how to deploy AI tools, vibe coding teaches how to **effectively use AI coding tools** to build real software. Each challenge provides only requirements and verification criteria—no code is provided upfront. ^[inferred]

## Learning Path

```
getting-started/ → fundamentals/ → practices/ → advanced/
```

### Level 1: Tool Selection (getting-started/)

| Tool | Best For |
|------|----------|
| Cursor | Daily development with Cmd+K inline editing |
| Claude Code | Terminal-based autonomous coding |
| Copilot | VS Code users wanting inline completions |
| Cline | Complex tasks requiring autonomous execution |
| Windsurf | Large tasks requiring multi-step reasoning |

### Level 2: Fundamentals (5 topics)

| Topic | Content |
|-------|---------|
| [[skills/prompt-engineering]] | Five effective prompt patterns + anti-patterns |
| [[skills/iterative-refinement]] | Skeleton → fill, test-driven, imitation → creation |
| [[skills/ai-debugging]] | Five debug patterns + meta-techniques |
| testing-with-ai | Four test generation methods + common pitfalls |
| code-review-with-ai | Three review modes + checklist |

### Level 3: Practices (10 challenges across 4 stacks)

**Go (4 challenges):**
- Cobra CLI — Building CLI step by step
- Gin Web — REST API development
- gRPC + Protobuf — Microservices communication
- Docker SDK — DevOps automation

**Python (3 challenges):**
- OOP — Object-oriented programming basics
- Async — Asynchronous programming
- FastAPI — Full-stack web development

**Node.js (2 challenges):**
- Closures — Functional programming
- Circuit Breaker — Fault tolerance patterns

**Kubernetes (1 challenge):**
- n8n Deployment — Production K8s deployment

### Level 4: Advanced (4 topics)

- MCP Integration — Connecting AI to databases, GitHub, filesystem
- Multi-file Refactoring — One prompt modifying 5+ files
- Cross-stack Project — Frontend + backend + deployment
- Legacy Migration — Migrating old code to new stacks

## Challenge Format

Each practice includes:

- **CHALLENGE.md** — Requirements, constraints, verification criteria, hints
- **SOLUTION.md** — Complete AI coding process with every prompt, error, and fix
- **prompts/** — Actual prompt sequence used

## Key Insight

The 518 existing OpenDemo demos serve as ready-made exercise problems. The challenge is not creating content but converting existing high-quality demos into a teachable format. ^[inferred]

## Related

- [[references/opendemo-project]] — OpenDemo project overview
- [[concepts/five-star-standard]] — Quality standard for demo documentation
- [[skills/prompt-engineering]] — Prompt techniques
- [[skills/ai-debugging]] — Debugging with AI
- [[entities/tech-stacks]] — Technology stacks for challenges
