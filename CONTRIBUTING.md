# Contributing to Gemini Showcase

Thank you for your interest in contributing! This document outlines how to add new projects to this collection.

---

## Adding a New Project

### 1. Prerequisites Checklist

Before starting, ensure:

- [ ] The original AI Studio project allows modification and distribution
- [ ] You have successfully tested the project locally
- [ ] You have documented all modifications made

### 2. Project Structure

Create a new directory in `projects/` (or at root level):

```
gemini-showcase/
└── your-project-name/
    ├── README.md          # Project documentation + changes
    ├── .env.example       # Environment variable template
    ├── package.json
    ├── vite.config.ts     # With COOP/COEP headers if using MediaPipe
    └── ...                # Other project files
```

### 3. Required Documentation

Each project MUST include:

#### README.md Sections

1. **Original Project Attribution**
   ```markdown
   > **Original Project**: [Name](link)
   > **Original Creator**: [Author](link)
   ```

2. **Local Modifications**
   - List all changes made to enable local development
   - Explain why each change was necessary

3. **How to Run**
   - Step-by-step setup instructions
   - Required API keys and where to get them

4. **License**
   - Maintain original project's license

#### .env.example

Template for all required environment variables (never include real API keys):

```bash
API_KEY=YOUR_API_KEY_HERE
```

### 4. Common Modifications Reference

#### MediaPipe WASM Fix

If the project uses MediaPipe:

```bash
# Install packages
npm install @mediapipe/hands @mediapipe/camera_utils @mediapipe/drawing_utils

# Copy WASM files
mkdir -p public/mediapipe
cp node_modules/@mediapipe/hands/*.wasm public/mediapipe/
cp node_modules/@mediapipe/hands/*.data public/mediapipe/
```

**vite.config.ts:**
```typescript
server: {
  headers: {
    'Cross-Origin-Embedder-Policy': 'require-corp',
    'Cross-Origin-Opener-Policy': 'same-origin',
  },
},
assetsInclude: ['**/*.wasm'],
```

### 5. Submit Your Project

1. Fork this repository
2. Add your project following the structure above
3. Update the root README.md with your project
4. Submit a pull request

---

## Code Standards

- Keep original code style where possible
- Only modify what's necessary for local development
- Comment your changes clearly
- Test thoroughly before submitting

---

## Questions?

Open an issue or start a discussion!
