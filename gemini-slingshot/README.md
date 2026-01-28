<div align="center">
<img width="1200" height="475" alt="GHBanner" src="https://github.com/user-attachments/assets/0aa67016-6eaf-458a-adb2-6e31a0763ed6" />
</div>

# Gemini Slingshot - Local Development Edition

> **Original Project**: [Gemini Slingshot on Google AI Studio](https://aistudio.google.com/apps/bundled/gemini_slingshot?showPreview=true&showAssistant=true)

This is a local development version of the **Gemini Slingshot** project, originally created on Google AI Studio. The original project demonstrates an interactive physics-based game combining hand tracking (MediaPipe) with AI-powered strategy recommendations (Google Gemini).

---

## Original Author

**Original Creator**: [Google AI Studio Team](https://aistudio.google.com)

**Original Project**: https://aistudio.google.com/apps/bundled/gemini_slingshot?showPreview=true&showAssistant=true

---

## Local Modifications

This local version has been adapted to run in a standard Vite development environment with the following changes:

### Key Changes

1. **MediaPipe WASM Compatibility**: Fixed MediaPipe Hands WASM module loading for local Vite development
   - Installed MediaPipe packages via npm instead of CDN scripts
   - Configured Vite with COOP/COEP headers for SharedArrayBuffer support
   - Copied WASM files to public directory as static assets

2. **Package Management**: Migrated from AI Studio's bundle system to standard npm

3. **Environment Configuration**: Added local environment variable support for API keys

### Modification Details

See commit history for detailed changes made to enable local development.

---

## Run Locally

**Prerequisites:** Node.js

1. Install dependencies:
   ```bash
   npm install
   ```

2. Set up your environment:
   ```bash
   cp .env.example .env.local
   ```
   Then edit `.env.local` and set `GEMINI_API_KEY` to your Gemini API key.

   Get your API key: https://aistudio.google.com/app/apikey

3. Run the app:
   ```bash
   npm run dev
   ```

4. Open http://localhost:3000 in your browser

---

## DigitalOcean - Referral Link

Deploy your next app in seconds. Get $200 in cloud credits from DigitalOcean:

<a href="https://www.digitalocean.com/?refcode=9b9563b5b0b2&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge"><img src="https://web-platforms.sfo2.cdn.digitaloceanspaces.com/WWW/Badge%202.svg" alt="DigitalOcean Referral Badge" /></a>

---

## License

SPDX-License-Identifier: Apache-2.0

This project maintains the original Apache 2.0 license from the Google AI Studio original.

---

## Acknowledgments

- **Google AI Studio** - For the original project and platform
- **MediaPipe** - For hand tracking capabilities
- **Google Gemini** - For AI-powered strategy recommendations
- **Vite** - For the build tooling
