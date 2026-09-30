/**
 * Design System Snapshot exporter v0.1 — READ ONLY.
 * Scans the current Figma file and exports figma-snapshot.raw.json.
 * Does not create, edit, rename, publish, or mutate any document nodes.
 */

const EXPORTER_VERSION = "0.1.0";
const EXPORTER_SCHEMA_VERSION = "1.0-raw";
const ICONS_PAGE_NAME = "Icons";

/** @type {{ category: string, expected: number|null, extracted: number, ok: boolean, error?: string }[]} */
let lastInventory = [];

figma.showUI(__html__, { width: 360, height: 560, themeColors: true });

figma.ui.onmessage = async (msg) => {
  if (!msg || typeof msg !== "object") return;
  if (msg.type === "ready") {
    postFileMeta();
    return;
  }
  if (msg.type === "export-snapshot") {
    try {
      await runExport();
    } catch (err) {
      const message = err && err.message ? err.message : String(err);
      figma.ui.postMessage({ type: "export-error", message });
    }
    return;
  }
  if (msg.type === "close") {
    figma.closePlugin();
  }
};

function postFileMeta() {
  figma.ui.postMessage({
    type: "file-meta",
    fileName: figma.root.name || "Untitled",
    fileKey: typeof figma.fileKey === "string" ? figma.fileKey : null,
    exporterVersion: EXPORTER_VERSION,
  });
}

function progress(phase, detail, pct) {
  figma.ui.postMessage({
    type: "progress",
    phase: phase || "",
    detail: detail || "",
    pct: typeof pct === "number" ? pct : null,
  });
}

function serializeValue(value) {
  if (value === null || value === undefined) return null;
  if (typeof value !== "object") return value;
  if (value.type === "VARIABLE_ALIAS" && value.id) {
    return { alias: true, id: value.id };
  }
  // Color / RGB(A)
  if (typeof value.r === "number" && typeof value.g === "number" && typeof value.b === "number") {
    const out = { r: value.r, g: value.g, b: value.b };
    if (typeof value.a === "number") out.a = value.a;
    return out;
  }
  // FLOAT boxed shapes from some plugins — keep primitives as-is when possible
  try {
    return JSON.parse(JSON.stringify(value));
  } catch (_) {
    return String(value);
  }
}

function serializeValuesByMode(valuesByMode) {
  const out = {};
  if (!valuesByMode || typeof valuesByMode !== "object") return out;
  for (const modeId of Object.keys(valuesByMode)) {
    out[modeId] = serializeValue(valuesByMode[modeId]);
  }
  return out;
}

function packPropertyDefinitions(defs) {
  const out = {};
  if (!defs || typeof defs !== "object") return out;
  for (const key of Object.keys(defs)) {
    const d = defs[key] || {};
    const packed = { type: d.type };
    if (d.defaultValue !== undefined) packed.defaultValue = serializeValue(d.defaultValue);
    if (Array.isArray(d.variantOptions)) packed.variantOptions = d.variantOptions.slice();
    out[key] = packed;
  }
  return out;
}

function packComponentProperties(props) {
  const out = {};
  if (!props || typeof props !== "object") return out;
  for (const key of Object.keys(props)) {
    const p = props[key];
    if (p && typeof p === "object" && "value" in p) {
      out[key] = { type: p.type, value: serializeValue(p.value) };
    } else {
      out[key] = p;
    }
  }
  return out;
}

async function ensurePagesLoaded() {
  // dynamic-page: load each page before findAll
  const pages = figma.root.children.filter((n) => n.type === "PAGE");
  for (let i = 0; i < pages.length; i++) {
    const page = pages[i];
    progress("pages", `Loading page ${i + 1}/${pages.length}: ${page.name}`, 5 + Math.floor((i / Math.max(pages.length, 1)) * 10));
    if ("loadAsync" in page && typeof page.loadAsync === "function") {
      await page.loadAsync();
    }
  }
  return pages;
}

async function exportVariables() {
  progress("variables", "Reading variable collections…", 18);
  const collectionsIn = await figma.variables.getLocalVariableCollectionsAsync();
  progress("variables", "Reading variables…", 22);
  const variablesIn = await figma.variables.getLocalVariablesAsync();

  const collections = collectionsIn.map((c) => ({
    id: c.id,
    name: c.name,
    description: c.description || "",
    defaultModeId: c.defaultModeId || null,
    modes: (c.modes || []).map((m) => ({ id: m.modeId, name: m.name })),
    variableIds: (c.variableIds || []).slice(),
  }));

  const variables = variablesIn.map((v) => ({
    id: v.id,
    key: v.key || null,
    name: v.name,
    description: v.description || "",
    variableCollectionId: v.variableCollectionId,
    resolvedType: v.resolvedType,
    valuesByMode: serializeValuesByMode(v.valuesByMode),
    scopes: Array.isArray(v.scopes) ? v.scopes.slice() : [],
    codeSyntax: v.codeSyntax && typeof v.codeSyntax === "object" ? { ...v.codeSyntax } : {},
  }));

  return { collections, variables };
}

function serializeTextStyle(s) {
  return {
    id: s.id,
    key: s.key || null,
    name: s.name,
    description: s.description || "",
    styleType: "TEXT",
    documentationLinks: (s.documentationLinks || []).map((l) => ({ url: l.url })),
    details: {
      fontSize: s.fontSize,
      fontName: s.fontName ? { family: s.fontName.family, style: s.fontName.style } : null,
      lineHeight: s.lineHeight,
      letterSpacing: s.letterSpacing,
      textCase: s.textCase,
      textDecoration: s.textDecoration,
      paragraphSpacing: s.paragraphSpacing,
      paragraphIndent: s.paragraphIndent,
    },
  };
}

function serializeEffectStyle(s) {
  let effects = [];
  try {
    effects = JSON.parse(JSON.stringify(s.effects || []));
  } catch (_) {
    effects = [];
  }
  return {
    id: s.id,
    key: s.key || null,
    name: s.name,
    description: s.description || "",
    styleType: "EFFECT",
    documentationLinks: (s.documentationLinks || []).map((l) => ({ url: l.url })),
    details: { effects },
  };
}

function serializePaintStyle(s) {
  let paints = [];
  try {
    paints = JSON.parse(JSON.stringify(s.paints || []));
  } catch (_) {
    paints = [];
  }
  return {
    id: s.id,
    key: s.key || null,
    name: s.name,
    description: s.description || "",
    styleType: "PAINT",
    documentationLinks: (s.documentationLinks || []).map((l) => ({ url: l.url })),
    details: { paints },
  };
}

function serializeGridStyle(s) {
  let layoutGrids = [];
  try {
    layoutGrids = JSON.parse(JSON.stringify(s.layoutGrids || []));
  } catch (_) {
    layoutGrids = [];
  }
  return {
    id: s.id,
    key: s.key || null,
    name: s.name,
    description: s.description || "",
    styleType: "GRID",
    documentationLinks: (s.documentationLinks || []).map((l) => ({ url: l.url })),
    details: { layoutGrids },
  };
}

async function exportStyles() {
  progress("styles", "Reading text styles…", 30);
  const text = (await figma.getLocalTextStylesAsync()).map(serializeTextStyle);
  progress("styles", "Reading effect styles…", 34);
  const effect = (await figma.getLocalEffectStylesAsync()).map(serializeEffectStyle);
  progress("styles", "Reading paint styles…", 36);
  const paint = (await figma.getLocalPaintStylesAsync()).map(serializePaintStyle);
  progress("styles", "Reading grid styles…", 38);
  const grid = (await figma.getLocalGridStylesAsync()).map(serializeGridStyle);
  return { text, effect, paint, grid };
}

function packVariantComponent(c) {
  // Component variants expose axes via variantProperties (not instance componentProperties).
  const variantProperties = c.variantProperties || null;
  const componentProperties = {};
  if (variantProperties && typeof variantProperties === "object") {
    for (const k of Object.keys(variantProperties)) {
      componentProperties[k] = variantProperties[k];
    }
  }
  return {
    id: c.id,
    key: c.key || null,
    name: c.name,
    description: c.description || "",
    componentProperties,
    variantProperties,
    documentationLinks: (c.documentationLinks || []).map((l) => ({ url: l.url })),
  };
}

function packStandaloneComponent(c, page) {
  return {
    id: c.id,
    key: c.key || null,
    name: c.name,
    description: c.description || "",
    page: page ? page.name : null,
    pageId: page ? page.id : null,
    componentSetId: null,
    componentPropertyDefinitions: packPropertyDefinitions(c.componentPropertyDefinitions),
    documentationLinks: (c.documentationLinks || []).map((l) => ({ url: l.url })),
    remote: !!c.remote,
  };
}

function packComponentSet(set, page) {
  const variants = [];
  const childVariantIds = [];
  for (const child of set.children || []) {
    if (child.type !== "COMPONENT") continue;
    childVariantIds.push(child.id);
    variants.push(packVariantComponent(child));
  }

  // Correct API: defaultVariant is a ComponentNode (not defaultVariantId)
  let defaultVariantId = null;
  try {
    if (set.defaultVariant && set.defaultVariant.id) {
      defaultVariantId = set.defaultVariant.id;
    }
  } catch (_) {
    defaultVariantId = null;
  }

  return {
    id: set.id,
    key: set.key || null,
    name: set.name,
    description: set.description || "",
    page: page ? page.name : null,
    pageId: page ? page.id : null,
    componentPropertyDefinitions: packPropertyDefinitions(set.componentPropertyDefinitions),
    childVariantIds,
    defaultVariantId,
    variants,
    documentationLinks: (set.documentationLinks || []).map((l) => ({ url: l.url })),
    remote: !!set.remote,
  };
}

async function exportComponentsAndIcons(pages) {
  const componentSets = [];
  const components = []; // standalone only (not children of a set)
  const icons = [];
  let iconsPage = null;

  const total = pages.length;
  for (let i = 0; i < total; i++) {
    const page = pages[i];
    progress("components", `Scanning ${page.name} (${i + 1}/${total})…`, 40 + Math.floor((i / Math.max(total, 1)) * 45));

    const isIconsPage = page.name === ICONS_PAGE_NAME;
    if (isIconsPage) {
      iconsPage = { id: page.id, name: page.name };
    }

    const nodes = page.findAll((n) => n.type === "COMPONENT" || n.type === "COMPONENT_SET");
    for (const node of nodes) {
      if (node.type === "COMPONENT_SET") {
        const packed = packComponentSet(node, page);
        componentSets.push(packed);
        if (isIconsPage) {
          icons.push({
            id: node.id,
            name: node.name,
            type: "COMPONENT_SET",
            page: page.name,
            description: node.description || "",
          });
        }
      } else if (node.type === "COMPONENT") {
        const parentIsSet = node.parent && node.parent.type === "COMPONENT_SET";
        if (isIconsPage) {
          icons.push({
            id: node.id,
            name: node.name,
            type: "COMPONENT",
            page: page.name,
            description: node.description || "",
          });
        }
        if (!parentIsSet) {
          components.push(packStandaloneComponent(node, page));
        }
      }
    }
  }

  return {
    componentSets,
    components,
    icons: {
      page: iconsPage || { id: null, name: ICONS_PAGE_NAME },
      icons,
    },
  };
}

function buildInventory(counts, errors) {
  const rows = [
    { category: "variables", expected: null, extracted: counts.variables, ok: !errors.variables, error: errors.variables || null },
    { category: "variableCollections", expected: null, extracted: counts.collections, ok: !errors.variables, error: null },
    { category: "textStyles", expected: null, extracted: counts.textStyles, ok: !errors.styles, error: errors.styles || null },
    { category: "effectStyles", expected: null, extracted: counts.effectStyles, ok: !errors.styles, error: null },
    { category: "paintStyles", expected: null, extracted: counts.paintStyles, ok: !errors.styles, error: null },
    { category: "gridStyles", expected: null, extracted: counts.gridStyles, ok: !errors.styles, error: null },
    { category: "componentSets", expected: null, extracted: counts.componentSets, ok: !errors.components, error: errors.components || null },
    { category: "components", expected: null, extracted: counts.components, ok: !errors.components, error: null },
    { category: "icons", expected: null, extracted: counts.icons, ok: !errors.components, error: null },
  ];
  return rows;
}

function assertComplete(payload) {
  const failures = [];
  if (!payload.file || !payload.file.name) failures.push({ category: "file", message: "missing file name" });
  if (!Array.isArray(payload.collections)) failures.push({ category: "collections", message: "missing collections array" });
  if (!Array.isArray(payload.variables)) failures.push({ category: "variables", message: "missing variables array" });
  if (!payload.styles || !Array.isArray(payload.styles.text) || !Array.isArray(payload.styles.effect)) {
    failures.push({ category: "styles", message: "missing styles.text/effect arrays" });
  }
  if (!Array.isArray(payload.componentSets)) failures.push({ category: "componentSets", message: "missing componentSets array" });
  if (!Array.isArray(payload.components)) failures.push({ category: "components", message: "missing components array" });
  if (!payload.icons || !Array.isArray(payload.icons.icons)) {
    failures.push({ category: "icons", message: "missing icons.icons array" });
  }
  // Structural integrity: every component set must have id + name
  for (const s of payload.componentSets || []) {
    if (!s.id || !s.name) {
      failures.push({ category: "componentSets", message: "set missing id/name" });
      break;
    }
    if (!Array.isArray(s.variants)) {
      failures.push({ category: "componentSets", message: `set ${s.id} missing variants array` });
      break;
    }
  }
  return failures;
}

async function runExport() {
  progress("start", "Starting read-only scan…", 2);
  const errors = {};
  const startedAt = new Date().toISOString();

  const pages = await ensurePagesLoaded();

  let collections = [];
  let variables = [];
  try {
    const v = await exportVariables();
    collections = v.collections;
    variables = v.variables;
  } catch (e) {
    errors.variables = e && e.message ? e.message : String(e);
  }

  let styles = { text: [], effect: [], paint: [], grid: [] };
  try {
    styles = await exportStyles();
  } catch (e) {
    errors.styles = e && e.message ? e.message : String(e);
  }

  let componentSets = [];
  let components = [];
  let icons = { page: { id: null, name: ICONS_PAGE_NAME }, icons: [] };
  try {
    const c = await exportComponentsAndIcons(pages);
    componentSets = c.componentSets;
    components = c.components;
    icons = c.icons;
  } catch (e) {
    errors.components = e && e.message ? e.message : String(e);
  }

  progress("assemble", "Assembling raw snapshot…", 92);

  const fileKey = typeof figma.fileKey === "string" && figma.fileKey ? figma.fileKey : null;

  const counts = {
    collections: collections.length,
    variables: variables.length,
    textStyles: styles.text.length,
    effectStyles: styles.effect.length,
    paintStyles: styles.paint.length,
    gridStyles: styles.grid.length,
    componentSets: componentSets.length,
    components: components.length,
    icons: icons.icons.length,
    pages: pages.length,
  };

  const payload = {
    exporter: {
      name: "design-system-lab-snapshot",
      version: EXPORTER_VERSION,
      schemaVersion: EXPORTER_SCHEMA_VERSION,
      readOnly: true,
      exportedAt: startedAt,
    },
    file: {
      key: fileKey,
      name: figma.root.name || "Untitled",
    },
    sourceCapabilities: {
      variables: errors.variables ? "partial" : "complete",
      components: errors.components ? "partial" : "complete",
      styles: errors.styles ? "partial" : "complete",
      icons: errors.components ? "partial" : "complete",
      previews: "deferred",
      structuralAudit: "deferred",
    },
    extractionNotes: {
      transport: "figma-plugin",
      iconsScope: "Icons page only",
      defaultVariantApi: "ComponentSetNode.defaultVariant.id",
    },
    counts,
    collections,
    variables,
    styles,
    componentSets,
    components,
    icons,
  };

  const failures = assertComplete(payload);
  if (errors.variables) failures.push({ category: "variables", message: errors.variables });
  if (errors.styles) failures.push({ category: "styles", message: errors.styles });
  if (errors.components) failures.push({ category: "components", message: errors.components });

  const inventory = buildInventory(counts, errors);
  lastInventory = inventory;

  const complete = failures.length === 0 && !fileKeyMissingBlocking(fileKey);

  // fileKey may be null without private API — warn but allow download with placeholder
  // Ingestion requires a key; plugin marks incomplete if missing.
  let effectiveComplete = complete;
  if (!fileKey) {
    failures.push({
      category: "file",
      message: "fileKey unavailable (enablePrivatePluginApi / private plugin required). Snapshot marked incomplete.",
    });
    effectiveComplete = false;
  }

  progress("done", effectiveComplete ? "Snapshot ready" : "Snapshot incomplete", 100);

  figma.ui.postMessage({
    type: "export-result",
    complete: effectiveComplete,
    inventory,
    counts,
    failures,
    fileName: payload.file.name,
    fileKey: payload.file.key,
    // Only send downloadable JSON when complete — incomplete must not be treated as valid
    json: effectiveComplete ? JSON.stringify(payload) : null,
    suggestedName: "figma-snapshot.raw.json",
  });
}

function fileKeyMissingBlocking(fileKey) {
  return !fileKey;
}
