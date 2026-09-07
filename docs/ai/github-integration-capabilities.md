# GitHub integration capabilities

Audited on 2026-09-07 against `aneq05/coding_assistant_demo_repo` at remote
`main` commit `6209ad5791eca5213f537f7b1e87a5d83a85e7bc`.

This was a read-only audit. `gh` was authenticated as `aneq05`; the repository
reported `ADMIN` viewer permission and token scopes `repo` and `workflow`.
Those facts indicate potential write authority, but this audit did not probe
any mutation. A separate GitHub MCP tool surface was not available in this
session; the evidence below comes from the authenticated GitHub CLI/API.

| Area | Capability | Classification | Evidence / boundary |
| --- | --- | --- | --- |
| Repository | Read repository identity, default branch, and viewer permission | READ | `gh repo view` returned the private repository, `main`, and `ADMIN`. |
| Branches | List remote branches and their protection metadata | READ | Seven branches, including `main`, were returned. |
| Branches | Create, update, or delete remote branches | WRITE | Prior worklog entries record pushes and dedicated-branch delivery; not exercised in this audit. |
| Issues | List repository Issues | READ | The all-state query returned no Issues. |
| Issues | Create, edit, comment on, or close Issues | NOT VERIFIED | Deliberately not attempted; no Issue was created. |
| Pull requests | List PRs and inspect metadata/diffs | READ | All six PRs were retrieved; each is merged. |
| Reviews | Read submitted PR reviews | READ | PR #6 review submissions, reviewers, timestamps, and reviewed commit IDs were retrieved. |
| Pull requests and reviews | Create/update PRs; submit comments; reply to or resolve threads | WRITE | Prior worklog evidence records draft-PR creation and review-thread responses; not re-exercised here. |
| Actions | List workflow runs and inspect jobs | READ | Current `main` run `34138540854` and its successful `Python validation` job were retrieved for `6209ad5`. |
| Actions | Dispatch, rerun, cancel, or edit workflows | NOT VERIFIED | Not attempted in this read-only audit. |
| Artifacts | List artifact metadata | READ | 20 non-expired validation-report artifacts were returned. |
| Artifacts | Download artifact contents | NOT VERIFIED | Metadata was read; archive download was intentionally not attempted. |
| GitHub MCP | Use a dedicated GitHub MCP server/tool surface | UNAVAILABLE | No such tool was exposed in this session; authenticated `gh` provided the read integration instead. |

No capability was found to be unavailable within the authenticated GitHub CLI
integration itself. `UNAVAILABLE` above is limited to the distinct GitHub MCP
tool surface.

## Short harness retrospective

- **Duplicated or stale guidance:** `AGENTS.md` and several Git workflow
  Skills repeat the human-merge boundary. The repetition is a deliberate
  safety guard, but the roadmap's planned GitHub MCP integration did not
  distinguish a dedicated MCP surface from the already working authenticated
  GitHub CLI integration. This document supplies that distinction; no routing
  changes are justified yet.
- **Missing persistent knowledge:** The repository lacked a dated record of
  what GitHub operations are actually observable, which ones have historical
  write evidence, and which mutations remain intentionally unverified. This
  document is the smallest durable record. Re-audit it after credential,
  connector, or repository-permission changes.
- **Unnecessary complexity:** Do not add a GitHub-specific Skill, extra
  permission probes, or a separate issue/PR workflow from this snapshot. The
  existing delivery, review, and PR-validation Skills already cover the
  justified write workflows; this audit is a compact reference, not a new
  automation layer.
