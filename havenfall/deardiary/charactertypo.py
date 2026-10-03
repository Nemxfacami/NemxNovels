import os

# Folder containing your HTML files
folder = "."

old_link = 'deardiary-characters.html'
new_link = 'deardiary-character-melissa.html'

for filename in os.listdir(folder):
    if filename.endswith(".html"):
        filepath = os.path.join(folder, filename)

        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()

        if old_link in content:
            content = content.replace(old_link, new_link)

            with open(filepath, "w", encoding="utf-8") as file:
                file.write(content)

            print(f"Updated: {filename}")

print("Done.")