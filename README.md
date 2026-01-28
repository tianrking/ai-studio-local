<div align="center">

# 🎮 Gemini Showcase

**AI Studio Projects — Local Development Edition**

A collection of amazing projects from [Google AI Studio](https://aistudio.google.com), adapted for local development.

Each project has been modified to run in a standard local development environment, with detailed documentation of all changes.

[![DigitalOcean Referral Badge](https://web-platforms.sfo2.cdn.digitaloceanspaces.com/WWW/Badge%202.svg)](https://www.digitalocean.com/?refcode=9b9563b5b0b2&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge)

---

## Projects

| Project | Description | Tech Stack |
|---------|-------------|------------|
| [Gemini Slingshot](./gemini-slingshot/) | Physics-based game with hand tracking & AI strategy | React, MediaPipe, Gemini AI |

---

## Quick Start

Each project is self-contained. To run a project:

```bash
cd <project-name>
npm install
cp .env.example .env.local
# Edit .env.local with your API keys
npm run dev
```

---

## About This Collection

### Why This Exists

Projects exported from Google AI Studio are designed to run in AI Studio's hosted environment. When downloaded, they often require modifications to run locally due to:

- **MediaPipe WASM modules** requiring special HTTP headers
- **Package dependencies** configured for CDN rather than npm
- **Environment variables** needing local configuration

### What We Do

Each project in this collection has been carefully adapted:

1. ✅ **Fixed MediaPipe WASM compatibility** for local Vite/Webpack dev servers
2. ✅ **Migrated to npm packages** from CDN scripts where applicable
3. ✅ **Added environment configuration** templates (`.env.example`)
4. ✅ **Documented all modifications** in project READMEs
5. ✅ **Preserved original attribution** and licenses

### Common Modifications

#### Vite Configuration (COOP/COEP Headers)

MediaPipe WASM requires these headers for `SharedArrayBuffer`:

```typescript
// vite.config.ts
server: {
  headers: {
    'Cross-Origin-Embedder-Policy': 'require-corp',
    'Cross-Origin-Opener-Policy': 'same-origin',
  },
}
```

#### MediaPipe Local WASM Files

WASM files are copied to `public/mediapipe/` to avoid CDN issues:

```typescript
hands = new Hands({
  locateFile: (file) => {
    if (file.endsWith('.wasm') || file.endsWith('.data')) {
      return `/mediapipe/${file}`;
    }
    return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
  },
});
```

---

## Contributing

Have an AI Studio project you've localized? We'd love to add it!

**Requirements:**
- Original project must allow modification/distribution (check license)
- Include attribution to original creator and AI Studio
- Document all changes made
- Follow the project structure conventions

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

---

## Disclaimer

All projects are based on work from Google AI Studio and respective original creators. Modifications are provided to enable local development.

Please respect the original licenses and attributions.

---

## License

Each project maintains its original license. See individual project directories for details.

---

## Acknowledgments

- **[Google AI Studio](https://aistudio.google.com)** - The platform that makes these projects possible
- **[MediaPipe](https://google.github.io/mediapipe/)** - For amazing ML solutions
- **[Google Gemini](https://ai.google.dev/)** - For the AI capabilities
- **All original creators** - For building these incredible projects

---

## DigitalOcean Sponsor

Deploy your next app in seconds. Get $200 in cloud credits from DigitalOcean:

<a href="https://www.digitalocean.com/?refcode=9b9563b5b0b2&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge"><img src="https://web-platforms.sfo2.cdn.digitaloceanspaces.com/WWW/Badge%202.svg" alt="DigitalOcean Referral Badge" /></a>

</div>
