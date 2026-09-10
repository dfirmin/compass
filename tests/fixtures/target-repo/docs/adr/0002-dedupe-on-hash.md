---
type: ADR
title: "Dedupe policy snapshots on a content hash"
description: "A surrogate hash of the full record decides duplicates."
adr_status: accepted
status: stable
generated: { by: compass/domain-modeling, at: 2026-09-10T20:10:00Z }
verified: { by: human:dfirmin, at: 2026-09-10T20:10:00Z }
---
# Dedupe policy snapshots on a content hash

Natural keys collided on late-arriving corrections; a content hash does not.
