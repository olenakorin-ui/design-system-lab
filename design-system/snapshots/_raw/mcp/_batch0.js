const NS = 'ds.snapshot.v1';
const jobs = [{"key": "idx_0", "partIndex": 0, "totalParts": 4, "expectedLen": 18596, "size": 6000}, {"key": "idx_0", "partIndex": 1, "totalParts": 4, "expectedLen": 18596, "size": 6000}, {"key": "idx_0", "partIndex": 2, "totalParts": 4, "expectedLen": 18596, "size": 6000}];
return jobs.map((j) => {
  const b64 = figma.root.getSharedPluginData(NS, 'b64_' + j.key) ?? '';
  const start = j.partIndex * j.size;
  return {
    key: j.key,
    expectedLen: b64.length,
    partIndex: j.partIndex,
    totalParts: j.totalParts,
    slice: b64.slice(start, start + j.size),
  };
});
