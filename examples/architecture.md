# Architecture (long form)

This file is the prose version of `assets/architecture.png`. The diagram is a placeholder; this text is the source of truth until the diagram is redrawn from a vector tool.

## Components

### Encoder
Maps a single observation (a video frame, a sensor window, an agent state) to a latent vector `z ∈ ℝ^d`. We pin `d = 256` for the first cut. The encoder is **frozen** during predictor training so the latent space stays stable across runs.

### Predictor
A small autoregressive transformer over the latent stream. Input is `z_{t-k:t}`, output is `ẑ_{t+1}`. There is **no decoder in the loss** — we train the predictor on the latent-space loss directly. This is the JEPA flavor of the world model.

### Decoder (debug only)
Optional. Used by the UI to render `ẑ` back to pixels for human-readable previews. It is never on the critical path.

### Latent Memory
A versioned store of `(session_id, step, z)` triples plus the rollout branches that diverge from them. Treat it like git for latents: every fork has a parent, every state is hashed, and you can replay any path.

### Browser Runtime (Latens UI)
What you see on the screenshot. Three panels:

- **Sessions** — left rail, one entry per world-model run.
- **Latent flow** — top-right, the time-series of `z_norm` / `delta` for the active session, clickable to seek.
- **Logs** — bottom-right, streaming structured events from the runtime.

## Data flow

```
observation ──▶ Encoder ──▶ z_t ──▶ Predictor ──▶ ẑ_{t+1}
                              │           │
                              ▼           ▼
                        Latent Memory  Loss (latent-space)
                              │
                              ▼
                          Browser UI
```

## Open questions

- How do we keep the encoder genuinely frozen across long-running labs without freezing *progress*? (Versioned encoders + lineage on the session manifest is the current bet.)
- What's the right horizon `H` for the predictor — fixed, curriculum, or adaptive?
- Does the Browser UI need a "compare two rollouts side by side" mode, or is parent/child diff enough?
