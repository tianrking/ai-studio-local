# ReachyMini 集成说明

## 概述

本项目已集成 ReachyMini 机器人回调系统，可以在游戏事件发生时触发后端请求，用于控制 ReachyMini 机器人的动作。

## 新增功能

### 1. 五种游戏事件回调

| 事件 | 触发时机 | 可用数据 |
|------|----------|----------|
| `slingshot_draw` | 拉弓蓄力时 | 拖拽距离、力度百分比、角度 |
| `slingshot_fire` | 发射小球时 | 发射力度、速度向量、颜色 |
| `ball_collision` | 小球碰撞时 | 碰撞位置、目标颜色 |
| `bubble_eliminated` | 气泡消除时 | 消除数量、颜色、得分 |
| `game_win` | 游戏胜利时 | 最终得分、射击次数、时长 |

### 2. 后端服务器

Express 服务器接收游戏事件并转发到机器人 API。

**位置**: `server/server.js`

**端点**:
- `GET /api/health` - 健康检查
- `GET /api/events` - 查看最近的事件
- `POST /api/events` - 接收游戏事件

## 安装与运行

### 1. 安装依赖

```bash
npm install
```

新增的依赖：
- `express` - Web 服务器框架
- `cors` - 跨域支持
- `npm-run-all` - 并行运行多个命令

### 2. 配置环境变量

复制 `.env.example` 到 `.env.local` 并配置：

```bash
cp .env.example .env.local
```

编辑 `.env.local`:
```
GEMINI_API_KEY=your_api_key_here
VITE_BACKEND_URL=http://localhost:3001
```

### 3. 运行方式

#### 方式一：分别启动（推荐用于开发）

```bash
# 终端 1 - 启动后端服务器
npm run server

# 终端 2 - 启动前端开发服务器
npm run dev
```

#### 方式二：同时启动

```bash
npm run dev:all
```

## 集成 ReachyMini 机器人

在 `server/server.js` 的事件处理函数中添加你的机器人控制代码：

```javascript
async function handleBubbleEliminated(data) {
  // 发送命令到 ReachyMini
  await reachyMini.celebrate({
    count: data.count,
    color: data.color
  });
}
```

## 事件数据结构

### SlingshotDrawEvent
```json
{
  "timestamp": "2024-01-28T10:00:00.000Z",
  "isDrawing": true,
  "dragDistance": 120,
  "maxDragDistance": 180,
  "powerRatio": 0.67,
  "ballPosition": { "x": 500, "y": 400 },
  "angle": 1.57
}
```

### SlingshotFireEvent
```json
{
  "timestamp": "2024-01-28T10:00:01.000Z",
  "powerRatio": 0.67,
  "velocityMultiplier": 0.25,
  "velocity": { "vx": 30, "vy": -50 },
  "ballPosition": { "x": 500, "y": 400 },
  "color": "red"
}
```

### BallCollisionEvent
```json
{
  "timestamp": "2024-01-28T10:00:02.000Z",
  "ballPosition": { "x": 600, "y": 300 },
  "collisionPosition": { "x": 620, "y": 280 },
  "hitBubbleId": "3-5-1234567890",
  "hitBubbleColor": "red"
}
```

### BubbleEliminationEvent
```json
{
  "timestamp": "2024-01-28T10:00:03.000Z",
  "count": 5,
  "color": "red",
  "colorLabel": "Red",
  "points": 500,
  "multiplier": 1.5,
  "totalPoints": 750,
  "bubbles": [...]
}
```

### GameWinEvent
```json
{
  "timestamp": "2024-01-28T10:05:00.000Z",
  "finalScore": 15000,
  "shotsFired": 25,
  "bubblesEliminated": 48,
  "duration": 300000
}
```

## 调试

查看最近收到的游戏事件：
```bash
curl http://localhost:3001/api/events
```

清除事件历史：
```bash
curl -X DELETE http://localhost:3001/api/events
```

## 文件结构

```
gemini-slingshot-reachymini/
├── components/
│   └── GeminiSlingshot.tsx    # 游戏逻辑 + 回调触发点
├── server/
│   └── server.js                # 后端服务器
├── types.ts                     # 类型定义
├── App.tsx                      # 回调实现 + 后端请求
└── package.json                 # 项目配置
```
