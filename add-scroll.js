const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(process.argv[2] || ".");
const WRITE = process.argv.includes("--write");
const BACKUP = !process.argv.includes("--no-backup");

const START = "/* SCROLL-RESTORE START */";
const END = "/* SCROLL-RESTORE END */";

const NEW_CODE = `${START}
(function () {
    var key = "scroll-position-" + window.location.pathname;

    if ("scrollRestoration" in history) {
        history.scrollRestoration = "manual";
    }

    // Clicking Previous/Next means "fresh chapter": don't restore there
    document.addEventListener("click", function (e) {
        var link = e.target.closest ? e.target.closest(".nav-buttons a") : null;
        if (!link) return;
        if (e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) return;
        if (link.pathname === window.location.pathname) return; // href="#" placeholders
        try {
            sessionStorage.setItem("scroll-skip", link.pathname + "|" + Date.now());
        } catch (err) {}
    });

    // Save (throttled, plus once when leaving the page)
    var timer;
    function save() {
        try { localStorage.setItem(key, window.scrollY); } catch (err) {}
    }
    window.addEventListener("scroll", function () {
        clearTimeout(timer);
        timer = setTimeout(save, 150);
    });
    window.addEventListener("pagehide", save);

    // Restore
    function restore() {
        try {
            var skip = (sessionStorage.getItem("scroll-skip") || "").split("|");
            sessionStorage.removeItem("scroll-skip");
            if (skip[0] === window.location.pathname && Date.now() - Number(skip[1]) < 15000) {
                localStorage.removeItem(key);
                window.scrollTo(0, 0);
                return;
            }
        } catch (err) {}

        var saved = null;
        try { saved = localStorage.getItem(key); } catch (err) {}
        if (saved === null) return;

        var target = parseInt(saved, 10);
        var tries = 0;
        var t = setInterval(function () {
            window.scrollTo(0, target);
            tries++;
            if (Math.abs(window.scrollY - target) < 5 || tries > 20) {
                clearInterval(t);
            }
        }, 100);
    }

    if (document.readyState === "complete") restore();
    else window.addEventListener("load", restore);
})();
${END}`;

// ---------- helpers ----------

// Given the index of an opening "(", return the index just after the matching ")"
function matchParen(src, open) {
    let depth = 0;
    for (let i = open; i < src.length; i++) {
        const c = src[i];
        if (c === '"' || c === "'" || c === "`") {
            const q = c;
            i++;
            while (i < src.length && src[i] !== q) {
                if (src[i] === "\\") i++;
                i++;
            }
        } else if (c === "/" && src[i + 1] === "/") {
            while (i < src.length && src[i] !== "\n") i++;
        } else if (c === "/" && src[i + 1] === "*") {
            i = src.indexOf("*/", i + 2);
            if (i === -1) return -1;
            i++;
        } else if (c === "(") depth++;
        else if (c === ")") {
            depth--;
            if (depth === 0) return i + 1;
        }
    }
    return -1;
}

// Remove old scroll-position localStorage code from JS text
function stripOldScrollCode(js) {
    let out = js;
    const re = /\b(?:window|document)\.addEventListener\s*\(/g;
    let m;
    const cuts = [];
    while ((m = re.exec(out)) !== null) {
        const open = out.indexOf("(", m.index);
        let end = matchParen(out, open);
        if (end === -1) continue;
        const stmt = out.slice(m.index, end);
        if (/localStorage/.test(stmt) && /scroll/i.test(stmt)) {
            if (out[end] === ";") end++;
            cuts.push([m.index, end]);
        }
    }
    for (let i = cuts.length - 1; i >= 0; i--) {
        out = out.slice(0, cuts[i][0]) + out.slice(cuts[i][1]);
    }

    // old key variable, e.g. const scrollPositionKey = "scroll-position-" + window.location.pathname;
    out = out.replace(
        /^[ \t]*(?:const|let|var)\s+\w+\s*=\s*[^;\n]*scroll[^;\n]*(?:pathname|location)[^;\n]*;[ \t]*\r?\n?/gim, ""
    );
    // old comment lines about scroll position
    out = out.replace(/^[ \t]*\/\/[^\n]*scroll[^\n]*\r?\n?/gim, "");
    out = out.replace(/\n{3,}/g, "\n\n");
    return { js: out, removed: cuts.length };
}

function processHtml(html) {
    const scriptRe = /<script\b(?![^>]*\bsrc\s*=)[^>]*>([\s\S]*?)<\/script>/gi;
    const scripts = [...html.matchAll(scriptRe)];
    const notes = [];

    if (scripts.length) {
        const last = scripts[scripts.length - 1];
        let body = last[1];

        const marked = new RegExp(
            START.replace(/[*/]/g, "\\$&") + "[\\s\\S]*?" + END.replace(/[*/]/g, "\\$&")
        );

        if (marked.test(body)) {
            body = body.replace(marked, () => NEW_CODE);
            notes.push("updated existing new-style block");
        } else {
            const r = stripOldScrollCode(body);
            body = r.js.replace(/\s+$/, "") + "\n\n" + NEW_CODE + "\n";
            notes.push(r.removed ? `removed ${r.removed} old listener(s), added new` : "added new (no old code found)");
            if (/localStorage[^\n]*scroll|scroll[^\n]*localStorage|onscroll/i.test(r.js)) {
                notes.push("WARNING: leftover scroll/localStorage code, check by hand");
            }
        }

        const start = last.index + last[0].indexOf(">") + 1;
        const end = last.index + last[0].lastIndexOf("</script>");
        return { html: html.slice(0, start) + body + html.slice(end), notes };
    }

    // no inline script at all
    const block = `<script>\n${NEW_CODE}\n</script>\n`;
    notes.push("no inline script found, created one");
    if (/<\/body>/i.test(html)) {
        return { html: html.replace(/<\/body>/i, () => block + "</body>"), notes };
    }
    return { html: html + "\n" + block, notes };
}

function* walk(dir) {
    for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
        if (e.name === "node_modules" || e.name === ".git") continue;
        const p = path.join(dir, e.name);
        if (e.isDirectory()) yield* walk(p);
        else if (/\.html?$/i.test(e.name)) yield p;
    }
}

// ---------- run ----------
let found = 0, changed = 0;
for (const file of walk(ROOT)) {
    const html = fs.readFileSync(file, "utf8");
    const hasMenu = /<div\s+id\s*=\s*["']menu["']/i.test(html) && /option-box-style/.test(html);
    if (!hasMenu) continue;
    found++;

    const res = processHtml(html);
    console.log(`${path.relative(ROOT, file)}: ${res.notes.join("; ")}`);

    if (WRITE && res.html !== html) {
        if (BACKUP) fs.writeFileSync(file + ".bak", html);
        fs.writeFileSync(file, res.html);
        changed++;
    }
}
console.log(`\n${found} page(s) with the menu found.` +
    (WRITE ? ` ${changed} file(s) written.` : " Dry run only. Add --write to apply."));