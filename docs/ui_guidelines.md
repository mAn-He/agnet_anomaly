# UI guidelines — FieldOps Copilot

Premium **blue-and-white** industrial product aesthetic (avoid copying external dark-theme references literally).

## Tokens

Defined in [`frontend/src/app/globals.css`](../frontend/src/app/globals.css) and mirrored in Tailwind ([`frontend/tailwind.config.ts`](../frontend/tailwind.config.ts)):

| Token | Value | Usage |
|-------|-------|--------|
| Background | `#F7FBFF` | Page canvas |
| Surface | `#FFFFFF` | Cards |
| Text | `#0B1220` | Primary copy |
| Border | `#DCE8FF` | Hairlines |
| Primary | `#2563EB` | CTAs, emphasis |
| Cyan | `#38BDF8` | Accents, highlights |
| Violet | `#8B5CF6` | Optional accent |

## Components

- **Hero**: oversized bold sans-serif, strong hierarchy, soft radial gradients (`hero-glow`).
- **Cards**: `rounded-2xl`, light border, `shadow-card`.
- **Buttons**: pill shape (`rounded-pill`), primary solid and ghost outline.
- **Badges**: modality chips (`image`, `pdf`, `text`, `sensor`).
- **Layout**: max width `6xl`, generous padding, high contrast.

## Screens

See Next.js routes under `frontend/src/app/`: landing, analysis, upload, pipeline, evidence, report, review, export, eval.
