---
name: job-analysis
description: Analyze a job description and map it to resume revision priorities for internet industry roles, especially product manager, product design, UX, interaction design, and AI product positions. Use when Codex needs to break down a single JD, evaluate a resume against a JD, identify HR initial-screen signals, extract core competencies, infer hidden expectations, prioritize application focus areas, or suggest concrete resume edits for stronger relevance.
---

# Job Analysis

## Overview

Use this skill to convert a JD into an application strategy. Focus on what matters for HR screening, hiring-manager interest, and resume relevance rather than restating the JD.

Default to internet industry hiring logic. Bias toward product manager, product design, UX design, interaction design, and AI-related product roles unless the user specifies a different domain.

## Workflow

### 1. Normalize the input

Determine which of these cases applies:
- JD only
- Resume plus JD
- Multiple versions of the same resume plus JD

If the JD is messy, first rewrite it into structured fields:
- Role title
- Company or team context if present
- Core responsibilities
- Hard requirements
- Preferred requirements
- Seniority signals
- AI or domain signals
- Tool, method, or platform keywords

### 2. Identify the real screening logic

Extract what will actually decide the first two hiring steps.

Separate signals into:
- Must-have signals: If absent, the candidate is likely screened out
- Strong differentiators: Signals that materially improve shortlist odds
- Hidden expectations: Not stated directly, but implied by wording, seniority, scope, or business context
- Noise: Requirements that appear in the JD but should not dominate resume edits

Pay special attention to:
- Ownership verbs such as define, lead, drive, build, launch, optimize
- Scope markers such as end-to-end, cross-functional, strategy, roadmap, system-level
- Evidence markers such as metrics, experimentation, growth, conversion, retention, efficiency
- Collaboration markers such as engineers, researchers, data, operations, business
- AI markers such as LLM, AI workflow, prompt design, model capability, human-in-the-loop, agent, automation

For product and UX roles, read [references/screening-signals.md](./references/screening-signals.md). For AI-product positioning, also read [references/ai-role-signals.md](./references/ai-role-signals.md).

### 3. Build the JD analysis report

Unless the user asks for a different format, structure the report in this order:
1. Role summary in 2 to 4 sentences
2. Core hiring priorities
3. HR initial-screen checklist
4. Hidden expectations and inferred evaluation criteria
5. Keywords and phrasing worth mirroring in the resume
6. Application focus: what the candidate should emphasize when applying
7. Risks or likely rejection reasons

Keep it specific. Avoid generic advice like "show communication skills" unless the JD provides evidence for it.

### 4. Translate the analysis into resume edits

When a resume is provided, evaluate the resume against the JD in these dimensions:
- Role alignment
- Domain alignment
- Scope and ownership
- Outcome and metrics evidence
- Collaboration and stakeholder evidence
- AI or emerging-tech relevance when applicable
- Keyword coverage
- Seniority fit

Then produce targeted resume guidance:
- Keep: content already aligned with the JD
- Rewrite: bullets that should be reframed with stronger wording
- Add: missing signals that can be truthfully supported by existing experience
- Downplay or remove: content that consumes space but does not support this application
- Summary strategy: what the top section of the resume should signal
- Project selection: which projects or cases deserve more or less space

Prefer rewriting into evidence-backed bullets, not keyword stuffing. If a recommendation cannot be supported by the user's real experience, label it as a gap rather than suggesting fabrication.

When useful, output a table with:
- JD requirement
- Resume evidence today
- Gap level
- Recommended rewrite or addition

### 5. State the user's application focus clearly

Always include a short section answering:
- What should the user pay attention to before applying?
- Which 3 to 5 signals should the resume lead with?
- What might HR reject quickly?
- What story should the candidate tell about themselves for this role?

If the role is AI-related, clarify whether the role expects:
- AI product strategy
- AI feature design
- AI workflow design
- model/application integration experience
- hands-on experimentation and shipping evidence

### 6. Adapt depth to the user request

Use shorter output when the user wants a quick screen.
Use the full report when the user asks how to optimize a resume or prepare an application.

If the user only shares a JD, still provide:
- likely screening logic
- ideal candidate profile
- resume revision priorities
- what evidence the user should surface from past work

## Output standard

Default to a practical report in Chinese unless the user asks for English.

Use this structure:
- JD analysis report
- Application focus
- Resume revision recommendations
- Optional matching assessment if a resume is provided

Use the template in [assets/jd-analysis-report-template.md](./assets/jd-analysis-report-template.md) when the user wants a consistent deliverable.

## Quality bar

Do not merely paraphrase the JD.

Make defensible inferences, but label them as inferred when they are not explicit in the JD.

Anchor recommendations in hiring logic:
- Why this signal matters
- Where the JD indicates it
- How the resume should reflect it

Do not advise the user to invent tools, domains, metrics, or AI experience they do not have.
