
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

const ids = ["11005:4393", "11005:4449", "11005:4483", "11005:4512", "11005:4564", "11005:4607", "11005:4626", "11005:4633", "11005:4658", "11005:4687", "11005:4694", "11005:4701", "11005:4725", "11005:4750", "11005:4769", "11005:4787", "11005:4812", "11005:4838", "11005:4865", "11005:4881", "11005:4896", "11005:4912", "11005:4925", "11005:4941"];
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
const chunks = [];
let buf = [];
let len = 0;
for (const line of lines) {
  if (len + line.length + 1 > 12000 && buf.length) {
    chunks.push(buf.join('\n'));
    buf = [];
    len = 0;
  }
  buf.push(line);
  len += line.length + 1;
}
if (buf.length) chunks.push(buf.join('\n'));
return { count: items.length, requested: ids.length, tsvLen: tsv.length, tsvChunks: chunks };
