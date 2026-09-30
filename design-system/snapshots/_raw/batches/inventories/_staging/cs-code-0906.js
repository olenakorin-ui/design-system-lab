
async function pack(id) {
  const n = await figma.getNodeByIdAsync(id);
  if (!n || n.type !== 'COMPONENT_SET') return null;
  const page = n.parent && n.parent.type === 'PAGE' ? n.parent.name : null;
  const variants = [];
  for (const c of n.children) {
    if (c.type !== 'COMPONENT') continue;
    variants.push({ id: c.id, key: c.key || null, name: c.name, description: '', componentProperties: {} });
  }
  const defs = {};
  for (const [k, v] of Object.entries(n.componentPropertyDefinitions || {})) {
    const d = { type: v.type };
    if (v.defaultValue !== undefined) d.defaultValue = v.defaultValue;
    if (v.variantOptions) d.variantOptions = v.variantOptions;
    defs[k] = d;
  }
  return { id: n.id, key: n.key || null, name: n.name, description: n.description || '', page, componentPropertyDefinitions: defs, defaultVariantId: n.defaultVariant ? n.defaultVariant.id : null, variants };
}

const ids = ["11005:4393", "11005:4449", "11005:4483", "11005:4512", "11005:4564", "11005:4607", "11005:4626", "11005:4633"];
const items = [];
for (const id of ids) { const x = await pack(id); if (x) items.push(x); }
function esc(s){return String(s||'').replace(/\t/g,' ').replace(/\n/g,' ');}
const lines = items.map(s => {
  const prop = JSON.stringify(s.componentPropertyDefinitions);
  const vars = s.variants.map(v => v.id+'|'+esc(v.key)+'|'+esc(v.name)).join(';');
  return [s.id, esc(s.key), esc(s.name), esc(s.page), esc(s.defaultVariantId), prop, vars].join('\t');
});
const tsv = lines.join('\n');
if (tsv.length <= 15000) return { count: items.length, requested: ids.length, tsv };
const CH = 12000;
const chunks = [];
for (let i = 0; i < tsv.length; i += CH) chunks.push(tsv.slice(i, i + CH));
return { count: items.length, requested: ids.length, tsvLen: tsv.length, tsvChunks: chunks };
