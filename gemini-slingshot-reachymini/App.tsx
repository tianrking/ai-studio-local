/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
*/

import React, { useEffect } from 'react';
import GeminiSlingshot from './components/GeminiSlingshot';
import { BubbleEliminationEvent, ReachyMiniConfig, SlingshotDrawEvent, SlingshotFireEvent, BallCollisionEvent, GameWinEvent } from './types';

// Backend API URL - configure this to point to your ReachyMini backend server
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:3001';

// Helper function to send events to backend
const sendToBackend = async (eventType: string, data: any) => {
  try {
    const response = await fetch(`${BACKEND_URL}/api/events`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        eventType,
        timestamp: new Date().toISOString(),
        data
      })
    });

    if (!response.ok) {
      console.warn(`⚠️ Backend returned ${response.status}`);
    }
  } catch (error) {
    console.warn(`⚠️ Failed to send ${eventType} to backend:`, error);
  }
};

const App: React.FC = () => {
  useEffect(() => {
    // Test backend connection on mount
    fetch(`${BACKEND_URL}/api/health`)
      .then(res => res.json())
      .then(data => console.log('✅ Backend connected:', data))
      .catch(err => console.log('⚠️ Backend not available:', err.message));
  }, []);

  // Callback: Slingshot draw (pull back) - triggered during aiming
  const handleSlingshotDraw = async (event: SlingshotDrawEvent) => {
    console.log('🎯 [Draw] Power:', Math.round(event.powerRatio * 100) + '%', 'Distance:', event.dragDistance);
    await sendToBackend('slingshot_draw', event);
  };

  // Callback: Slingshot fire - triggered when ball is released
  const handleSlingshotFire = async (event: SlingshotFireEvent) => {
    console.log('🚀 [Fire] Power:', Math.round(event.powerRatio * 100) + '%', 'Color:', event.color);
    await sendToBackend('slingshot_fire', event);
  };

  // Callback: Ball collision - triggered when ball hits a bubble
  const handleBallCollision = async (event: BallCollisionEvent) => {
    console.log('💥 [Collision] Hit', event.hitBubbleColor, 'bubble at', event.collisionPosition);
    await sendToBackend('ball_collision', event);
  };

  // Callback: Bubble elimination - triggered when bubbles are matched and popped
  const handleBubbleEliminated = async (event: BubbleEliminationEvent) => {
    console.log('🎉 [Eliminated]', event.count, event.colorLabel, 'bubbles,', event.totalPoints, 'pts');
    await sendToBackend('bubble_eliminated', event);
  };

  // Callback: Game win - triggered when all bubbles are cleared
  const handleGameWin = async (event: GameWinEvent) => {
    console.log('🏆 [WIN] Score:', event.finalScore, 'Shots:', event.shotsFired, 'Time:', Math.round(event.duration / 1000) + 's');
    await sendToBackend('game_win', event);
  };

  // Configure the ReachyMini callback system
  const reachyMiniConfig: ReachyMiniConfig = {
    onSlingshotDraw: handleSlingshotDraw,
    onSlingshotFire: handleSlingshotFire,
    onBallCollision: handleBallCollision,
    onBubbleEliminated: handleBubbleEliminated,
    onGameWin: handleGameWin,
    backendUrl: BACKEND_URL,
    debug: true,           // Enable debug logging for callbacks
    minBubbleCount: 3      // Only trigger elimination callback for 3+ bubbles
  };

  return (
    <div className="w-full h-full">
      <GeminiSlingshot reachyMiniConfig={reachyMiniConfig} />
    </div>
  );
};

export default App;
