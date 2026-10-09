# First release checklist

This repository starts without a public channel pointer. Do not add empty manifests or sample ZIP files: the promotion workflow creates the first signed pointer from the selected artifact. The public site intentionally shows an unpublished channel until then.

## One-time state

- `main` contains the public site, `manifest.schema.json`, and the Pages workflow.
- There are no historical public releases or tags that collide with the first intended tag, for example `stable/v0.4.0`.
- The GitHub Pages site is enabled and the **Release page** workflow can deploy from `main`.
- Release immutability is enabled for this repository.
- The publishing token used by the source repository can create tags and releases and push the signed channel pointers to this repository's `main` branch.

## First STABLE (0.4.0 bootstrap)

1. In the source repository, run **Build TEST** from `main` and wait for every test and `finalize-test` to pass.
2. Download and inspect the inner add-on ZIP from the TEST artifact.
3. Run the bootstrap **Promote STABLE** workflow from `main` and select the exact `TEST …` candidate.
2. Approve the protected `stable` environment.
3. Verify the new immutable STABLE release `vX.Y.Z`, unchanged ZIP SHA-256, `stable/manifest.json`, and the Pages download card.

The bootstrap reuses already-tested ZIP bytes and creates no new build. Later releases use TEST → BETA → STABLE.
