/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

export interface Point {
  x: number;
  y: number;
}

export interface Vector {
  vx: number;
  vy: number;
}

export type BubbleColor = 'red' | 'blue' | 'green' | 'yellow' | 'purple' | 'orange';

export interface Bubble {
  id: string;
  row: number;
  col: number;
  x: number;
  y: number;
  color: BubbleColor;
  active: boolean; // if false, popped
  isFloating?: boolean; // For animation
}

export interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  life: number;
  color: string;
}

export interface StrategicHint {
  message: string;
  rationale?: string;
  targetRow?: number;
  targetCol?: number;
  recommendedColor?: BubbleColor;
}

export interface DebugInfo {
  latency: number;
  screenshotBase64?: string;
  promptContext: string;
  rawResponse: string;
  parsedResponse?: any;
  error?: string;
  timestamp: string;
}

export interface AiResponse {
  hint: StrategicHint;
  debug: DebugInfo;
}

// MediaPipe Type Definitions (Augmenting window)
declare global {
  interface Window {
    Hands: any;
    Camera: any;
    drawConnectors: any;
    drawLandmarks: any;
    HAND_CONNECTIONS: any;
  }
}

// === ReachyMini Integration Types ===

/**
 * Event data when bubbles are eliminated
 * Used for triggering robot reactions
 */
export interface BubbleEliminationEvent {
  timestamp: string;
  count: number;
  color: BubbleColor;
  colorLabel: string;
  points: number;
  multiplier: number;
  totalPoints: number;
  bubbles: Array<{
    id: string;
    row: number;
    col: number;
    x: number;
    y: number;
  }>;
}

/**
 * Event data when slingshot is being drawn
 * Triggered during the pinch and drag phase
 */
export interface SlingshotDrawEvent {
  timestamp: string;
  isDrawing: boolean;
  dragDistance: number;
  maxDragDistance: number;
  powerRatio: number; // 0.0 to 1.0
  ballPosition: Point;
  angle: number; // radians
}

/**
 * Event data when slingshot is fired
 * Triggered when the ball is released
 */
export interface SlingshotFireEvent {
  timestamp: string;
  powerRatio: number; // 0.0 to 1.0
  velocityMultiplier: number;
  velocity: Vector;
  ballPosition: Point;
  color: BubbleColor;
}

/**
 * Event data when ball collides with a bubble
 * Triggered on initial collision before elimination check
 */
export interface BallCollisionEvent {
  timestamp: string;
  ballPosition: Point;
  collisionPosition: Point;
  hitBubbleId: string;
  hitBubbleColor: BubbleColor;
}

/**
 * Event data when game is won
 * Triggered when all bubbles are eliminated
 */
export interface GameWinEvent {
  timestamp: string;
  finalScore: number;
  shotsFired: number;
  bubblesEliminated: number;
  duration: number; // milliseconds
}

/**
 * Callback type for bubble elimination events
 * Can be connected to ReachyMini robot actions
 */
export type BubbleEliminationCallback = (event: BubbleEliminationEvent) => void | Promise<void>;

/**
 * Callback type for slingshot draw events
 */
export type SlingshotDrawCallback = (event: SlingshotDrawEvent) => void | Promise<void>;

/**
 * Callback type for slingshot fire events
 */
export type SlingshotFireCallback = (event: SlingshotFireEvent) => void | Promise<void>;

/**
 * Callback type for ball collision events
 */
export type BallCollisionCallback = (event: BallCollisionEvent) => void | Promise<void>;

/**
 * Callback type for game win events
 */
export type GameWinCallback = (event: GameWinEvent) => void | Promise<void>;

/**
 * Configuration for ReachyMini integration
 */
export interface ReachyMiniConfig {
  /** Callback function triggered when bubbles are eliminated */
  onBubbleEliminated?: BubbleEliminationCallback;
  /** Callback function triggered during slingshot draw (pull back) */
  onSlingshotDraw?: SlingshotDrawCallback;
  /** Callback function triggered when slingshot is fired */
  onSlingshotFire?: SlingshotFireCallback;
  /** Callback function triggered when ball collides with a bubble */
  onBallCollision?: BallCollisionCallback;
  /** Callback function triggered when game is won */
  onGameWin?: GameWinCallback;
  /** Backend API endpoint URL for sending callbacks */
  backendUrl?: string;
  /** Enable debug logging for callbacks */
  debug?: boolean;
  /** Minimum number of bubbles to trigger elimination callback */
  minBubbleCount?: number;
}