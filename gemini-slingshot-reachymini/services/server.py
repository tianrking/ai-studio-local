#!/usr/bin/env python3
"""
ReachyMini Backend Server (Python)

A simple Flask server that receives game events from the frontend
and logs them for the ReachyMini robot integration.

Endpoints:
- GET  /api/health   - Health check
- GET  /api/events   - View recent events
- DELETE /api/events - Clear events history
- POST /api/events   - Receive game events
"""

import os
import json
import uuid
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

PORT = int(os.environ.get('PORT', 3001))

# Store recent events for debugging
recent_events = []
MAX_EVENTS = 100


def add_event(event):
    """Add event to history, maintaining max size."""
    recent_events.append(event)
    if len(recent_events) > MAX_EVENTS:
        recent_events.pop(0)


def log_event(event_type, timestamp, data):
    """Print event to console with formatted output."""
    print(f"\n{'='*60}")
    print(f"{'='*20} [{event_type.upper()}] {'='*20}")
    print(f"{'='*60}")
    print(f"   Time: {timestamp}")
    print(f"   Data: {json.dumps(data, indent=2, ensure_ascii=False)}")
    print(f"{'='*60}\n")


# ========================================================================
# EVENT HANDLERS - Add your ReachyMini robot commands here
# ========================================================================

def handle_slingshot_draw(data):
    """Handle slingshot draw event (when player is pulling back)."""
    power_percent = round(data.get('powerRatio', 0) * 100)
    drag_distance = data.get('dragDistance', 0)
    angle = data.get('angle', 0)

    print(f"   🤖 [DRAW] Power: {power_percent}%, Distance: {drag_distance}, Angle: {angle:.2f} rad")

    # High power draw (> 70%) - robot gets excited
    if data.get('powerRatio', 0) > 0.7:
        print("   🤖 Robot: High power detected - preparing for big shot!")
        # TODO: Send command to ReachyMini
        # await reachy_mini.animate('anticipation_high')


def handle_slingshot_fire(data):
    """Handle slingshot fire event (when ball is released)."""
    power_percent = round(data.get('powerRatio', 0) * 100)
    velocity = data.get('velocity', {})
    color = data.get('color', 'unknown')

    print(f"   🤖 [FIRE] Power: {power_percent}%, Color: {color}")
    print(f"   🤖 [FIRE] Velocity: vx={velocity.get('vx', 0):.1f}, vy={velocity.get('vy', 0):.1f}")

    # Power shot (> 80%) - robot watches intensely
    if data.get('powerRatio', 0) > 0.8:
        print("   🤖 Robot: Power shot! Tracking trajectory...")
        # TODO: Send command to ReachyMini
        # await reachy_mini.animate('watch_intense')


def handle_ball_collision(data):
    """Handle ball collision event (when ball hits a bubble)."""
    hit_color = data.get('hitBubbleColor', 'unknown')
    collision_pos = data.get('collisionPosition', {})

    print(f"   🤖 [COLLISION] Hit {hit_color} bubble at ({collision_pos.get('x', 0)}, {collision_pos.get('y', 0)})")
    # TODO: Send command to ReachyMini
    # await reachy_mini.animate('flinch')


def handle_bubble_eliminated(data):
    """Handle bubble elimination event (when bubbles are popped)."""
    count = data.get('count', 0)
    color_label = data.get('colorLabel', 'Unknown')
    points = data.get('totalPoints', 0)

    print(f"   🤖 [ELIMINATED] {count} {color_label} bubbles, {points} pts")

    if count >= 5:
        print("   🤖 Robot: Big combo! Celebrating!")
        # TODO: Send command to ReachyMini
        # await reachy_mini.animate('celebrate_combo')
    elif count >= 3:
        print("   🤖 Robot: Nice shot!")
        # TODO: Send command to ReachyMini
        # await reachy_mini.animate('nod_approval')


def handle_game_win(data):
    """Handle game win event (when all bubbles are cleared)."""
    final_score = data.get('finalScore', 0)
    shots_fired = data.get('shotsFired', 0)
    duration_ms = data.get('duration', 0)
    duration_sec = round(duration_ms / 1000)

    print(f"   🤖 [GAME WIN] Score: {final_score}, Shots: {shots_fired}, Time: {duration_sec}s")
    print("   🤖 Robot: 🎉 VICTORY DANCE! 🎉")
    # TODO: Send command to ReachyMini
    # await reachy_mini.animate('victory')


# ========================================================================
# API ENDPOINTS
# ========================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    uptime_seconds = 0  # TODO: Implement actual uptime tracking
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'uptime': uptime_seconds,
        'eventsReceived': len(recent_events)
    })


@app.route('/api/events', methods=['GET'])
def get_events():
    """Get recent events."""
    return jsonify({
        'count': len(recent_events),
        'events': recent_events
    })


@app.route('/api/events', methods=['DELETE'])
def clear_events():
    """Clear events history."""
    recent_events.clear()
    return jsonify({'status': 'cleared'})


@app.route('/api/events', methods=['POST'])
def receive_event():
    """Main event receiver endpoint."""
    body = request.get_json()
    event_type = body.get('eventType')
    timestamp = body.get('timestamp')
    data = body.get('data', {})

    event = {
        'id': f"{int(datetime.now().timestamp() * 1000)}-{uuid.uuid4().hex[:9]}",
        'eventType': event_type,
        'timestamp': timestamp,
        'data': data,
        'receivedAt': datetime.now().isoformat()
    }

    add_event(event)
    log_event(event_type, timestamp, data)

    # Process event based on type
    try:
        handlers = {
            'slingshot_draw': handle_slingshot_draw,
            'slingshot_fire': handle_slingshot_fire,
            'ball_collision': handle_ball_collision,
            'bubble_eliminated': handle_bubble_eliminated,
            'game_win': handle_game_win,
        }

        handler = handlers.get(event_type)
        if handler:
            handler(data)
        else:
            print(f"   ⚠️ Unknown event type: {event_type}")
    except Exception as e:
        print(f"   ❌ Error handling {event_type}: {e}")

    return jsonify({'status': 'received', 'eventId': event['id']})


# ========================================================================
# MAIN
# ========================================================================

if __name__ == '__main__':
    print("""
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║          ReachyMini Backend Server (Python)               ║
║                                                            ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  Status: Running on http://localhost:3001                  ║
║                                                            ║
║  Endpoints:                                                ║
║    GET  /api/health   - Health check                      ║
║    GET  /api/events   - View recent events                ║
║    DELETE /api/events - Clear events history              ║
║    POST /api/events   - Receive game events               ║
║                                                            ║
║  Waiting for game events...                               ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
""")
    app.run(host='0.0.0.0', port=PORT, debug=True)
