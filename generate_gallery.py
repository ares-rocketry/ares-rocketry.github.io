import os
from pathlib import Path

# Paths
base_dir = Path(
    "/Users/nicholascotugnomorrison/ares-rocketry/website/ares-rocketry.github.io"
)
gallery_dir = base_dir / "assets/ARES Photos"
html_file = base_dir / "gallery.html"

# Scan for images
extensions = {".jpg", ".jpeg", ".png"}
images = []
for root, _, files in os.walk(gallery_dir):
    for f in files:
        if Path(f).suffix.lower() in extensions:
            full_path = Path(root) / f
            rel_path = full_path.relative_to(base_dir)
            images.append(str(rel_path))

# Sorting images for consistent order, or randomness
images.sort()

# Generate Gallery HTML
gallery_html = """
                <h2 class="section__title">Gallery</h2>
                <div class="gallery-container">
"""
for img_path in images:
    # Use HTML friendly path
    img_src = img_path.replace("\\", "/")
    gallery_html += f"""
                    <div class="gallery-item" onclick="openLightbox('{img_src}')">
                        <img src="{img_src}" alt="ARES Gallery Image" loading="lazy">
                    </div>
"""
gallery_html += """
                </div>
"""

# Lightbox HTML
lightbox_html = """
    <!-- Lightbox Modal -->
    <div id="lightbox" class="lightbox">
        <button class="lightbox-close" onclick="closeLightbox()">&times;</button>
        <img id="lightbox-img" src="" alt="Enlarged Image">
    </div>

    <script>
        function openLightbox(src) {
            const lightbox = document.getElementById('lightbox');
            const img = document.getElementById('lightbox-img');
            img.src = src;
            lightbox.classList.add('active');
            document.body.style.overflow = 'hidden'; 
        }

        function closeLightbox() {
            const lightbox = document.getElementById('lightbox');
            lightbox.classList.remove('active');
            document.body.style.overflow = 'auto';
            document.getElementById('lightbox-img').src = ''; // Clear source
        }

        document.getElementById('lightbox').addEventListener('click', (e) => {
            if (e.target.id === 'lightbox') {
                closeLightbox();
            }
        });
        
        // Close on Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                closeLightbox();
            }
        });
    </script>
"""

# Read existing file
with open(html_file, "r") as f:
    content = f.read()

# Replace existing content block
# Target: <div class="container">...</div> inside main section
# I'll use simple string slicing if possible, or regex
import re

# Find the container inside the section with specific padding
# <section class="section" style="padding-top: 120px;">
#     <div class="container">
#       ... content to replace ...
#     </div>
# </section>

pattern = re.compile(
    r'(<section class="section"[^>]*>\s*<div class="container">)(.*?)(</div>\s*</section>)',
    re.DOTALL,
)


def replacement(match):
    return match.group(1) + gallery_html + match.group(3)


new_content = pattern.sub(replacement, content)

# Inject Lightbox before script or closing body
if "</body>" in new_content:
    new_content = new_content.replace("</body>", lightbox_html + "\n</body>")

with open(html_file, "w") as f:
    f.write(new_content)

print(f"Generated gallery with {len(images)} images.")
