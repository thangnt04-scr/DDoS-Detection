from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import pickle
import pandas as pd
import numpy as np
from datetime import datetime
import time
from collections import deque
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# State
monitoring = False
packets = deque(maxlen=500)
stats = {'total': 0, 'normal': 0, 'attack': 0, 'start': None, 'blocked': 0}
requests_log = deque(maxlen=100)
blocked_ips = set()  # IPs that are blocked
ip_attack_count = {}  # Track attack count per IP

# Load model
model = None
try:
    with open('../Phase3_Network_Models/network_xgboost_optimized.pkl', 'rb') as f:
        model = pickle.load(f)
    print("✓ Model loaded")
except:
    print("✗ Model not loaded (will use heuristics)")

def analyze_requests():
    """Analyze request patterns"""
    if len(requests_log) < 2:
        return None
    
    now = time.time()
    recent = [r for r in requests_log if (now - r['time']) < 5]
    
    if len(recent) < 2:
        return None
    
    # Calculate rate
    duration = recent[-1]['time'] - recent[0]['time']
    if duration == 0:
        duration = 0.1
    
    rate = len(recent) / duration
    
    # Simple detection - lower threshold
    is_attack = rate > 3  # More than 3 req/s = suspicious
    confidence = min(0.95, rate / 15)
    
    # ML prediction if available
    if model and len(recent) >= 5:
        try:
            features = {
                'dur': duration,
                'spkts': len(recent),
                'dpkts': len(recent),
                'sbytes': len(recent) * 400,
                'dbytes': len(recent) * 200,
                'rate': rate,
                'sttl': 64, 'dttl': 64,
                'sload': (len(recent) * 400) / duration,
                'dload': (len(recent) * 200) / duration,
                'sloss': 0, 'dloss': 0,
                'sinpkt': duration / len(recent),
                'dinpkt': duration / len(recent),
                'sjit': 0, 'djit': 0,
                'swin': 0, 'stcpb': 0, 'dtcpb': 0, 'dwin': 0,
                'tcprtt': 0, 'synack': 0, 'ackdat': 0,
                'smean': 400, 'dmean': 200,
                'trans_depth': 0, 'response_body_len': 0,
                'ct_srv_src': len(recent),
                'ct_state_ttl': 0, 'ct_dst_ltm': 0,
                'ct_src_dport_ltm': 0, 'ct_dst_sport_ltm': 0,
                'ct_dst_src_ltm': 0
            }
            df = pd.DataFrame([features])
            pred = model.predict(df)[0]
            prob = model.predict_proba(df)[0]
            is_attack = (pred == 1)
            confidence = float(max(prob))
        except Exception as e:
            print(f"ML error: {e}")
    
    return {
        'attack': is_attack,
        'conf': confidence,
        'rate': rate
    }

@app.before_request
def log_request():
    """Log every request and block if needed"""
    global blocked_ips, ip_attack_count
    
    client_ip = request.remote_addr
    
    # Check if IP is blocked
    if client_ip in blocked_ips:
        print(f"🚫 BLOCKED: {client_ip} - {request.method} {request.path}")
        return jsonify({'error': 'Your IP has been blocked due to suspicious activity'}), 403
    
    if not monitoring:
        return
    
    # Skip static and socket.io
    if request.path.startswith('/static') or request.path.startswith('/socket.io'):
        return
    
    # Log request
    req = {
        'time': time.time(),
        'ip': client_ip,
        'method': request.method,
        'path': request.path
    }
    requests_log.append(req)
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {request.method} {request.path} from {client_ip}")
    
    # Analyze
    analysis = analyze_requests()
    if not analysis:
        # Still create packet even without analysis
        pkt = {
            'no': stats['total'] + 1,
            'time': datetime.now().strftime('%H:%M:%S'),
            'src': client_ip,
            'dst': '127.0.0.1',
            'proto': 'HTTP',
            'len': 400,
            'ttl': 64,
            'threat': 'Unknown',
            'conf': 0,
            'prob': 0,
            'blocked': False
        }
        stats['total'] += 1
        packets.append(pkt)
        socketio.emit('packet', pkt)
        return
    
    # Create packet
    pkt = {
        'no': stats['total'] + 1,
        'time': datetime.now().strftime('%H:%M:%S'),
        'src': client_ip,
        'dst': '127.0.0.1',
        'proto': 'HTTP',
        'len': 400,
        'ttl': 64,
        'threat': 'Attack' if analysis['attack'] else 'Normal',
        'conf': analysis['conf'],
        'prob': analysis['conf'] if analysis['attack'] else 1 - analysis['conf'],
        'blocked': False
    }
    
    # Update stats
    stats['total'] += 1
    if analysis['attack']:
        stats['attack'] += 1
        
        # Track attack count per IP
        ip_attack_count[client_ip] = ip_attack_count.get(client_ip, 0) + 1
        
        # Block IP if too many attacks (threshold: 5 attacks)
        if ip_attack_count[client_ip] >= 5:
            blocked_ips.add(client_ip)
            stats['blocked'] += 1
            pkt['blocked'] = True
            print(f"🚫 BLOCKED IP: {client_ip} (attack count: {ip_attack_count[client_ip]})")
            
            # Notify clients
            socketio.emit('ip_blocked', {
                'ip': client_ip,
                'count': ip_attack_count[client_ip],
                'time': datetime.now().strftime('%H:%M:%S')
            })
    else:
        stats['normal'] += 1
    
    packets.append(pkt)
    
    # Send to clients
    socketio.emit('packet', pkt)
    
    if stats['total'] % 5 == 0:
        send_stats()

def send_stats():
    """Send stats to clients"""
    uptime = time.time() - stats['start'] if stats['start'] else 0
    pps = stats['total'] / uptime if uptime > 0 else 0
    attack_pct = stats['attack'] / stats['total'] * 100 if stats['total'] > 0 else 0
    
    socketio.emit('stats', {
        'total': stats['total'],
        'normal': stats['normal'],
        'attack': stats['attack'],
        'blocked': stats['blocked'],
        'pps': round(pps, 1),
        'attack_pct': round(attack_pct, 1),
        'uptime': round(uptime, 1)
    })

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    """Test endpoint for generating traffic"""
    return 'OK'

@socketio.on('start')
def handle_start():
    global monitoring, stats
    monitoring = True
    stats['start'] = time.time()
    print("✓ Monitoring started")
    emit('started', broadcast=True)

@socketio.on('stop')
def handle_stop():
    global monitoring
    monitoring = False
    print("✓ Monitoring stopped")
    emit('stopped', broadcast=True)

@socketio.on('clear')
def handle_clear():
    global stats, blocked_ips, ip_attack_count
    packets.clear()
    requests_log.clear()
    blocked_ips.clear()
    ip_attack_count.clear()
    stats = {'total': 0, 'normal': 0, 'attack': 0, 'start': None, 'blocked': 0}
    emit('cleared', broadcast=True)

@socketio.on('unblock_ip')
def handle_unblock(data):
    """Unblock an IP"""
    ip = data.get('ip')
    if ip in blocked_ips:
        blocked_ips.remove(ip)
        if ip in ip_attack_count:
            del ip_attack_count[ip]
        stats['blocked'] -= 1
        print(f"✓ Unblocked IP: {ip}")
        emit('ip_unblocked', {'ip': ip}, broadcast=True)

@socketio.on('get_blocked_ips')
def handle_get_blocked():
    """Get list of blocked IPs"""
    blocked_list = [{'ip': ip, 'count': ip_attack_count.get(ip, 0)} for ip in blocked_ips]
    emit('blocked_ips', blocked_list)

if __name__ == '__main__':
    print("="*60)
    print("DDoS Detector - HTTP Monitoring Mode")
    print("="*60)
    print("✓ No admin required")
    print("✓ Monitors HTTP requests to this server")
    print("✓ Access: http://localhost:5000")
    print("="*60)
    print("\nTo test:")
    print("1. Open http://localhost:5000")
    print("2. Click 'Start'")
    print("3. Run: python start.py GET http://127.0.0.1:5000 4 100 proxy.txt 100 60")
    print("="*60)
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
