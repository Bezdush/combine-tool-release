# First release checklist

This repository may start without a BETA or STABLE channel pointer. Do not add empty manifests or sample ZIP files: the promotion workflows create the first signed pointers from the selected artifact. The public site intentionally shows an unpublished channel until then.

## One-time state

- `main` contains the public site, `manifest.schema.json`, and the Pages workflow.
- There are no historical public releases or tags that collide with the first intended tags, for example `beta/v0.3.112-beta.1` and `stable/v0.3.112`.
- The GitHub Pages site is enabled and the **Release page** workflow can deploy from `main`.
- Release immutability is enabled for this repository.
- The publishing token used by the source repository can create tags and releases and push the signed channel pointers to this repository's `main` branch.

## First BETA

1. In the source repository, run **Build TEST** from `main` and wait for every test and `finalize-test` to pass.
2. Download and inspect the inner add-on ZIP from the TEST artifact.
3. Run **Promote BETA** from `main`, select the exact `TEST …` candidate from the environment dropdown, then approve the protected `beta` environment.
4. Verify the new immutable BETA release, its ZIP digest, `channel-manifest.json`, the `beta/manifest.json` pointer, and the Pages download card.

## First STABLE

1. Run **Promote STABLE** from the source repository's `main` and enter the exact BETA tag.
2. Approve the protected `stable` environment.
3. Verify the new immutable STABLE release `vX.Y.Z`, unchanged ZIP SHA-256, `stable/manifest.json`, and the Pages download card.

Both promotions reuse already-tested ZIP bytes; neither creates a new build.
