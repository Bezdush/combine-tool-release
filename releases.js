'use strict';

const repo = 'Bezdush/combine-tool-release';

function node(tag, text) {
  const element = document.createElement(tag);
  if (text !== undefined) element.textContent = text;
  return element;
}

function safeArchive(url, version, name) {
  return /^combine_tool_\d+\.\d+\.\d+(-beta\.[1-9]\d*)?\.zip$/.test(name)
    && url === `https://github.com/${repo}/releases/download/v${version}/${name}`;
}

function makeLink(url, text) {
  const element = node('a', text);
  element.href = url;
  element.className = 'download';
  return element;
}

function showUnavailable(panel, channel) {
  panel.replaceChildren(
    node('h3', channel === 'stable' ? 'Stable' : 'Beta'),
    node('p', `No ${channel} release is available yet.`)
  );
  panel.setAttribute('aria-busy', 'false');
}

async function loadChannel(channel) {
  const panel = document.getElementById(channel);
  try {
    const response = await fetch(`${channel}/manifest.json`, { cache: 'no-store' });
    if (response.status === 404) {
      showUnavailable(panel, channel);
      return;
    }
    if (!response.ok) throw new Error('Release manifest unavailable');

    const manifest = await response.json();
    const version = /\/v(\d+\.\d+\.\d+(?:-beta\.[1-9]\d*)?)\//.exec(manifest.archive.url)?.[1];
    const blenderRangeIsValid = Array.isArray(manifest.blender_min)
      && Array.isArray(manifest.blender_max)
      && manifest.blender_min.every(Number.isInteger)
      && manifest.blender_max.every(Number.isInteger);

    if (manifest.channel !== channel || manifest.schema_version !== 1 || !manifest.signature || !version
      || !safeArchive(manifest.archive.url, version, manifest.archive.name)
      || (channel === 'beta') !== version.includes('-beta.')
      || version.split('-')[0] !== manifest.addon_version || !blenderRangeIsValid) {
      throw new Error('Invalid release manifest');
    }

    const versionText = node('p', `Version ${version}`);
    versionText.className = 'version';
    panel.replaceChildren(node('h3', channel === 'stable' ? 'Stable' : 'Beta'), versionText);
    const compatibility = node('p', `Blender ${manifest.blender_min.join('.')}–${manifest.blender_max.join('.')}`);
    compatibility.className = 'availability';
    panel.append(compatibility);

    if (channel === 'beta') {
      const betaNotice = node('p', 'Preview version.');
      betaNotice.className = 'availability';
      panel.append(betaNotice);
    }

    panel.append(makeLink(manifest.archive.url, channel === 'stable' ? 'Download' : 'Download beta'));

    const notesHeading = node('h4', 'Release notes');
    const notes = node('p', manifest.release_notes || 'No release notes provided.');
    notes.className = 'notes';
    panel.append(notesHeading, notes);
    panel.setAttribute('aria-busy', 'false');
  } catch (_) {
    panel.replaceChildren(
      node('h3', channel === 'stable' ? 'Stable' : 'Beta'),
      node('p', 'Release information is temporarily unavailable. Please try again later.')
    );
    panel.setAttribute('aria-busy', 'false');
  }
}

Promise.allSettled([loadChannel('stable'), loadChannel('beta')]);
