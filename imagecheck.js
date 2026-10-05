// Read-only image audit. It never changes, moves or deletes anything.
//
// Usage:  node check-images.js [site-root]
// Output: image-check-report.csv  (and a summary in the console)
//
// It answers two questions:
//   1. MISSING  - is any file pointing at an image that does not exist?
//                 (also flags wrong letter case, which works on Windows but breaks on a Linux server)
//   2. UNUSED   - is any image still sitting in a folder with .html files that nothing uses?
//
// Run it from the site root so paths starting with "/" or https://nemxnovels.site/ resolve correctly.

const fs = require("fs");
const path = require("path");

const args = process.argv.slice(2);
const ROOT = path.resolve(args.find(a => !a.startsWith("--")) || ".");
const TRASH_NAME = "_unused-images-removed";
const TRASH = path.join(ROOT, TRASH_NAME);
const SELF = path.basename(__filename);

const EXT = "png|jpe?g|gif|webp|svg|ico|avif|bmp";
const IMG_RE = new RegExp("\\.(" + EXT + ")$", "i");
const TEXT_RE = /\.(html?|css|js|json|xml|txt|md|php|webmanifest)$/i;

function* walkDirs(dir) {
    let entries;
    try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch (e) { return; }
    yield { dir, entries };
    for (const e of entries) {
        if (!e.isDirectory()) continue;
        if (e.name === "node_modules" || e.name === TRASH_NAME || e.name.startsWith(".")) continue;
        yield* walkDirs(path.join(dir, e.name));
    }
}

// Every image-looking reference in a text file, with its position
function refsIn(text) {
    const out = [];
    let m;
    const quoted = new RegExp("([\"'])([^\"'\\n]*?\\.(?:" + EXT + ")(?:[?#][^\"'\\n]*)?)\\1", "gi");
    while ((m = quoted.exec(text))) out.push({ ref: m[2], index: m.index });
    const urlRe = new RegExp("url\\(\\s*[\"']?([^\"')\\n]+?\\.(?:" + EXT + ")(?:[?#][^\"')\\n]*)?)[\"']?\\s*\\)", "gi");
    while ((m = urlRe.exec(text))) out.push({ ref: m[1], index: m.index });
    const srcset = /srcset\s*=\s*(["'])([\s\S]*?)\1/gi;
    while ((m = srcset.exec(text))) {
        for (const part of m[2].split(",")) {
            const u = part.trim().split(/\s+/)[0];
            if (u) out.push({ ref: u, index: m.index });
        }
    }
    return out;
}

// -> absolute path, or null for other websites / data: URIs
function resolveRef(ref, fromDir) {
    let p = ref.trim();
    const site = p.match(/^https?:\/\/(?:www\.)?nemxnovels\.site(\/[^?#]*)?/i);
    if (site) p = site[1] || "/";
    else if (/^[a-z][a-z0-9+.-]*:/i.test(p) || p.startsWith("//")) return null;
    p = p.split(/[?#]/)[0];
    try { p = decodeURIComponent(p); } catch (e) {}
    return p.startsWith("/") ? path.join(ROOT, p) : path.resolve(fromDir, p);
}

// Exact-case existence check, one path segment at a time
function checkExact(abs) {
    const rel = path.relative(ROOT, abs);
    if (rel === "" || rel.startsWith("..") || path.isAbsolute(rel)) return { kind: "outside" };
    let cur = ROOT, caseFix = false;
    const real = [];
    for (const seg of rel.split(path.sep)) {
        let names;
        try { names = fs.readdirSync(cur); } catch (e) { return { kind: "missing", rel }; }
        if (names.includes(seg)) { cur = path.join(cur, seg); real.push(seg); continue; }
        const ci = names.find(n => n.toLowerCase() === seg.toLowerCase());
        if (!ci) return { kind: "missing", rel };
        caseFix = true; cur = path.join(cur, ci); real.push(ci);
    }
    try { if (!fs.statSync(cur).isFile()) return { kind: "missing", rel }; } catch (e) { return { kind: "missing", rel }; }
    return caseFix ? { kind: "case", rel, real: real.join("/") } : { kind: "ok", rel };
}

function lineOf(text, index) {
    let n = 1;
    for (let i = 0; i < index; i++) if (text.charCodeAt(i) === 10) n++;
    return n;
}

function mentions(lowerText, name) {
    const variants = new Set([name.toLowerCase(), encodeURIComponent(name).toLowerCase()]);
    for (const v of variants) {
        const re = new RegExp("(^|[^a-z0-9_\\-.])" + v.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "(?![a-z0-9_\\-])", "i");
        if (re.test(lowerText)) return true;
    }
    return false;
}

// ---------- pass 1: read everything, check every reference ----------
const dirs = [...walkDirs(ROOT)];
const usedResolved = new Map();
const dirTexts = new Map();
const imageIndex = new Map(); // lowercase file name -> [relative paths]
const problems = new Map();   // key -> row
let textFiles = 0, refCount = 0, externalSkipped = 0, dynamicSkipped = 0;

for (const { dir, entries } of dirs) {
    for (const e of entries) {
        if (e.isFile() && IMG_RE.test(e.name)) {
            const k = e.name.toLowerCase();
            if (!imageIndex.has(k)) imageIndex.set(k, []);
            imageIndex.get(k).push(path.relative(ROOT, path.join(dir, e.name)));
        }
    }
}

for (const { dir, entries } of dirs) {
    const texts = [];
    for (const e of entries) {
        if (!e.isFile() || !TEXT_RE.test(e.name) || e.name === SELF) continue;
        const file = path.join(dir, e.name);
        const fileRel = path.relative(ROOT, file);
        let text;
        try { text = fs.readFileSync(file, "utf8"); } catch (err) { continue; }
        if (/\.js$/i.test(e.name) && /require\(\s*["']fs["']\s*\)/.test(text)) continue; // your own node tools
        textFiles++;
        texts.push({ name: e.name, lower: text.toLowerCase() });

        let ranges = null;
        const inComment = idx => {
            if (!ranges) {
                const re = /\.html?$/i.test(e.name) ? /<!--[\s\S]*?-->/g : /\/\*[\s\S]*?\*\//g;
                ranges = [...text.matchAll(re)].map(m => [m.index, m.index + m[0].length]);
            }
            return ranges.some(([a, b]) => idx >= a && idx < b);
        };

        for (const { ref, index } of refsIn(text)) {
            const bare = path.basename(ref.split(/[?#]/)[0]);
            if (/[${}<>+*]|\{\{/.test(ref) || new RegExp("^\\.(" + EXT + ")$", "i").test(bare)) { dynamicSkipped++; continue; }
            const abs = resolveRef(ref, dir);
            if (!abs) { externalSkipped++; continue; }
            refCount++;
            if (!usedResolved.has(abs.toLowerCase())) usedResolved.set(abs.toLowerCase(), fileRel);

            const res = checkExact(abs);
            if (res.kind === "ok") continue;

            const commented = inComment(index);
            let type, detail;
            if (res.kind === "outside") { type = "OUTSIDE SITE"; detail = "points outside the site folder"; }
            else if (res.kind === "case") { type = "CASE MISMATCH"; detail = `real file is "${res.real}"`; }
            else {
                type = commented ? "MISSING (in comment)" : "MISSING";
                const hints = [];
                const trashPath = path.join(TRASH, res.rel);
                if (fs.existsSync(trashPath)) hints.push(`it is in ${TRASH_NAME}/ - move it back`);
                const same = (imageIndex.get(path.basename(res.rel).toLowerCase()) || []).slice(0, 3);
                if (same.length) hints.push("same file name exists at: " + same.join(", "));
                detail = hints.join("; ");
            }
            const key = [type, fileRel, ref].join("|");
            if (problems.has(key)) problems.get(key).count++;
            else problems.set(key, { type, file: fileRel, line: lineOf(text, index), ref, count: 1, detail });
        }
    }
    dirTexts.set(dir, texts);
}

// ---------- pass 2: images left that nothing uses ----------
let foldersChecked = 0, imagesChecked = 0, imagesInNoHtmlFolders = 0;
for (const { dir, entries } of dirs) {
    const images = entries.filter(e => e.isFile() && IMG_RE.test(e.name));
    if (!entries.some(e => e.isFile() && /\.html?$/i.test(e.name))) { imagesInNoHtmlFolders += images.length; continue; }
    if (!images.length) continue;
    foldersChecked++;
    const texts = dirTexts.get(dir) || [];
    for (const img of images) {
        imagesChecked++;
        const abs = path.join(dir, img.name);
        let used = usedResolved.has(abs.toLowerCase());
        if (!used) used = texts.some(t => mentions(t.lower, img.name));
        if (!used) {
            const rel = path.relative(ROOT, abs);
            problems.set("UNUSED|" + rel, { type: "UNUSED", file: rel, line: "", ref: img.name, count: 1, detail: "no file in the site uses this image" });
        }
    }
}

// ---------- report ----------
const rows = [...problems.values()];
const order = ["MISSING", "CASE MISMATCH", "OUTSIDE SITE", "MISSING (in comment)", "UNUSED"];
rows.sort((a, b) => order.indexOf(a.type) - order.indexOf(b.type) || a.file.localeCompare(b.file));

const cols = ["type", "file", "line", "ref", "count", "detail"];
const esc = v => '"' + String(v).replace(/"/g, '""') + '"';
fs.writeFileSync("image-check-report.csv", [cols.join(",")].concat(rows.map(r => cols.map(c => esc(r[c])).join(","))).join("\n"));

const count = t => rows.filter(r => r.type === t).length;
console.log(`Text files scanned: ${textFiles}`);
console.log(`Image references checked: ${refCount}  (skipped: ${externalSkipped} external, ${dynamicSkipped} built-in-code)`);
console.log(`Folders with html checked for unused images: ${foldersChecked} (${imagesChecked} images; ${imagesInNoHtmlFolders} images in folders with no html were not checked)\n`);

for (const t of order) {
    const list = rows.filter(r => r.type === t);
    if (!list.length) continue;
    console.log(`${t}: ${list.length}`);
    list.slice(0, 40).forEach(r => console.log(`   ${r.file}${r.line ? ":" + r.line : ""}  ->  ${r.ref}${r.detail ? "   (" + r.detail + ")" : ""}`));
    if (list.length > 40) console.log(`   ... and ${list.length - 40} more (see the csv)`);
    console.log("");
}

const bad = count("MISSING") + count("CASE MISMATCH") + count("OUTSIDE SITE") + count("UNUSED");
console.log(bad === 0
    ? "ALL GOOD: no missing images and no unused images."
    : `Found ${bad} problem(s). Full list in image-check-report.csv`);
if (count("MISSING (in comment)")) console.log(`Note: ${count("MISSING (in comment)")} missing image(s) are only inside comments, so they don't break anything and aren't counted above.`);
process.exitCode = bad === 0 ? 0 : 1;