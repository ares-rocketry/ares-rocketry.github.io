# ARES Rocketry Website

This is the new static website for ARES Rocketry, designed to be modern, responsive, and lightweight. It matches the visual identity of the University of Melbourne ARES page but is built as a standalone static site for GitHub Pages.

## Project Structure

```
ares-rocketry.github.io/
├── index.html      # Main entry point (Single Page Application structure)
├── styles.css      # All styles (Variables, Reset, Components, Utilities)
├── script.js       # Minimal logic for mobile navigation and smooth scrolling
└── assets/         # Images and icons
    └── ares-logo.png
```

## Visual Style

- **Theme**: University Blue (Clean, Academic, Professional).
- **Colors**: 
    - Navy: `#000f46`
    - Cyan: `#46c8f0`
    - White: `#ffffff`
- **Typography**: 
    - Headings: `Fraunces` (Serif)
    - Body: `Source Sans Pro` (Sans-serif)

## Development

The site is purely static (HTML/CSS/JS). No build step is required.
To edit, simply modify the files and open `index.html` in your browser to inspect changes.

## Deployment to GitHub Pages

1.  **Push to GitHub**:
    Ensure this directory (`ares-rocketry.github.io`) is the root of your repository or the source folder.
    
    ```bash
    git add .
    git commit -m "Update website content"
    git push origin main
    ```

2.  **Configure GitHub Pages**:
    - Go to your repository **Settings** on GitHub.
    - Navigate to **Pages** (sidebar).
    - Under **Build and deployment**, select **Source** as `Deploy from a branch`.
    - Select your branch (e.g., `main`) and root folder (`/`).
    - Click **Save**.

The site will be live at `https://<organization>.github.io/ares-rocketry.github.io/` (or your custom domain).
