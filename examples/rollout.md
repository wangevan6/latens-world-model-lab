# Example: a latent rollout trace

A *rollout* is what the predictor does when you hand it a starting latent `z_t` and ask it to walk forward `H` steps without seeing the real frames. The trace below is a toy of that.

```jsonl
{"step": 0,  "z_norm": 1.02, "delta": 0.000, "mse_vs_real": 0.000, "note": "anchor"}
{"step": 1,  "z_norm": 1.04, "delta": 0.018, "mse_vs_real": 0.004}
{"step": 2,  "z_norm": 1.05, "delta": 0.022, "mse_vs_real": 0.006}
{"step": 3,  "z_norm": 1.07, "delta": 0.025, "mse_vs_real": 0.009}
{"step": 4,  "z_norm": 1.11, "delta": 0.041, "mse_vs_real": 0.018, "note": "cabinet-open frame"}
{"step": 5,  "z_norm": 1.18, "delta": 0.073, "mse_vs_real": 0.037, "note": "predictor surprised"}
{"step": 6,  "z_norm": 1.14, "delta": 0.044, "mse_vs_real": 0.022, "note": "recovers"}
{"step": 7,  "z_norm": 1.10, "delta": 0.038, "mse_vs_real": 0.016}
{"step": 8,  "z_norm": 1.08, "delta": 0.028, "mse_vs_real": 0.012}
```

## How to read this

- **`z_norm`** — L2 norm of the predicted latent. Drift here usually means the predictor is wandering outside the training manifold.
- **`delta`** — `‖z_t − z_{t-1}‖`. Spikes correlate with scene changes in the source stream.
- **`mse_vs_real`** — only available when you also encoded the real frame. This is the *closed-loop* error.
- **`note`** — free-form anchor for "what was happening on screen." The Latens UI lets you click these to jump to the source frame.

## What "good" looks like

For a well-trained world model, you want:

1. `delta` to track the *real* per-step change, not zero (a frozen latent is not a useful prediction).
2. `mse_vs_real` to grow slowly with the rollout horizon, not explode after 2–3 steps.
3. Recovery after surprises (step 6 above): the predictor should pull back toward the real trajectory once it gets new evidence.
