# Example: a Latens session manifest

A *session* is a single run of a world model on a stream — encoder + predictor + the trace of latents it produced. The manifest is the human-readable header that points at the binary artifacts.

```yaml
id: world-07
created_at: 2026-05-07T18:30:00Z
seed: 42

source:
  kind: video
  uri: file://datasets/clips/kitchen_07.mp4
  fps: 30
  frames: 1800

model:
  encoder: jepa-v2-small
  predictor: latent-transformer-128
  latent_dim: 256
  horizon: 16

artifacts:
  latents: artifacts/world-07/z.npy        # shape: (1800, 256)
  rollouts: artifacts/world-07/rollouts/   # one file per branch
  metrics: artifacts/world-07/metrics.json

notes: |
  First clean run after fixing the encoder normalization bug.
  The 14:00–18:00 region is the interesting one — predictor diverges
  on the cabinet-open frame and recovers two steps later.
```

## How to read this

- **`id`** is stable; you can link to it from issues, papers, or the UI.
- **`source`** is the raw observation stream. Latens never modifies it.
- **`model`** is enough to reproduce the encoder and predictor versions.
- **`artifacts`** are the binary outputs — the manifest is just the index.
- **`notes`** are free-form. Write the things a future reader would have to dig through logs to find.

Manifests are append-only. To "edit" a session, fork it: copy the manifest, change the model or seed, give it a new `id`, and link `parent: world-07` so the lineage survives.
