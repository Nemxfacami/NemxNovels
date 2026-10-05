// Read-only audit of Previous/Next buttons. It never edits your HTML files.
// Usage:  node scan-nav-buttons.js [site-folder]
// Output: nav-buttons-report.csv and nav-buttons-report.json (in the folder you run it from)

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(process.argv[2] || ".");

function* walk(dir) {
    for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
        if (e.name === "node_modules" || e.name === ".git") continue;
        const p = path.join(dir, e.name);
        if (e.isDirectory()) yield* walk(p);
        else if (/\.html?$/i.test(e.name)) yield p;
    }
}

function lineOf(text, index) {
    let n = 1;
    for (let i = 0; i < index; i++) if (text.charCodeAt(i) === 10) n++;
    return n;
}

function clean(s) {
    return s.replace(/<[^>]*>/g, " ").replace(/\s+/g, " ").trim();
}

function attr(attrs, name) {
    const m = attrs.match(new RegExp("\\b" + name + "\\s*=\\s*(?:\"([^\"]*)\"|'([^']*)')", "i"));
    return m ? (m[1] !== undefined ? m[1] : m[2]) : null;
}

function kindOf(label) {
    if (/prev|back|←|‹|«/i.test(label)) return "previous";
    if (/next|continue|→|›|»/i.test(label)) return "next";
    return "other";
}

// Where does this href point, and does that file exist (exact letter case)?
function checkTarget(href, fileDir) {
    if (href === null) return { exists: null, note: "NO HREF" };
    const h = href.trim();
    if (h === "") return { exists: null, note: "EMPTY HREF" };
    if (h.startsWith("#")) return { exists: null, note: "PLACEHOLDER #" };
    if (/^javascript:/i.test(h)) return { exists: null, note: "JAVASCRIPT HREF" };

    let p = h;
    const site = h.match(/^https?:\/\/(?:www\.)?nemxnovels\.site(\/[^?#]*)?/i);
    if (site) p = site[1] || "/";
    else if (/^[a-z][a-z0-9+.-]*:/i.test(h) || h.startsWith("//")) return { exists: null, note: "EXTERNAL" };

    p = p.split(/[?#]/)[0];
    try { p = decodeURIComponent(p); } catch (e) {}
    const abs = p.startsWith("/") ? path.join(ROOT, p) : path.resolve(fileDir, p);
    const rel = path.relative(ROOT, abs);

    let entries;
    try { entries = fs.readdirSync(path.dirname(abs)); } catch (e) { return { exists: false, resolved: rel, note: "TARGET MISSING" }; }
    const base = path.basename(abs);
    if (entries.includes(base)) return { exists: true, resolved: rel, note: "" };
    const ci = entries.find(n => n.toLowerCase() === base.toLowerCase());
    if (ci) return { exists: false, resolved: rel, note: `CASE MISMATCH (real file is "${ci}")` };
    return { exists: false, resolved: rel, note: "TARGET MISSING" };
}

const rows = [];
let storyPages = 0;

for (const file of walk(ROOT)) {
    const html = fs.readFileSync(file, "utf8");
    const rel = path.relative(ROOT, file);
    const fileDir = path.dirname(file);

    const hasMenu = /<div\s+id\s*=\s*["']menu["']/i.test(html) && /option-box-style/.test(html);
    const navRe = /<div\b[^>]*class\s*=\s*["'][^"']*\bnav-buttons\b[^"']*["'][^>]*>([\s\S]*?)<\/div>/gi;
    const blocks = [...html.matchAll(navRe)];
    if (!hasMenu && !blocks.length) continue; // not a story page
    storyPages++;

    const comments = [...html.matchAll(/<!--[\s\S]*?-->/g)].map(m => [m.index, m.index + m[0].length]);
    const inComment = i => comments.some(([a, b]) => i >= a && i < b);

    const found = [];
    const anchorRe = /<a\b([^>]*)>([\s\S]*?)<\/a>/gi;

    if (blocks.length) {
        for (const b of blocks) {
            const start = b.index + b[0].indexOf(">") + 1;
            for (const a of b[1].matchAll(anchorRe)) {
                found.push({ index: start + a.index, attrs: a[1], label: clean(a[2]), location: "nav-buttons" });
            }
            if (!/<a\b/i.test(b[1])) found.push({ index: b.index, attrs: "", label: "(empty block)", location: "nav-buttons", empty: true });
        }
    } else {
        // no nav-buttons block: look for stray Next/Previous links anywhere
        for (const a of html.matchAll(anchorRe)) {
            const label = clean(a[2]);
            if (/^(next|previous|prev|back)\b/i.test(label)) {
                found.push({ index: a.index, attrs: a[1], label, location: "outside nav-buttons" });
            }
        }
    }

    if (!found.length) {
        rows.push({ file: rel, line: "", location: "-", status: "-", kind: "-", label: "(none)", href: "", class: "", target_exists: "", target_resolved: "", flags: "NO NAV BUTTONS ON STORY PAGE" });
        continue;
    }

    for (const f of found) {
        const href = attr(f.attrs, "href");
        const t = f.empty ? { exists: null, note: "NO BUTTONS IN BLOCK" } : checkTarget(href, fileDir);
        const commented = inComment(f.index);
        const flags = [];
        if (commented) flags.push("COMMENTED OUT");
        if (t.note) flags.push(t.note);
        if (f.location !== "nav-buttons") flags.push("OUTSIDE NAV-BUTTONS");
        if (t.resolved && path.normalize(t.resolved) === path.normalize(rel)) flags.push("LINKS TO ITSELF");

        rows.push({
            file: rel,
            line: lineOf(html, f.index),
            location: f.location,
            status: commented ? "commented" : "live",
            kind: f.empty ? "-" : kindOf(f.label),
            label: f.label,
            href: href === null ? "" : href,
            class: attr(f.attrs, "class") || "",
            target_exists: t.exists === null ? "" : t.exists,
            target_resolved: t.resolved || "",
            flags: flags.join("; ")
        });
    }
}

// ---------- write reports ----------
const cols = ["file", "line", "location", "status", "kind", "label", "href", "class", "target_exists", "target_resolved", "flags"];
const esc = v => '"' + String(v).replace(/"/g, '""') + '"';
const csv = [cols.join(",")].concat(rows.map(r => cols.map(c => esc(r[c])).join(","))).join("\n");
fs.writeFileSync("nav-buttons-report.csv", csv);

// per-file view of live buttons
const byFile = {};
for (const r of rows) (byFile[r.file] = byFile[r.file] || []).push(r);
const noLive = Object.keys(byFile).filter(f => !byFile[f].some(r => r.status === "live"));

fs.writeFileSync("nav-buttons-report.json", JSON.stringify({ root: ROOT, storyPages, rows, filesWithNoLiveButtons: noLive }, null, 2));

// ---------- console summary ----------
const flagCounts = {};
for (const r of rows) for (const f of r.flags.split("; ").filter(Boolean)) {
    const k = f.replace(/\(real file is.*\)/, "").trim();
    flagCounts[k] = (flagCounts[k] || 0) + 1;
}
console.log(`Story pages scanned: ${storyPages}`);
console.log(`Button rows recorded: ${rows.length} (${rows.filter(r => r.status === "live").length} live, ${rows.filter(r => r.status === "commented").length} commented)`);
console.log(`Files with no live buttons at all: ${noLive.length}`);
console.log("Flags:");
Object.entries(flagCounts).sort((a, b) => b[1] - a[1]).forEach(([k, v]) => console.log(`  ${String(v).padStart(4)}  ${k}`));
console.log("\nWrote nav-buttons-report.csv and nav-buttons-report.json");