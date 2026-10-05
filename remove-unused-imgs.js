// Finds images that no page uses and removes them, one folder at a time.
//
// Usage:
//   node remove-unused-images.js [site-root]                       -> dry run, only reports
//   node remove-unused-images.js [site-root] --delete              -> moves unused images to _unused-images-removed/
//   node remove-unused-images.js [site-root] --delete --permanent  -> deletes them for good
//
// Rules:
//  - Only folders that directly contain at least one .html file are touched.
//  - Only images sitting directly in that folder are candidates (never subfolders, never other folders).
//  - An image counts as USED if:
//      a) any html/css/js/json file anywhere in the site points to it (relative, ../, /rooted, or
//         https://nemxnovels.site/... paths all resolve to the real file), or
//      b) its file name appears in any text file (html/css/js/...) in the same folder.
//    References inside HTML comments still count as "used" (the safe side).

const fs = require("fs");
const path = require("path");

const args = process.argv.slice(2);
const DELETE = args.includes("--delete");
const PERMANENT = args.includes("--permanent");
const ROOT = path.resolve(args.find(a => !a.startsWith("--")) || ".");
const TRASH_NAME = "_unused-images-removed";
const TRASH = path.join(ROOT, TRASH_NAME);
const SELF = path.basename(__filename);

if (PERMANENT && !DELETE) {
    console.error("--permanent only works together with --delete");
    process.exit(1);
}

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

// Pull every image-looking reference out of a text file
function refsIn(text) {
    const out = [];
    let m;
    const quoted = new RegExp("([\"'])([^\"'\\n]*?\\.(?:" + EXT + ")(?:[?#][^\"'\\n]*)?)\\1", "gi");
    while ((m = quoted.exec(text))) out.push(m[2]);
    const urlRe = new RegExp("url\\(\\s*[\"']?([^\"')\\n]+?\\.(?:" + EXT + ")(?:[?#][^\"')\\n]*)?)[\"']?\\s*\\)", "gi");
    while ((m = urlRe.exec(text))) out.push(m[1]);
    const srcset = /srcset\s*=\s*(["'])([\s\S]*?)\1/gi;
    while ((m = srcset.exec(text))) {
        for (const part of m[2].split(",")) {
            const u = part.trim().split(/\s+/)[0];
            if (u) out.push(u);
        }
    }
    return out;
}

function resolveRef(ref, fromDir) {
    let p = ref.trim();
    const site = p.match(/^https?:\/\/(?:www\.)?nemxnovels\.site(\/[^?#]*)?/i);
    if (site) p = site[1] || "/";
    else if (/^[a-z][a-z0-9+.-]*:/i.test(p) || p.startsWith("//")) return null; // other sites, data: URIs
    p = p.split(/[?#]/)[0];
    try { p = decodeURIComponent(p); } catch (e) {}
    const abs = p.startsWith("/") ? path.join(ROOT, p) : path.resolve(fromDir, p);
    return abs.toLowerCase();
}

function mentions(lowerText, name) {
    const variants = new Set([name.toLowerCase(), encodeURIComponent(name).toLowerCase()]);
    for (const v of variants) {
        const re = new RegExp("(^|[^a-z0-9_\\-.])" + v.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "(?![a-z0-9_\\-])", "i");
        if (re.test(lowerText)) return true;
    }
    return false;
}

// ---------- pass 1: read every text file, collect references ----------
const dirs = [...walkDirs(ROOT)];
const usedResolved = new Map();   // lowercase absolute path -> file that points to it
const dirTexts = new Map();       // dir -> [{ name, lower }]

for (const { dir, entries } of dirs) {
    const texts = [];
    for (const e of entries) {
        if (!e.isFile() || !TEXT_RE.test(e.name) || e.name === SELF) continue;
        const file = path.join(dir, e.name);
        let text;
        try { text = fs.readFileSync(file, "utf8"); } catch (err) { continue; }
        texts.push({ name: e.name, lower: text.toLowerCase() });
        for (const ref of refsIn(text)) {
            const r = resolveRef(ref, dir);
            if (r && !usedResolved.has(r)) usedResolved.set(r, path.relative(ROOT, file));
        }
    }
    dirTexts.set(dir, texts);
}

// ---------- pass 2: per folder, decide used / unused ----------
const rows = [];
let foldersChecked = 0, totalImages = 0, totalUnused = 0, totalBytes = 0;

console.log(DELETE ? (PERMANENT ? "MODE: permanent delete\n" : "MODE: move unused images to " + TRASH_NAME + "/\n") : "MODE: dry run (nothing will be changed)\n");

for (const { dir, entries } of dirs) {
    const hasHtml = entries.some(e => e.isFile() && /\.html?$/i.test(e.name));
    if (!hasHtml) continue;
    const images = entries.filter(e => e.isFile() && IMG_RE.test(e.name));
    if (!images.length) continue;

    foldersChecked++;
    const folderRel = path.relative(ROOT, dir) || ".";
    const texts = dirTexts.get(dir) || [];
    const unusedHere = [];

    for (const img of images) {
        totalImages++;
        const abs = path.join(dir, img.name);
        let usedBy = usedResolved.get(abs.toLowerCase());
        if (!usedBy) {
            for (const t of texts) {
                if (mentions(t.lower, img.name)) { usedBy = path.relative(ROOT, path.join(dir, t.name)); break; }
            }
        }

        const row = { folder: folderRel, image: img.name, size: 0, status: usedBy ? "used" : "unused", used_by: usedBy || "", action: "" };
        try { row.size = fs.statSync(abs).size; } catch (e) {}

        if (!usedBy) {
            totalUnused++;
            totalBytes += row.size;
            unusedHere.push(img.name);
            if (!DELETE) {
                row.action = "would remove (dry run)";
            } else {
                try {
                    if (PERMANENT) {
                        fs.unlinkSync(abs);
                        row.action = "deleted";
                    } else {
                        let dest = path.join(TRASH, path.relative(ROOT, abs));
                        fs.mkdirSync(path.dirname(dest), { recursive: true });
                        if (fs.existsSync(dest)) dest = dest + "." + Date.now();
                        fs.renameSync(abs, dest);
                        row.action = "moved to " + TRASH_NAME;
                    }
                } catch (e) {
                    row.action = "FAILED: " + e.message;
                }
            }
        }
        rows.push(row);
    }

    if (unusedHere.length) {
        console.log(`${folderRel}  (${unusedHere.length} unused of ${images.length} images)`);
        unusedHere.forEach(n => console.log("   - " + n));
    }
}

// ---------- report ----------
const cols = ["folder", "image", "size", "status", "used_by", "action"];
const esc = v => '"' + String(v).replace(/"/g, '""') + '"';
fs.writeFileSync("unused-images-report.csv", [cols.join(",")].concat(rows.map(r => cols.map(c => esc(r[c])).join(","))).join("\n"));

console.log(`\nFolders with html checked: ${foldersChecked}`);
console.log(`Images looked at: ${totalImages}`);
console.log(`Unused: ${totalUnused} (${(totalBytes / 1048576).toFixed(2)} MB)`);
console.log(DELETE ? "Done." : "Dry run only. Add --delete to act.");
console.log("Full list written to unused-images-report.csv");