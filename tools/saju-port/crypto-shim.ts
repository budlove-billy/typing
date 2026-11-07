// node:crypto 대체(브라우저용) — 사주 해시는 캐시 키로만 쓰이므로 FNV-1a 64비트 비슷한 값이면 충분하다.
export function createHash(_alg: string) {
  let s = '';
  return { update(x: string) { s += x; return this; }, digest(_enc?: string) {
    let h1 = 0x811c9dc5, h2 = 0x01000193;
    for (let i = 0; i < s.length; i++) { const c = s.charCodeAt(i); h1 = Math.imul(h1 ^ c, 16777619) >>> 0; h2 = Math.imul(h2 ^ c, 2246822519) >>> 0; }
    return (h1.toString(16).padStart(8, '0') + h2.toString(16).padStart(8, '0')).repeat(4);
  } };
}
