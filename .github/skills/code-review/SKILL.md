---
name: code-review
description: Generate concrete, repository-aware findings when reviewing a Coffee-Driven Development pull request. Use for pull-request code review, not for validating review feedback or final pull-request readiness.
---

# Coffee-Driven Development code review

Review pull requests to generate useful findings. This Skill does not decide
whether a finding is accepted and does not determine final pull-request
readiness. Those responsibilities belong to `validate-review-feedback` and
`validate-pull-request` respectively.

1. Establish the pull request's goal, current HEAD SHA, base branch, metadata,
   complete changed-file set, repository architecture, and applicable roadmap
   phase. Read `AGENTS.md`, the Python guidelines, testing strategy, and the
   relevant section of `docs/IMPLEMENTATION_PLAN.md`.
2. When relevant context is available, use the GitHub context or GitHub MCP to
   inspect only the current pull request: its current HEAD and base, changed
   files, explicitly referenced Issues, current-HEAD Actions results and
   accessible validation artifacts, and existing review threads. Do not explore
   unrelated repository data. Do not assume a successful run for an older SHA
   validates the current HEAD.
3. Prioritize concrete correctness defects, regressions, meaningful test gaps,
   typing or lint problems, architecture-boundary violations, CI workflow
   problems, documentation inconsistencies, current-scope leakage, and genuine
   security issues. Prefer no finding to a speculative one.
4. Respect the deliberately small architecture. Do not recommend service
   layers, repository interfaces, dependency injection, frameworks, ORMs,
   databases, plugin systems, or future roadmap features unless the pull
   request itself makes such a change necessary.
5. Check existing threads before commenting. Do not repeat a finding already
   reported, handled, or rejected with valid reasoning.
6. Make every actionable finding concise and specific: state what is wrong,
   cite the relevant change or current evidence, explain why it matters, and
   propose the smallest reasonable correction. Do not claim CI or tool use that
   the available current-HEAD evidence does not establish.
