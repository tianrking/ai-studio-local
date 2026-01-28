#!/usr/bin/env python3
"""
ReachyMini Backend Server with Robot Control

Antenna behaviors (opposite motor directions):
- Idle: Antennas breathe open/close (↔ ↕)
- Drawing: Antennas fold inward (→←)
- Firing: Antennas spread outward (←→)
- Eliminated: Body spin celebration (correct hit! blocks input)

Prerequisites:
    reachy-mini-daemon should be running
"""

import os
import json
import uuid
import math
import threading
import time
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose


app = Flask(__name__)
CORS(app)

PORT = int(os.environ.get('PORT', 3001))

recent_events = []
MAX_EVENTS = 100

# Robot state
robot_state = {
    'mode': 'idle',  # idle, drawing, fired
    'power_level': 0.0,
    'animating': False  # Busy with animation, ignore events
}

idle_thread_running = True
idle_lock = threading.Lock()

# Static head pose - never changes (camera stability)
STATIC_HEAD_POSE = create_head_pose(
    x=0, y=0, z=10,
    roll=0, pitch=0, yaw=0,
    degrees=True, mm=True
)

# Robot instance
robot = ReachyMini(media_backend='no_media')
print("✅ ReachyMini initialized")


# ========================================================================
# MOTION CONTROL
# ========================================================================

def goto_antennas(left_deg, right_deg, duration=0.15):
    """Move antennas with smooth interpolation."""
    try:
        left_rad = math.radians(left_deg)
        right_rad = math.radians(right_deg)

        robot.goto_target(
            head=STATIC_HEAD_POSE,
            antennas=[left_rad, right_rad],
            duration=duration
        )
    except Exception as e:
        pass  # Ignore errors for smooth animation


def set_antennas(left_deg, right_deg):
    """Set antenna angles immediately (for instant response)."""
    try:
        left_rad = math.radians(left_deg)
        right_rad = math.radians(right_deg)

        robot.set_target(
            head=STATIC_HEAD_POSE,
            antennas=[left_rad, right_rad]
        )
    except Exception as e:
        pass


def goto_body(body_yaw_deg, duration=0.3):
    """Rotate body smoothly."""
    try:
        body_yaw_rad = math.radians(body_yaw_deg)

        robot.goto_target(
            head=STATIC_HEAD_POSE,
            antennas=[0, 0],
            body_yaw=body_yaw_rad,
            duration=duration
        )
    except Exception as e:
        pass


# ========================================================================
# IDLE ANIMATION - antennas breathe open/close
# ========================================================================

def idle_animation_loop():
    """Antennas breathe open/close continuously."""
    global idle_thread_running

    phase = 0
    while idle_thread_running:
        with idle_lock:
            if robot_state['mode'] == 'idle':
                # Breathing: antennas open/close (opposite directions)
                # Left: -25° to +25°, Right: +25° to -25°
                phase += 0.1  # Moderate speed
                angle = math.sin(phase) * 25

                # Use set_target for immediate, smooth response
                set_antennas(angle, -angle)

        time.sleep(0.08)  # ~12 FPS


idle_thread = threading.Thread(target=idle_animation_loop, daemon=True)
idle_thread.start()
print("✅ Idle animation started")


# ========================================================================
# EVENT HANDLERS
# ========================================================================

def handle_slingshot_draw(data):
    """Drawing - antennas fold inward."""
    power_ratio = data.get('powerRatio', 0)
    power_percent = round(power_ratio * 100)

    print(f"   🤖 [DRAW] Power: {power_percent}%")

    with idle_lock:
        robot_state['mode'] = 'drawing'

    # Antennas fold INWARD: left negative, right positive
    angle = power_ratio * 40
    set_antennas(-angle, angle)


def handle_slingshot_fire(data):
    """Firing - antennas spread outward!"""
    power_ratio = data.get('powerRatio', 0)
    power_percent = round(power_ratio * 100)

    print(f"   🤖 [FIRE] Power: {power_percent}%")

    with idle_lock:
        robot_state['mode'] = 'fired'

    # Antennas spread OUTWARD: left positive, right negative
    angle = power_ratio * 50
    set_antennas(angle, -angle)

    # Return to idle after delay
    def return_to_idle():
        time.sleep(0.4)
        with idle_lock:
            robot_state['mode'] = 'idle'

    threading.Thread(target=return_to_idle, daemon=True).start()


def handle_bubble_eliminated(data):
    """Bubbles eliminated (correct hit!) - body celebration animation."""
    count = data.get('count', 0)
    color = data.get('colorLabel', 'Unknown')

    print(f"   🤖 [ELIMINATED] {count} {color} bubbles - celebration spin!")

    with idle_lock:
        robot_state['animating'] = True
        robot_state['mode'] = 'celebrating'

    # Body spin animation for celebration
    try:
        # Rotate left
        goto_body(-30, duration=0.2)
        time.sleep(0.25)

        # Rotate right (faster)
        goto_body(30, duration=0.15)
        time.sleep(0.2)

        # Return to center
        goto_body(0, duration=0.25)
        time.sleep(0.3)
    except Exception as e:
        print(f"   ❌ Animation error: {e}")

    with idle_lock:
        robot_state['animating'] = False
        robot_state['mode'] = 'idle'

    print("   ✅ Animation complete - accepting events again")


# ========================================================================
# HELPER FUNCTIONS
# ========================================================================

def add_event(event):
    recent_events.append(event)
    if len(recent_events) > MAX_EVENTS:
        recent_events.pop(0)


def log_event(event_type, timestamp, data):
    print(f"\n{'='*60}")
    print(f"{'='*20} [{event_type.upper()}] {'='*20}")
    print(f"{'='*60}")
    print(f"   Time: {timestamp}")
    print(f"   Data: {json.dumps(data, indent=2, ensure_ascii=False)}")
    print(f"{'='*60}\n")


# ========================================================================
# API ENDPOINTS
# ========================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'robot': {
            'connected': True,
            'mode': robot_state['mode']
        },
        'eventsReceived': len(recent_events)
    })


@app.route('/api/events', methods=['GET'])
def get_events():
    return jsonify({'count': len(recent_events), 'events': recent_events})


@app.route('/api/events', methods=['DELETE'])
def clear_events():
    recent_events.clear()
    return jsonify({'status': 'cleared'})


@app.route('/api/events', methods=['POST'])
def receive_event():
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

    handlers = {
        'slingshot_draw': handle_slingshot_draw,
        'slingshot_fire': handle_slingshot_fire,
        'bubble_eliminated': handle_bubble_eliminated,
    }

    # Skip events if busy animating (body spin)
    if robot_state['animating']:
        print(f"   ⏸️  Animation in progress - event ignored")
        return jsonify({'status': 'ignored', 'reason': 'animating'})

    handler = handlers.get(event_type)
    if handler:
        try:
            handler(data)
        except Exception as e:
            print(f"   ❌ Error: {e}")

    return jsonify({'status': 'received', 'eventId': event['id']})


# ========================================================================
# MAIN
# ========================================================================

if __name__ == '__main__':
    print(f"""
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║       ReachyMini Backend Server + Robot Control           ║
║                                                            ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  ✅ Robot: CONNECTED                                       ║
║  🔒 Head: LOCKED (camera stability)                       ║
║                                                            ║
║  Status: http://localhost:{PORT}                             ║
║                                                            ║
║  Robot Behaviors:                                          ║
║    🎯 Idle       - Antennas breathe open/close            ║
║    🎯 Drawing    - Antennas fold inward (→←)              ║
║    🎯 Firing     - Antennas spread outward (←→)            ║
║    🎯 Eliminated - Body spin celebration (correct hit!)    ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
""")

    try:
        app.run(host='0.0.0.0', port=PORT, debug=True, use_reloader=False)
    finally:
        idle_thread_running = False
        print("\n✅ Server stopped")
