const socket = io({
    transports: ['websocket', 'polling'],
    reconnection: true,
    reconnectionDelay: 1000,
    reconnectionAttempts: 5
});

let allPackets = [];
let selectedPacket = null;

socket.on('connect', () => {
    console.log('✓ Connected to server');
    document.getElementById('status').textContent = 'Connected';
    document.getElementById('status').style.color = '#4caf50';
});

socket.on('disconnect', () => {
    console.log('✗ Disconnected from server');
    document.getElementById('status').textContent = 'Disconnected';
    document.getElementById('status').style.color = '#f44336';
});

socket.on('connect_error', (error) => {
    console.error('Connection error:', error);
    document.getElementById('status').textContent = 'Connection Error';
    document.getElementById('status').style.color = '#f44336';
});

socket.on('started', () => {
    console.log('Capture started');
    document.getElementById('status').textContent = 'Capturing...';
    document.getElementById('btn-start').disabled = true;
    document.getElementById('btn-stop').disabled = false;
});

socket.on('stopped', () => {
    console.log('Capture stopped');
    document.getElementById('status').textContent = 'Stopped';
    document.getElementById('btn-start').disabled = false;
    document.getElementById('btn-stop').disabled = true;
});

socket.on('cleared', () => {
    allPackets = [];
    document.getElementById('packets').innerHTML = '';
    document.getElementById('details').innerHTML = '<p>Click a packet to view details</p>';
});

socket.on('packet', (pkt) => {
    allPackets.unshift(pkt);
    if (allPackets.length > 500) {
        allPackets.pop();
    }
    
    addPacketRow(pkt);
});

socket.on('stats', (stats) => {
    document.getElementById('total').textContent = stats.total;
    document.getElementById('normal').textContent = stats.normal;
    document.getElementById('attack').textContent = stats.attack;
    document.getElementById('blocked').textContent = stats.blocked || 0;
    document.getElementById('pps').textContent = stats.pps + ' pkt/s';
    document.getElementById('attack-pct').textContent = stats.attack_pct + '%';
    document.getElementById('uptime').textContent = stats.uptime + 's';
});

socket.on('ip_blocked', (data) => {
    console.log('🚫 IP Blocked:', data.ip);
    alert(`🚫 IP BLOCKED: ${data.ip}\nAttack count: ${data.count}\nTime: ${data.time}`);
    updateBlockedList();
});

socket.on('ip_unblocked', (data) => {
    console.log('✓ IP Unblocked:', data.ip);
    updateBlockedList();
});

socket.on('blocked_ips', (list) => {
    displayBlockedIPs(list);
});

socket.on('error', (data) => {
    alert('Error: ' + data.msg);
});

function addPacketRow(pkt) {
    const tbody = document.getElementById('packets');
    const row = tbody.insertRow(0);
    
    if (pkt.threat === 'Attack') {
        row.className = 'attack';
    }
    
    if (pkt.blocked) {
        row.className += ' blocked';
    }
    
    row.onclick = () => selectPacket(pkt, row);
    
    const threatClass = pkt.threat === 'Attack' ? 'red' : 
                       pkt.threat === 'Normal' ? 'green' : '';
    
    const threatText = pkt.blocked ? '🚫 BLOCKED' : pkt.threat;
    
    row.innerHTML = `
        <td>${pkt.no}</td>
        <td>${pkt.time}</td>
        <td>${pkt.src}</td>
        <td>${pkt.dst}</td>
        <td>${pkt.proto}</td>
        <td>${pkt.len}</td>
        <td>${pkt.ttl}</td>
        <td class="${threatClass}">${threatText}</td>
        <td>${(pkt.conf * 100).toFixed(0)}%</td>
    `;
    
    // Limit rows
    while (tbody.rows.length > 300) {
        tbody.deleteRow(tbody.rows.length - 1);
    }
}

function selectPacket(pkt, row) {
    document.querySelectorAll('tbody tr').forEach(r => r.classList.remove('selected'));
    row.classList.add('selected');
    
    selectedPacket = pkt;
    showDetails(pkt);
}

function showDetails(pkt) {
    const details = document.getElementById('details');
    
    details.innerHTML = `
        <div class="detail-row">
            <span class="detail-label">Packet No:</span>
            <span class="detail-value">${pkt.no}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Time:</span>
            <span class="detail-value">${pkt.time}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Source IP:</span>
            <span class="detail-value">${pkt.src}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Dest IP:</span>
            <span class="detail-value">${pkt.dst}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Protocol:</span>
            <span class="detail-value">${pkt.proto}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Length:</span>
            <span class="detail-value">${pkt.len} bytes</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">TTL:</span>
            <span class="detail-value">${pkt.ttl}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Threat:</span>
            <span class="detail-value ${pkt.threat === 'Attack' ? 'red' : 'green'}">${pkt.threat}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Confidence:</span>
            <span class="detail-value">${(pkt.conf * 100).toFixed(2)}%</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Attack Prob:</span>
            <span class="detail-value">${(pkt.prob * 100).toFixed(2)}%</span>
        </div>
    `;
    
    // Update analysis panel
    const threat = document.getElementById('threat');
    threat.textContent = pkt.threat;
    threat.className = 'threat-badge ' + (pkt.threat === 'Attack' ? 'attack' : 'normal');
    
    document.getElementById('confidence').textContent = (pkt.conf * 100).toFixed(1) + '%';
    
    const probBar = document.getElementById('prob-bar');
    const probText = document.getElementById('prob-text');
    const prob = pkt.prob * 100;
    probBar.style.width = prob + '%';
    probText.textContent = prob.toFixed(1) + '%';
}

function startCapture() {
    socket.emit('start');
}

function stopCapture() {
    socket.emit('stop');
}

function clearAll() {
    socket.emit('clear');
}

function exportData() {
    const data = JSON.stringify(allPackets, null, 2);
    const blob = new Blob([data], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ddos_capture_${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
}

function showBlockedIPs() {
    socket.emit('get_blocked_ips');
}

function updateBlockedList() {
    socket.emit('get_blocked_ips');
}

function displayBlockedIPs(list) {
    const container = document.getElementById('blocked-list');
    
    if (!list || list.length === 0) {
        container.innerHTML = '<p>No IPs blocked yet</p>';
        return;
    }
    
    container.innerHTML = list.map(item => `
        <div class="blocked-item">
            <div class="blocked-ip">${item.ip}</div>
            <div class="blocked-count">Attacks: ${item.count}</div>
            <button onclick="unblockIP('${item.ip}')" class="btn-unblock">Unblock</button>
        </div>
    `).join('');
}

function unblockIP(ip) {
    if (confirm(`Unblock ${ip}?`)) {
        socket.emit('unblock_ip', { ip: ip });
    }
}
