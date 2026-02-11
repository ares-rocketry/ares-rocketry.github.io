#!/usr/bin/env python3
import os
import subprocess
import re

# Configuration
GALLERY_HTML_PATHS = ["gallery.html", "projects.html", "about.html", "subteams.html"]
ASSETS_DIR = "assets/ARES Photos"
THUMBS_DIR = "assets/thumbnails"
THUMB_WIDTH = 800


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

    # Generate thumbnails for all images
    image_replacements = {}

    # Walk through the assets directory
    for root, dirs, files in os.walk(ASSETS_DIR):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, start=".")

                # Create corresponding thumbnail path
                rel_dir = os.path.relpath(root, start=ASSETS_DIR)
                if rel_dir == ".":
                    dest_dir = THUMBS_DIR
                else:
                    dest_dir = os.path.join(THUMBS_DIR, rel_dir)

                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)

                thumb_path = os.path.join(dest_dir, file)

                # Check if thumbnail exists or regenerate
                # We'll regenerate if file size is 0 or if explicitly requested (by deleting folder beforehand)
                # But here we assume we want to update width to 800.
                # Simplest check: check if width matches 800? Hard with just python.
                # Let's just always overwrite or rely on user clearing cache.
                # For this run, let's overwrite to ensure 800px update.
                print(f"Processing thumbnail for: {rel_path}...")
                cmd = ["sips", "-Z", str(THUMB_WIDTH), full_path, "--out", thumb_path]
                run_command(cmd)

                # Calculate relative path for HTML src
                thumb_rel_path = os.path.relpath(thumb_path, start=".")

                html_orig = rel_path.replace(os.path.sep, "/")
                html_thumb = thumb_rel_path.replace(os.path.sep, "/")

                image_replacements[html_orig] = html_thumb

                # Also handle encoded spaces just in case
                html_orig_encoded = html_orig.replace(" ", "%20")
                html_thumb_encoded = html_thumb.replace(" ", "%20")
                image_replacements[html_orig_encoded] = html_thumb_encoded

    # Update HTML files
    for html_path in GALLERY_HTML_PATHS:
        try:
            with open(html_path, "r") as f:
                html_content = f.read()
        except FileNotFoundError:
            print(f"Error: {html_path} not found.")
            continue

        new_html = html_content

        for orig, thumb in image_replacements.items():
            # Match src="orig"
            # We want to replace src but NOT create broken links if user clicks on thumbnails?
            # Wait, `projects.html` and `about.html` might rely on `src` for full-res display if no lightbox.
            # `projects.html` has no lightbox script?
            # Oh, `projects.html` has logic?
            # actually `projects.html` has `class="project-gallery"`.
            # If I replace `src` with thumb, the image is smaller.
            # If user clicks it? `projects.html` has no lightbox script.
            # The images just sit there. `transform: scale(1.05)` on hover.
            # So replacing `src` with thumbnail is SAFE because there is no "click to expand".
            # Perfect.

            # For hero images? Same.

            target = f'src="{orig}"'
            replacement = f'src="{thumb}"'
            if target in new_html:
                new_html = new_html.replace(target, replacement)

            # Try encoded version if not found
            target_enc = f'src="{orig.replace(" ", "%20")}"'
            replacement_enc = f'src="{thumb.replace(" ", "%20")}"'
            if target_enc in new_html and target_enc != target:
                new_html = new_html.replace(target_enc, replacement_enc)

        # Write updated HTML
        with open(html_path, "w") as f:
            f.write(new_html)

        print(f"Successfully updated {html_path}")


if __name__ == "__main__":
    optimize_images()
