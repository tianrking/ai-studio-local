/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { GoogleGenAI } from '@google/genai';
import type { Bubble, BubbleColor, AiResponse, StrategicHint, DebugInfo } from '../types';

const GEMINI_API_KEY = import.meta.env.VITE_GEMINI_API_KEY || '';
const MODEL_NAME = 'gemini-2.5-flash-exp';

interface ClusterInfo {
  color: BubbleColor;
  count: number;
  bubbles: Array<{ row: number; col: number }>;
}

function getApiKey(): string {
  const key = import.meta.env.VITE_GEMINI_API_KEY || GEMINI_API_KEY;
  if (!key || key === 'YOUR_GEMINI_API_KEY_HERE') {
    throw new Error('GEMINI_API_KEY not configured. Please set VITE_GEMINI_API_KEY in your .env.local file.');
  }
  return key;
}

function analyzeBubbles(bubbles: Bubble[]): ClusterInfo[] {
  const clusters = new Map<BubbleColor, ClusterInfo>();

  for (const bubble of bubbles) {
    if (!bubble.active) continue;

    let cluster = clusters.get(bubble.color);
    if (!cluster) {
      cluster = { color: bubble.color, count: 0, bubbles: [] };
      clusters.set(bubble.color, cluster);
    }
    cluster.count++;
    cluster.bubbles.push({ row: bubble.row, col: bubble.col });
  }

  return Array.from(clusters.values()).sort((a, b) => b.count - a.count);
}

function buildPrompt(allBubbles: Bubble[], maxRow: number): string {
  const clusters = analyzeBubbles(allBubbles);
  const totalActive = allBubbles.filter(b => b.active).length;
  const maxClusterSize = clusters.length > 0 ? clusters[0].count : 0;
  const minClusterSize = clusters.length > 0 ? clusters[clusters.length - 1].count : 0;

  let prompt = `You are analyzing a bubble shooter puzzle game to provide strategic advice.

GAME STATE:
- Total active bubbles: ${totalActive}
- Maximum row with bubbles: ${maxRow}
- Rows are arranged in a hexagonal pattern (odd rows are offset)

BUBBLE CLUSTERS (grouped by color, size ${maxClusterSize} to ${minClusterSize}):
`;

  for (const cluster of clusters) {
    prompt += `- ${cluster.color}: ${cluster.count} bubbles at positions: ${cluster.bubbles.slice(0, 5).map(b => `(${b.row},${b.col})`).join(', ')}${cluster.bubbles.length > 5 ? '...' : ''}\n`;
  }

  prompt += `
ANALYSIS TASKS:
1. Identify the most promising target (largest cluster or one that will cause chain reactions)
2. Suggest the best color to use
3. Provide a brief strategic hint (max 15 words)

RESPONSE FORMAT (strict JSON):
{
  "hint": "Your strategic hint here (max 15 words)",
  "rationale": "Brief explanation of why this target is good (max 25 words)",
  "targetRow": <row number 0-${maxRow}>,
  "targetCol": <column number>,
  "recommendedColor": "<color from: red, blue, green, yellow, purple, orange>"
}

IMPORTANT: Choose targetRow and targetCol that match an EXISTING bubble from the clusters above.`;

  return prompt;
}

async function callGemini(prompt: string, imageData?: string): Promise<string> {
  const ai = new GoogleGenAI(getApiKey());
  const model = ai.getGenerativeModel({ model: MODEL_NAME });

  const contents: any[] = [{ role: 'user', parts: [{ text: prompt }] }];

  if (imageData) {
    contents[0].parts.unshift({
      inlineData: {
        mimeType: 'image/png',
        data: imageData
      }
    });
  }

  const result = await model.generateContent(contents);
  const response = result.response;
  return response.text();
}

function parseGeminiResponse(responseText: string): StrategicHint {
  // Try to extract JSON from the response
  const jsonMatch = responseText.match(/\{[\s\S]*\}/);
  if (jsonMatch) {
    try {
      return JSON.parse(jsonMatch[0]);
    } catch {
      // Fall through to default parsing
    }
  }

  // Fallback parsing
  const lines = responseText.split('\n');
  return {
    message: lines[0]?.trim() || 'Aim for the largest cluster to maximize eliminations.',
    rationale: 'AI analysis completed'
  };
}

export interface TargetCandidate {
  row: number;
  col: number;
  clusterSize: number;
  color: BubbleColor;
}

export async function getStrategicHint(
  screenshot?: string,
  allBubbles: Bubble[] = [],
  maxRow: number = 0
): Promise<AiResponse> {
  const startTime = performance.now();
  const timestamp = new Date().toISOString();

  const debugInfo: DebugInfo = {
    latency: 0,
    screenshotBase64: screenshot?.substring(0, 100) + '...',
    promptContext: `Bubbles: ${allBubbles.filter(b => b.active).length}, MaxRow: ${maxRow}`,
    rawResponse: '',
    timestamp
  };

  try {
    const prompt = buildPrompt(allBubbles, maxRow);
    const rawResponse = await callGemini(prompt, screenshot);

    debugInfo.rawResponse = rawResponse;
    debugInfo.parsedResponse = rawResponse.substring(0, 200) + '...';

    const hint = parseGeminiResponse(rawResponse);
    debugInfo.latency = Math.round(performance.now() - startTime);

    return { hint, debug: debugInfo };
  } catch (error) {
    debugInfo.error = error instanceof Error ? error.message : String(error);
    debugInfo.latency = Math.round(performance.now() - startTime);

    return {
      hint: {
        message: 'Aim for the largest cluster to maximize eliminations.',
        rationale: 'AI unavailable - using default strategy'
      },
      debug: debugInfo
    };
  }
}

export function getTargetCandidates(allBubbles: Bubble[]): TargetCandidate[] {
  const candidates: TargetCandidate[] = [];
  const processed = new Set<string>();

  for (const bubble of allBubbles) {
    if (!bubble.active) continue;
    const key = `${bubble.row},${bubble.col}`;
    if (processed.has(key)) continue;
    processed.add(key);

    const neighbors = allBubbles.filter(b =>
      b.active &&
      b.color === bubble.color &&
      (Math.abs(b.row - bubble.row) <= 1 && Math.abs(b.col - bubble.col) <= 1)
    );

    candidates.push({
      row: bubble.row,
      col: bubble.col,
      clusterSize: neighbors.length,
      color: bubble.color
    });
  }

  return candidates.sort((a, b) => b.clusterSize - a.clusterSize);
}
