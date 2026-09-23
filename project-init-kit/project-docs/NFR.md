---
created: 2026-09-08T17:38:40Z
updated: 2026-09-11T14:49:25Z
---

# NFR.md — [Project Name]

**Answers:** What quality bar must this product meet?
**Depends on:** `PRD.md` (companion document, not a subset of it).

> **Status: starter structure.** ISO 25010 model, generic — little needs generalizing here, but every question still deserves a real answer for THIS project, not a generic one that would fit any project.

---

## Performance

> 1. What response time would feel broken to a real user?
> 2. Is there a known peak-load moment?
> 3. What's actually being measured — page load time, API latency, something else?

## Reliability / Availability

> 1. What does "down" mean for this product, precisely?
> 2. Is any downtime acceptable, and when?
> 3. What's the plan if a dependency this relies on goes down?

## Scalability

> 1. What happens if usage grows 10x overnight?
> 2. Which resource runs out first?
> 3. Is scale a real near-term risk here, or a hypothetical for V1?

## Security

> 1. What's the most sensitive thing this system holds?
> 2. Who should never be able to access it?
> 3. What's the worst-case breach scenario, and is it survivable?

## Usability / Accessibility

> 1. Who might struggle to use this as designed — device, language, ability?
> 2. Is there a minimum accessibility standard being targeted?
> 3. What's the simplest task a first-time user must be able to complete unaided?

## Compatibility

> 1. What environments (browsers, devices, OS) must this actually work on?
> 2. Is there an environment explicitly not supported?
> 3. Does it need to interoperate with any existing system?

## Compliance / Legal

> 1. What regulation applies to this data or this audience?
> 2. What consent or disclosure is legally required before collecting data?
> 3. Who is liable if this goes wrong?

## Maintainability

> 1. How easy is it for a future person, including future-you, to change this safely?
> 2. What's the plan for keeping documentation in sync with code?
> 3. Is there a test suite, and what does it actually cover?

## Portability

> 1. Could this move to a different host without a full rewrite?
> 2. Is anything hard-coded to one vendor that shouldn't be?

## Observability / Monitoring

> 1. What would you want alerted on immediately if it broke?
> 2. What's logged today versus what should be?
> 3. Who's actually watching this?

## Disaster Recovery / Backup

> 1. What's the worst data-loss scenario, and how would you recover from it?
> 2. How often is data backed up, and has a restore ever actually been tested?
> 3. What's the acceptable amount of data loss (RPO) and downtime (RTO)?

## Risks and Mitigations

> 1. What's most likely to go wrong before this ships?
> 2. For each risk, what's the plan if it happens anyway?
> 3. Which risk, if it happened, would be hardest to recover from?

## Dependencies

> 1. What external services, libraries, or people does this rely on to function?
> 2. What happens if one becomes unavailable or changes its API?
> 3. Is there a single point of failure among these?

---

*NFR.md — [Project Name] — starter structure from `project-init-kit/`.*
