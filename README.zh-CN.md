<div align="center">

# 🎮 AI Studio 本地化项目集合

**Google AI Studio 项目 — 本地开发版**

从 [Google AI Studio](https://aistudio.google.com) 收集的精彩项目合集，全部适配为本地开发环境。

每个项目都经过修改，可在标准本地开发环境中运行，并详细记录了所有改动。

[![DigitalOcean Referral Badge](https://web-platforms.sfo2.cdn.digitaloceanspaces.com/WWW/Badge%202.svg)](https://www.digitalocean/?refcode=9b9563b5b0b2&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge)

[English](./README.md) | 中文

---

## 项目列表

| 项目 | 描述 | 技术栈 |
|---------|-------------|------------|
| [Gemini 弹弓游戏](./gemini-slingshot/) | 基于物理的手势追踪游戏 + AI 策略 | React, MediaPipe, Gemini AI |
| [Gemini 弹弓游戏 (Reachy Mini版)](./gemini-slingshot-reachymini/) | 同上 + 机器人集成回调 | React, MediaPipe, Gemini AI |

---

## 快速开始

每个项目都是独立的，运行项目：

```bash
cd <项目名称>
npm install
cp .env.example .env.local
# 编辑 .env.local 填入你的 API 密钥
npm run dev
```

---

## 关于这个集合

### 为什么存在

从 Google AI Studio 导出的项目是为 AI Studio 托管环境设计的。下载后，由于以下原因通常需要修改才能在本地运行：

- **MediaPipe WASM 模块**需要特殊的 HTTP 头
- **包依赖**配置为 CDN 而非 npm
- **环境变量**需要本地配置

### 我们做了什么

集合中的每个项目都经过精心适配：

1. ✅ **修复 MediaPipe WASM 兼容性**以适配本地 Vite/Webpack 开发服务器
2. ✅ **迁移到 npm 包**替换 CDN 脚本（如适用）
3. ✅ **添加环境配置**模板（`.env.example`）
4. ✅ **记录所有修改**在项目 README 中
5. ✅ **保留原始署名**和许可证

### 常见修改

#### Vite 配置（COOP/COEP 头）

MediaPipe WASM 需要这些头才能使用 `SharedArrayBuffer`：

```typescript
// vite.config.ts
server: {
  headers: {
    'Cross-Origin-Embedder-Policy': 'require-corp',
    'Cross-Origin-Opener-Policy': 'same-origin',
  },
}
```

#### MediaPipe 本地 WASM 文件

WASM 文件被复制到 `public/mediapipe/` 以避免 CDN 问题：

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

## 贡献

有本地化的 AI Studio 项目？欢迎添加！

**要求：**
- 原项目必须允许修改/分发（请检查许可证）
- 包含对原作者和 AI Studio 的署名
- 记录所有更改
- 遵循项目结构约定

查看 [CONTRIBUTING.md](./CONTRIBUTING.md) 了解详细指南。

---

## 免责声明

所有项目基于 Google AI Studio 和各位原作者的作品。修改内容仅用于支持本地开发。

请尊重原始许可证和署名。

---

## 许可证

每个项目保持其原始许可证。详情请查看各项目目录。

---

## 致谢

- **[Google AI Studio](https://aistudio.google.com)** - 让这些项目成为可能的平台
- **[MediaPipe](https://google.github.io/mediapipe/)** - 提供了惊人的 ML 解决方案
- **[Google Gemini](https://ai.google.dev/)** - 提供了 AI 能力
- **所有原作者** - 构建了这些令人难以置信的项目

---

## DigitalOcean 赞助

秒级部署你的下一个应用。从 DigitalOcean 获取 $200 云额度：

<a href="https://www.digitalocean.com/?refcode=9b9563b5b0b2&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge"><img src="https://web-platforms.sfo2.cdn.digitaloceanspaces.com/WWW/Badge%202.svg" alt="DigitalOcean Referral Badge" /></a>

</div>
