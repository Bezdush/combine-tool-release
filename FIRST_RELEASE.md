# First release checklist

This repository starts without a BETA or STABLE channel pointer. Do not add empty manifests or sample ZIP files: the promotion workflows create the first signed pointers from the selected artifact.

## One-time state

- `main` contains the public site, `manifest.schema.json`, and the Pages workflow.
- There are no historical public releases or tags that collide with the first intended tags, for example `v0.3.110-beta.1` and `v0.3.110`.
- The GitHub Pages site is enabled and the **Release page** workflow can deploy from `main`.
- Release immutability is enabled for this repository.
- The publishing token used by the source repository can create tags and releases and push the signed channel pointers to this repository's `main` branch.

## First BETA

1. In the source repository, run **Build TEST** from `main` and wait for every test and `finalize-test` to pass.
2. Download and inspect the inner add-on ZIP from the TEST artifact.
3. Copy the resulting annotated TEST tag, for example `test-20261008T010000Z-r123456789-a1`.
4. Run **Promote BETA** from `main`, enter that TEST tag and a new version tag such as `v0.3.110-beta.1`, then approve the protected `beta` environment.
5. Verify the new immutable BETA release, its ZIP digest, `channel-manifest.json`, the `beta/manifest.json` pointer, and the Pages download card.

## First STABLE

1. Run **Promote STABLE** from the source repository's `main` and enter the exact BETA tag.
2. Approve the protected `stable` environment.
3. Verify the new immutable STABLE release `vX.Y.Z`, unchanged ZIP SHA-256, `stable/manifest.json`, and the Pages download card.

Both promotions reuse already-tested ZIP bytes; neither creates a new build.
