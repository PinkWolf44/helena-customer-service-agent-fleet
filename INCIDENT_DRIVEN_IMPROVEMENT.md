# Incident-Driven Improvement

## Pattern: an unsupported logistics claim

An agent once produced a confident carrier explanation that was not present in the available records. The reply sounded plausible, so tone review alone would not catch it.

The permanent correction had three layers:

1. **Rule:** carrier, hub and route claims must come from an authoritative record.
2. **Fallback:** when the record is missing, state the known status and hand off without inventing a cause or promising personal follow-up.
3. **Regression test:** give the agent an incomplete synthetic record and fail the test if it supplies any unsupported carrier detail.

## Why the baseline matters

Without a saved test, a later prompt cleanup or token optimisation can reintroduce the same failure. The regression suite preserves operational memory outside any individual conversation.

## A second lesson: context optimisation can remove rules

The system experimented with loading references only when needed. That reduced the starting context but created a new failure mode: an unavailable or forgotten reference could silently remove a necessary rule.

The architectural response is not “always load everything.” It is to define:

- a small mandatory safety kernel;
- explicit reference dependencies per classification;
- a failure path when a required reference cannot be loaded;
- baseline tests that simulate missing references;
- one unambiguous precedence rule for thread depth.

This is the kind of production feedback that turns prompt writing into agent engineering.
