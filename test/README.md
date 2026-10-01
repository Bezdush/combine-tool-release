# Public TEST feed

`test/manifest.json` is the public TEST channel pointer consumed by the updater. TEST packages are published only after main checks and Blender 4.4.3 validation pass. The exact candidate ZIP tested by CI is published; the workflow does not rebuild it.

The file uses the same signed `combine-tool-channel-manifest-v1` contract as BETA and STABLE. TEST has no private feed.
