#!/usr/bin/env python3
import os
import subprocess
import re

# Configuration
GALLERY_HTML_PATH = "gallery.html"
ASSETS_DIR = "assets/ARES Photos"
THUMBS_DIR = "assets/thumbnails"
THUMB_WIDTH = 600


def run_command(cmd):
    try:
        subprocess.run(
            cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError as e:
        print(f"Error executing {cmd}: {e}")


def sanitize_filename(filename):
    """Sanitize filename to avoid shell issues."""
    return filename.replace(" ", "%20")


def optimize_images():
    if not os.path.exists(THUMBS_DIR):
        os.makedirs(THUMBS_DIR)
        print(f"Created thumbnails directory: {THUMBS_DIR}")

    # Read original gallery.html content
    try:
        with open(GALLERY_HTML_PATH, "r") as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"Error: {GALLERY_HTML_PATH} not found.")
        return

    # Find all images in assets/ARES Photos
    image_replacements = {}

    # Walk through the assets directory
    for root, dirs, files in os.walk(ASSETS_DIR):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, start=".")

                # Create corresponding thumbnail path
                # Use flat structure or mirror? Flat structure easier for now but mirror might be safer for collisions.
                # Let's mirror structure within thumbnails dir to avoid collisions.
                rel_dir = os.path.relpath(root, start=ASSETS_DIR)
                if rel_dir == ".":
                    dest_dir = THUMBS_DIR
                else:
                    dest_dir = os.path.join(THUMBS_DIR, rel_dir)

                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)

                thumb_path = os.path.join(dest_dir, file)

                # Check if thumbnail exists
                if not os.path.exists(thumb_path):
                    print(f"Generating thumbnail for: {rel_path}...")
                    # Generate thumbnail using sips (macOS)
                    # Use --resampleWidth for width-based resize maintaining aspect ratio
                    cmd = [
                        "sips",
                        "-Z",
                        str(THUMB_WIDTH),
                        full_path,
                        "--out",
                        thumb_path,
                    ]
                    run_command(cmd)

                # Calculate relative path for HTML src
                thumb_rel_path = os.path.relpath(thumb_path, start=".")

                # Store replacement: original path -> thumbnail path
                # HTML paths might be URL encoded or just relative strings
                # The generate_gallery.py used str(rel_path) which uses OS separators.
                # Standardize to forward slashes for HTML
                html_orig = rel_path.replace(os.path.sep, "/")
                html_thumb = thumb_rel_path.replace(os.path.sep, "/")

                image_replacements[html_orig] = html_thumb

                # Also handle encoded spaces just in case
                html_orig_encoded = html_orig.replace(" ", "%20")
                html_thumb_encoded = html_thumb.replace(" ", "%20")
                image_replacements[html_orig_encoded] = html_thumb_encoded

    # Update gallery.html
    new_html = html_content

    # We need to be careful. We want to replace src="..." but NOT the onclick argument.
    # The onclick argument points to the full resolution image.
    # Pattern: <img src="ORIGINAL" ...> -> <img src="THUMBNAIL" ...>

    for orig, thumb in image_replacements.items():
        # Match src="orig"
        # We use simple string replacement but targeted
        # To avoid replacing the onclick part, we can rely on the fact that onclick is usually before or after src
        # But a global replace of `src="orig"` to `src="thumb"` is safe because onclick uses `onclick="openLightbox('orig')"`
        # (single quotes in my generation script basically, but let's check).

        # Check how it was generated:
        # <div class="gallery-item" onclick="openLightbox('assets/ARES Photos/...')">
        #     <img src="assets/ARES Photos/..." alt="..." loading="lazy">
        # </div>

        # So we ONLY want to replace the `src="..."` part.

        target = f'src="{orig}"'
        replacement = f'src="{thumb}"'
        if target in new_html:
            new_html = new_html.replace(target, replacement)
            # print(f"Replaced {target} with {replacement}")

        # Try encoded version if not found
        target_enc = f'src="{orig.replace(" ", "%20")}"'
        replacement_enc = f'src="{thumb.replace(" ", "%20")}"'
        if target_enc in new_html and target_enc != target:  # avoid double replace
            new_html = new_html.replace(target_enc, replacement_enc)

    # Write updated HTML
    with open(GALLERY_HTML_PATH, "w") as f:
        f.write(new_html)

    print(f"Successfully updated {GALLERY_HTML_PATH}")


if __name__ == "__main__":
    optimize_images()
