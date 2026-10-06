const fs = require("fs");
const path = require("path");

const folder = process.cwd();          // current folder only, no subfolders
const NEW_HREF = "behindthecurse-character-lucas.html";
const MARKER = "Characters are not available yet";

const files = fs.readdirSync(folder).filter(
  (f) => f.toLowerCase().endsWith(".html") && fs.statSync(path.join(folder, f)).isFile()
);

let totalFiles = 0;
let totalLinks = 0;

for (const file of files) {
  const filePath = path.join(folder, file);
  const original = fs.readFileSync(filePath, "utf8");
  let count = 0;

  // Look at every opening <a ...> tag
  const updated = original.replace(/<a\b[^>]*>/gi, (tag) => {
    // Only touch the tag that has the "Characters not available" onclick
    if (!tag.includes(MARKER)) return tag;

    count++;

    return tag
      // remove the onclick attribute (double or single quoted)
      .replace(/\s*onclick\s*=\s*"[^"]*"/i, "")
      .replace(/\s*onclick\s*=\s*'[^']*'/i, "")
      // replace href value (handles `href ="#"` spacing too)
      .replace(/href\s*=\s*(["'])[^"']*\1/i, `href ="${NEW_HREF}"`);
  });

  if (count > 0) {
    fs.writeFileSync(filePath, updated, "utf8");
    totalFiles++;
    totalLinks += count;
    console.log(`Updated ${file} (${count} link${count > 1 ? "s" : ""})`);
  }
}

console.log(`\nDone. ${totalLinks} link(s) changed in ${totalFiles} file(s) out of ${files.length} HTML file(s) scanned.`);