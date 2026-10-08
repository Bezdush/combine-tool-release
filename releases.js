'use strict';

function element(tag, text) {
  const item = document.createElement(tag);
  item.textContent = text;
  return item;
}

function link(url, text, className) {
  const item = element('a', text);
  item.href = url;
  if (className) item.className = className;
  return item;
}

function showRelease(channel, release) {
  const panel = document.getElementById(channel);
  const title = channel === 'stable' ? 'Stable' : 'Beta';
  if (!release) {
    panel.replaceChildren(element('h3', title),
      element('p', 'No release has been published for this channel yet.'));
    panel.setAttribute('aria-busy', 'false');
    return;
  }
  const version = element('p', `Version ${release.version}`);
  version.className = 'version';
  const compatibility = element('p', `Blender ${release.blender_min.join('.')}–${release.blender_max.join('.')}`);
  compatibility.className = 'availability';
  panel.replaceChildren(element('h3', title), version, compatibility);
  if (channel === 'beta') {
    const preview = element('p', 'Preview release');
    preview.className = 'preview';
    panel.append(preview);
  }
  panel.append(link(release.archive_url, channel === 'stable' ? 'Download Stable ZIP' : 'Download Beta ZIP', 'download'));
  const details = element('p', '');
  details.append(link(release.release_url, 'Read release notes'));
  panel.append(details);
  panel.setAttribute('aria-busy', 'false');
}

fetch('releases.json')
  .then(response => {
    if (!response.ok) throw new Error('Release data unavailable');
    return response.json();
  })
  .then(releases => {
    showRelease('stable', releases.stable);
    showRelease('beta', releases.beta);
  })
  .catch(() => {
    for (const channel of ['stable', 'beta']) {
      const panel = document.getElementById(channel);
      panel.replaceChildren(element('h3', channel === 'stable' ? 'Stable' : 'Beta'),
        element('p', 'Release information is temporarily unavailable. Please use the release history link below.'));
      panel.setAttribute('aria-busy', 'false');
    }
  });
