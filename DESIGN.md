# MangaTrack - Design System

## Color Strategy

**Strategy:** Committed

Primary color carries 30-60% of the surface through accents, buttons, and interactive elements.

### Palette (OKLCH)

**Primary:** oklch(45% .24 277.023) - Deep blue
**Secondary:** oklch(65% .241 354.308) - Vibrant pink
**Accent:** oklch(70% .18 45) - Warm yellow

**Neutrals (tinted toward primary):**
- Background: oklch(98% .005 277)
- Surface: oklch(100% .003 277)
- Border: oklch(90% .008 277)
- Text: oklch(15% .01 277)
- Muted text: oklch(45% .008 277)

### Usage Rules

- Primary: Main actions, navigation active states, progress indicators
- Secondary: Favorites, highlights, special callouts
- Accent: Stars, ratings, warnings
- Neutrals: Everything else

## Typography

**Font:** System sans-serif (Inter/San Francisco/Segoe UI)

**Scale:**
- Display: 2.5rem (40px) - Page titles
- H1: 2rem (32px) - Section headers
- H2: 1.5rem (24px) - Card titles
- H3: 1.25rem (20px) - Subsection headers
- Body: 1rem (16px) - Default text
- Small: 0.875rem (14px) - Labels, metadata
- Tiny: 0.75rem (12px) - Badges, footnotes

**Weights:**
- Bold: 700 - Headings, emphasis
- Semibold: 600 - Interactive elements
- Medium: 500 - Labels
- Regular: 400 - Body text

**Line heights:**
- Headings: 1.2
- Body: 1.5
- Small: 1.4

## Spacing

**Scale:** 4px base unit

- 2xs: 4px
- xs: 8px
- sm: 12px
- md: 16px
- lg: 24px
- xl: 32px
- 2xl: 48px
- 3xl: 64px

**Usage:**
- Component padding: md (16px)
- Section spacing: lg (24px)
- Page margins: xl (32px)
- Gap between elements: sm (12px)

## Elevation

**Levels:**
- Flat: No shadow (base surface)
- Low: 0 1px 2px rgba(0,0,0,0.05) (cards, inputs)
- Medium: 0 4px 6px rgba(0,0,0,0.07) (hover states)
- High: 0 10px 15px rgba(0,0,0,0.1) (modals, dropdowns)

## Border Radius

**Scale:**
- sm: 4px - Badges, small elements
- md: 8px - Buttons, inputs
- lg: 12px - Cards
- xl: 16px - Large containers
- full: 9999px - Pills, avatars

## Components

### Buttons

**Primary:** Primary background, white text, medium shadow
**Secondary:** Secondary background, white text, medium shadow
**Ghost:** Transparent background, primary text, no shadow
**Outline:** Transparent background, primary border, primary text

**States:**
- Hover: Darken background by 10%
- Active: Darken background by 20%
- Disabled: 30% opacity

### Cards

**Structure:**
- Background: Surface color
- Border: 1px solid border color
- Radius: lg (12px)
- Shadow: Low (default), Medium (hover)

**Content:**
- Cover image: 2:2.8 aspect ratio
- Title: H2 weight
- Metadata: Small size, muted color
- Badges: Tiny size, pill radius

### Forms

**Inputs:**
- Background: Surface color
- Border: 1px solid border color
- Radius: md (8px)
- Padding: sm (12px) horizontal
- Focus: Primary border, 2px

**Labels:**
- Size: Small
- Weight: Medium
- Color: Muted text

**Errors:**
- Color: oklch(55% .22 25) - Red
- Size: Tiny
- Weight: Medium

### Badges

**Status colors:**
- Reading: Primary blue
- Completed: oklch(60% .18 145) - Green
- Paused: oklch(70% .15 85) - Yellow
- Dropped: oklch(55% .22 25) - Red

**Structure:**
- Background: 10% opacity of status color
- Text: Full status color
- Radius: sm (4px)
- Padding: 2px 8px

## Motion

**Transitions:**
- Default: 200ms ease-out
- Hover: 150ms ease-out
- Focus: 100ms ease-out

**Animations:**
- Fade in: 300ms ease-out
- Slide up: 300ms ease-out
- Scale: 200ms ease-out

## Accessibility

**Contrast ratios:**
- Text on background: 4.5:1 minimum
- Large text: 3:1 minimum
- Interactive elements: 3:1 minimum

**Focus states:**
- 2px primary outline
- 4px offset from element

**Touch targets:**
- Minimum: 44x44px
- Recommended: 48x48px

## Responsive Breakpoints

**Mobile:** < 640px
**Tablet:** 640px - 1024px
**Desktop:** > 1024px

**Grid:**
- Mobile: 1 column
- Tablet: 2 columns
- Desktop: 3-4 columns
