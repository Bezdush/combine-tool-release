'use strict';
const repo = 'Bezdush/combine-tool-release';
function node(tag, text) { const n = document.createElement(tag); if (text !== undefined) n.textContent = text; return n; }
function safe(url, version, name) {
  return /^combine_tool_\d+\.\d+\.\d+(-beta\.[1-9]\d*)?\.zip$/.test(name)
    && url === `https://github.com/${repo}/releases/download/v${version}/${name}`;
}
function link(url, text) {const n=node('a',text);n.href=url;return n;}
async function channel(name) {
  const panel=document.getElementById(name);
  try {
    const response=await fetch(`${name}/manifest.json`,{cache:'no-store'});
    if(response.status===404){panel.replaceChildren(node('h2',name==='stable'?'Stable':'Beta'),node('p',`No ${name} release is available yet.`));return;}
    if(!response.ok) throw Error();
    const m=await response.json();
    const version=/\/v(\d+\.\d+\.\d+(?:-beta\.[1-9]\d*)?)\//.exec(m.archive.url)?.[1];
    if(m.channel!==name || m.schema_version!==1 || !m.signature || !version
      || !safe(m.archive.url,version,m.archive.name) || (name==='beta')!==version.includes('-beta.')
      || version.split('-')[0]!==m.addon_version || !Array.isArray(m.blender_min) || !Array.isArray(m.blender_max)) throw Error();
    panel.replaceChildren(node('p',name.toUpperCase()),node('h2',`Combine Tool ${version}`));
    panel.append(node('p',`Blender ${m.blender_min.join('.')} – ${m.blender_max.join('.')} · Released ${new Date(m.published_at).toLocaleDateString('en-GB',{year:'numeric',month:'short',day:'numeric',timeZone:'UTC'})}`));
    if(name==='beta') panel.append(node('p','Preview version. Save a backup before trying experimental changes.'));
    const button=link(m.archive.url,name==='stable'?'Download':'Download Beta');button.className='download';
    const notes=node('p',m.release_notes);notes.className='notes';
    panel.append(button,node('h3','What’s new'),notes);
    const details=node('details');details.append(node('summary','Technical details'),node('p',`SHA-256: ${m.archive.sha256}`),node('p',`Build: ${m.build_id}`),node('p',`Commit: ${m.commit_sha}`));panel.append(details);
  }catch(_){panel.replaceChildren(node('h2',name==='stable'?'Stable':'Beta'),node('p','Release data is temporarily unavailable. Please try again later.'));}
}
async function history(){
  const panel=document.getElementById('history');
  try{
    const releases=[];
    for(let page=1;;page++){const response=await fetch(`https://api.github.com/repos/${repo}/releases?per_page=100&page=${page}`);if(!response.ok)throw Error();const batch=await response.json();releases.push(...batch);if(batch.length<100)break;}
    const list=node('ul');
    for(const r of releases){if(r.draft||r.prerelease||!/^v\d+\.\d+\.\d+$/.test(r.tag_name))continue;
      const version=r.tag_name.slice(1),asset=r.assets.find(a=>a.name===`combine_tool_${version}.zip`);
      if(!asset||!r.assets.some(a=>a.name==='channel-manifest.json')||!safe(asset.browser_download_url,version,asset.name))continue;
      const row=node('li');row.append(link(r.html_url,`Combine Tool ${version}`),document.createTextNode(' · '),link(asset.browser_download_url,'Download ZIP'));list.append(row);}
    panel.replaceChildren(list.children.length?list:node('p','No previous stable releases yet.'));
  }catch(_){panel.replaceChildren(node('p','The archive is temporarily unavailable.'),link(`https://github.com/${repo}/releases`,'Open release history on GitHub'));}
}
Promise.allSettled([channel('stable'),channel('beta'),history()]);
