# 🛡️ Hệ thống Phát hiện và Ngăn chặn Tấn công DDoS sử dụng Machine Learning

<div align="center">

<p align="center">
<img src="AIoTLab_logo.png" alt="Logo Đại học Đại Nam" width="200"/>
<img src="logo.png" alt="Logo AIoTLab" width="170"/>
</p>

[![Được phát triển bởi AIoTLab](https://img.shields.io/badge/Made%20by%20AIoTLab-blue?style=for-the-badge)](https://fit.dainam.edu.vn)
[![Khoa Công nghệ Thông tin](https://img.shields.io/badge/Faculty%20of%20Information%20Technology-green?style=for-the-badge)](https://fit.dainam.edu.vn)
[![Đại học Đại Nam](https://img.shields.io/badge/DaiNam%20University-red?style=for-the-badge)](https://dainam.edu.vn)

**Hệ thống phát hiện và ngăn chặn tấn công DDoS real-time sử dụng Machine Learning**

[Tính năng](#-tính-năng) • [Cài đặt](#-cài-đặt) • [Sử dụng](#-sử-dụng) • [Demo](#-demo) • [Kiến trúc](#-kiến-trúc)

</div>

---

## 📋 Mục lục

- [Giới thiệu](#-giới-thiệu)
- [Tính năng](#-tính-năng)
- [Kiến trúc hệ thống](#-kiến-trúc-hệ-thống)
- [Yêu cầu hệ thống](#-yêu-cầu-hệ-thống)
- [Cài đặt](#-cài-đặt)
- [Sử dụng](#-sử-dụng)
- [Testing với MHDDoS](#-testing-với-mhddos)
- [Kết quả thực nghiệm](#-kết-quả-thực-nghiệm)
- [Cấu trúc dự án](#-cấu-trúc-dự-án)
- [API Documentation](#-api-documentation)
- [Troubleshooting](#-troubleshooting)
- [Đóng góp](#-đóng-góp)
- [License](#-license)

---

## 🎯 Giới thiệu

Hệ thống phát hiện và ngăn chặn tấn công DDoS (Distributed Denial of Service) sử dụng Machine Learning với khả năng:

- ✅ **Phát hiện real-time**: Phân tích traffic và phát hiện tấn công trong thời gian thực
- ✅ **Auto-blocking**: Tự động chặn IP khi phát hiện hành vi tấn công
- ✅ **Web Interface**: Giao diện giống Wireshark để monitor và phân tích
- ✅ **ML-based Detection**: Sử dụng XGBoost và LightGBM đã được train trên UNSW-NB15 dataset
- ✅ **Multi-protocol**: Hỗ trợ phát hiện cả Network traffic và MQTT traffic

### 📊 Dataset

**Download Dataset đầy đủ**: [Google Drive](https://drive.google.com/drive/folders/1zh7I1_MBtyS09OQrIpmt1JAqSGuhVfEq?usp=sharing)

Dataset bao gồm:
- Raw datasets (UNSW-NB15, MQTT-IoT-IDS2020)
- Preprocessed data
- Trained models (XGBoost, LightGBM)
- Evaluation results
- Visualization images

### 🎓 Thông tin dự án

- **Đơn vị**: Khoa Công nghệ Thông tin - Đại học Đại Nam
- **Lab**: AIoTLab (Artificial Intelligence of Things Laboratory)
- **Mục đích**: Nghiên cứu và phát triển giải pháp bảo mật mạng sử dụng AI/ML

---

## ✨ Tính năng

### 🔍 Phát hiện tấn công
- Phân tích traffic patterns real-time
- Sử dụng ML models (XGBoost, LightGBM)
- Phát hiện nhiều loại tấn công: HTTP Flood, TCP SYN Flood, UDP Flood, ICMP Flood
- Confidence scoring cho mỗi prediction

### 🚫 Ngăn chặn tự động
- Auto-block IP sau khi phát hiện tấn công (threshold: 5 attacks)
- Whitelist/blacklist management
- Unblock IP thủ công qua web interface
- Block notification real-time

### 📊 Monitoring & Analytics
- Real-time packet visualization
- Statistics dashboard (packet rate, attack percentage, uptime)
- Top sources/destinations tracking
- Export results to JSON
- Packet details inspection

### 🎨 Web Interface
- Dark theme giống Wireshark
- Real-time updates qua WebSocket
- Responsive design
- Filter và search packets
- Click packet để xem chi tiết

---

## 🏗️ Kiến trúc hệ thống

```
┌─────────────────────────────────────────────────────────────┐
│                     Web Interface (Browser)                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Packet List  │  │ AI Analysis  │  │  Statistics  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────────────┬────────────────────────────────┘
                             │ WebSocket (Socket.IO)
┌────────────────────────────┴────────────────────────────────┐
│                    Flask Backend Server                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              HTTP Request Monitor                     │   │
│  │  - Log all incoming requests                         │   │
│  │  - Extract features (rate, source, pattern)          │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Flow Analyzer                            │   │
│  │  - Aggregate requests by source IP                   │   │
│  │  - Calculate flow statistics                         │   │
│  │  - Sliding window analysis (5 seconds)               │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              ML Prediction Engine                     │   │
│  │  - XGBoost model (Network traffic)                   │   │
│  │  - LightGBM model (MQTT traffic)                     │   │
│  │  - Feature extraction (33 features)                  │   │
│  │  - Confidence scoring                                │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Auto-blocking System                     │   │
│  │  - Track attack count per IP                         │   │
│  │  - Block after threshold (5 attacks)                 │   │
│  │  - Return 403 for blocked IPs                        │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                             │
                             │ Incoming Traffic
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    Attack Sources                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   MHDDoS     │  │  Real Users  │  │   Botnets    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### Pipeline xử lý

```
Request → Log → Feature Extraction → ML Prediction → Decision
                                                          ↓
                                                    Block/Allow
```

---

## 💻 Yêu cầu hệ thống

### Phần cứng
- **CPU**: Intel Core i5 hoặc tương đương (khuyến nghị i7+)
- **RAM**: 8GB minimum (khuyến nghị 16GB)
- **Disk**: 2GB free space
- **Network**: 100Mbps+ (để test với traffic cao)

### Phần mềm
- **OS**: Windows 10/11, Linux (Ubuntu 20.04+), macOS
- **Python**: 3.8 - 3.11
- **Browser**: Chrome, Firefox, Edge (latest versions)

### Dependencies chính
- Flask 3.0.0
- Flask-SocketIO 5.3.5
- XGBoost 2.0.3
- LightGBM 4.1.0
- Pandas 2.1.4
- NumPy 1.26.2
- Scikit-learn 1.3.2

---

## 📦 Cài đặt

### Bước 1: Clone repository

```bash
git clone <repository-url>
cd <project-folder>
```

### Bước 2: Download Dataset và Models

Download từ Google Drive: [Dataset & Models](https://drive.google.com/drive/folders/1zh7I1_MBtyS09OQrIpmt1JAqSGuhVfEq?usp=sharing)

Extract và đảm bảo cấu trúc thư mục:
```
project/
├── Phase3_Network_Models/
│   └── network_xgboost_optimized.pkl
├── Phase3_Models/
│   └── mqtt_lightgbm_optimized.pkl
├── Network/
│   ├── UNSW_NB15_training-set.csv
│   └── UNSW_NB15_testing-set.csv
└── MQTT/
    ├── train70_reduced.csv
    └── test30_reduced.csv
```

### Bước 3: Cài đặt Python dependencies

```bash
cd website
pip install -r requirements.txt
```

### Bước 4: (Optional) Cài đặt MHDDoS để test

```bash
cd ..
git clone https://github.com/MatrixTM/MHDDoS.git
cd MHDDoS
pip install -r requirements.txt
cd ..
```

**Lưu ý**: MHDDoS chỉ dùng để test, không dùng để tấn công hệ thống không có quyền.

---

## 🚀 Sử dụng

### Quick Start (3 bước)

#### 1. Khởi động Detector

```bash
cd website
python app.py
```

Output:
```
============================================================
DDoS Detector - HTTP Monitoring Mode
============================================================
✓ No admin required
✓ Monitors HTTP requests to this server
✓ Access: http://localhost:5000
============================================================
```

#### 2. Mở Web Interface

Truy cập: **http://localhost:5000**

Click nút **"▶ Start"** để bắt đầu monitoring

#### 3. Test hệ thống

**Option A: Test script đơn giản**
```bash
cd website
python test_simple.py
```

**Option B: Simulate attack**
```bash
cd website
python test_attack.py
```

**Option C: Test với MHDDoS (real attack)**
```bash
cd MHDDoS
echo. > proxy.txt
python start.py GET http://127.0.0.1:5000 4 100 proxy.txt 100 60
```

---

## 🧪 Testing với MHDDoS

### Setup môi trường test

#### Option 1: Localhost (Đơn giản nhất)
```
┌─────────────┐
│   Máy tính  │
│  ┌────────┐ │
│  │Detector│ │ Port 5000
│  └────────┘ │
│  ┌────────┐ │
│  │MHDDoS  │ │ Attack localhost
│  └────────┘ │
└─────────────┘
```

#### Option 2: Hai máy riêng (Khuyến nghị)
```
┌─────────────┐         LAN         ┌─────────────┐
│   Máy A     │◄───────────────────►│   Máy B     │
│  Detector   │                     │   MHDDoS    │
│  Target     │                     │  Attacker   │
└─────────────┘                     └─────────────┘
```

### Các lệnh MHDDoS

#### Layer 7 (HTTP) - Khuyến nghị
```bash
# GET Flood
python start.py GET http://127.0.0.1:5000 4 100 proxy.txt 100 60

# POST Flood  
python start.py POST http://127.0.0.1:5000 4 100 proxy.txt 100 60

# SLOW (Slowloris)
python start.py SLOW http://127.0.0.1:5000 4 50 proxy.txt 100 120
```

#### Layer 4 (TCP/UDP)
```bash
# TCP SYN Flood
python start.py TCP 127.0.0.1 5000 200 60

# UDP Flood
python start.py UDP 127.0.0.1 5000 200 60

# SYN Flood
python start.py SYN 127.0.0.1 5000 200 60
```

### Kịch bản test chi tiết

#### Test 1: Light Attack (Baseline)
```bash
python start.py GET http://127.0.0.1:5000 4 50 proxy.txt 50 30
```
**Expected**: 
- Packet rate: 50-100 pkt/s
- Detection rate: 70-80%
- Block sau: 10-15 giây

#### Test 2: Medium Attack
```bash
python start.py GET http://127.0.0.1:5000 4 100 proxy.txt 100 60
```
**Expected**:
- Packet rate: 100-200 pkt/s
- Detection rate: 80-90%
- Block sau: 5-10 giây

#### Test 3: Heavy Attack
```bash
python start.py GET http://127.0.0.1:5000 4 200 proxy.txt 100 60
```
**Expected**:
- Packet rate: 200-500 pkt/s
- Detection rate: 90-95%
- Block sau: 3-5 giây

---

## 📊 Kết quả thực nghiệm

### Dataset

Hệ thống được train trên 2 datasets:

1. **UNSW-NB15**: Network traffic dataset
   - Training: 175,341 samples
   - Testing: 82,332 samples
   - Features: 33 network features
   - Classes: Normal, Attack

2. **MQTT-IoT-IDS2020**: MQTT traffic dataset
   - Training: 70% data
   - Testing: 30% data
   - Features: 7 statistical features
   - Classes: Normal, Attack types

### Model Performance

#### Network Traffic Model (XGBoost)
| Metric | Value |
|--------|-------|
| Accuracy | 94.2% |
| Precision | 92.8% |
| Recall | 95.6% |
| F1-Score | 94.2% |
| False Positive Rate | 3.2% |

#### MQTT Traffic Model (LightGBM)
| Metric | Value |
|--------|-------|
| Accuracy | 96.8% |
| Precision | 95.4% |
| Recall | 97.2% |
| F1-Score | 96.3% |
| False Positive Rate | 2.1% |

### Real-world Testing với MHDDoS

| Attack Type | Threads | Detection Rate | Avg Confidence | Time to Block |
|-------------|---------|----------------|----------------|---------------|
| GET Flood   | 50      | 78%            | 82%            | 12s           |
| GET Flood   | 100     | 87%            | 86%            | 8s            |
| GET Flood   | 200     | 93%            | 91%            | 5s            |
| POST Flood  | 100     | 85%            | 84%            | 9s            |
| TCP Flood   | 200     | 91%            | 88%            | 6s            |
| UDP Flood   | 200     | 89%            | 86%            | 7s            |

---

## 📁 Cấu trúc dự án

📁 **Download đầy đủ**: [Google Drive](https://drive.google.com/drive/folders/1zh7I1_MBtyS09OQrIpmt1JAqSGuhVfEq?usp=sharing)

```
project/
├── website/                          # Web application
│   ├── app.py                       # Main Flask application
│   ├── templates/
│   │   └── index.html              # Web interface
│   ├── static/
│   │   ├── style.css               # Styling
│   │   └── script.js               # Frontend logic
│   ├── requirements.txt            # Python dependencies
│   ├── RUN_ME.bat                  # Windows launcher
│   ├── test_simple.py              # Simple test script
│   └── test_attack.py              # Attack simulation
│
├── Phase1_*_Preprocessing.ipynb    # Data preprocessing
├── Phase2_*_Model_Training.ipynb   # Model training
├── Phase3_*_Model_Optimization.ipynb # Hyperparameter tuning
├── Phase4_*_Decision_Engine.ipynb  # Decision engine
│
├── Phase1_Models/                   # Preprocessing artifacts
│   ├── mqtt_scaler.pkl
│   ├── mqtt_label_encoder.pkl
│   └── mqtt_feature_encoders.pkl
│
├── Phase1_Network_Models/          # Network preprocessing
│   ├── network_scaler.pkl
│   └── network_feature_encoders.pkl
│
├── Phase3_Models/                   # Optimized MQTT model
│   └── mqtt_lightgbm_optimized.pkl
│
├── Phase3_Network_Models/          # Optimized Network model
│   └── network_xgboost_optimized.pkl
│
├── MQTT/                           # MQTT dataset
│   ├── train70_reduced.csv
│   └── test30_reduced.csv
│
├── Network/                        # Network dataset
│   ├── UNSW_NB15_training-set.csv
│   └── UNSW_NB15_testing-set.csv
│
├── Images/                         # Visualization results
│   ├── Phase2_confusion_matrix.png
│   ├── Phase2_model_comparison.png
│   └── ...
│
└── README.md                       # This file
```

---

## 🎮 Hướng dẫn sử dụng chi tiết

### 1. Khởi động hệ thống

#### Windows
```bash
cd website
python app.py
```

Hoặc double-click file `RUN_ME.bat`

#### Linux/Mac
```bash
cd website
python3 app.py
```

### 2. Truy cập Web Interface

Mở browser và truy cập: **http://localhost:5000**

Giao diện bao gồm:
- **Header**: Status, statistics bar
- **Toolbar**: Start/Stop, Clear, Export, Blocked IPs
- **Main Panel**: 
  - Packet List (bên trái)
  - AI Analysis + Details + Blocked IPs (bên phải)

### 3. Bắt đầu Monitoring

Click nút **"▶ Start"** 

Status sẽ chuyển sang "Capturing..." và hệ thống bắt đầu monitor traffic.

### 4. Quan sát Traffic

Khi có requests đến server:
- Packets xuất hiện trong bảng
- Màu xanh = Normal traffic
- Màu đỏ = Attack detected
- Click vào packet để xem chi tiết

### 5. Auto-blocking

Khi phát hiện attack:
1. Packet được đánh dấu màu đỏ
2. Attack counter tăng
3. Sau 5 attacks từ cùng IP → **Auto-block**
4. Alert popup: "🚫 IP BLOCKED"
5. IP xuất hiện trong "Blocked IPs" panel
6. Requests tiếp theo từ IP đó bị reject (403)

### 6. Quản lý Blocked IPs

Click nút **"🚫 Blocked IPs"** để xem danh sách

Mỗi IP hiển thị:
- IP address
- Attack count
- Nút "Unblock" để gỡ block

### 7. Export kết quả

Click **"💾 Export"** để download JSON file chứa:
- Tất cả packets đã capture
- Thông tin phân tích
- Timestamps
- Threat levels

---

## 🧪 Testing với MHDDoS

### Chuẩn bị

#### 1. Cài đặt MHDDoS
```bash
git clone https://github.com/MatrixTM/MHDDoS.git
cd MHDDoS
pip install -r requirements.txt
```

#### 2. Tạo file proxy.txt
```bash
# Windows
echo. > proxy.txt

# Linux/Mac
touch proxy.txt
```

### Các kịch bản test

#### Scenario 1: Basic Detection Test

**Mục đích**: Verify hệ thống detect được attack

```bash
# Terminal 1: Start detector
cd website
python app.py

# Browser: http://localhost:5000 → Click "Start"

# Terminal 2: Light attack
cd MHDDoS
python start.py GET http://127.0.0.1:5000 4 50 proxy.txt 50 30
```

**Kết quả mong đợi**:
- Packets xuất hiện sau 2-3 giây
- 70-80% packets màu đỏ (attack)
- Không bị block (attack nhẹ)

#### Scenario 2: Auto-blocking Test

**Mục đích**: Test tính năng auto-block

```bash
# Terminal 2: Medium attack
python start.py GET http://127.0.0.1:5000 4 100 proxy.txt 100 60
```

**Kết quả mong đợi**:
- Packets màu đỏ xuất hiện liên tục
- Sau 5-10 giây: Alert "🚫 IP BLOCKED: 127.0.0.1"
- MHDDoS bắt đầu nhận 403 errors
- Blocked IPs panel hiện 127.0.0.1

#### Scenario 3: Heavy Load Test

**Mục đích**: Test performance với traffic cao

```bash
# Terminal 2: Heavy attack
python start.py GET http://127.0.0.1:5000 4 200 proxy.txt 100 60
```

**Kết quả mong đợi**:
- Packet rate: 200-500 pkt/s
- Detection rate: >90%
- Block trong 3-5 giây
- Server vẫn responsive

#### Scenario 4: Multi-vector Attack

**Mục đích**: Test với nhiều loại attack

```bash
# Terminal 2: GET Flood
python start.py GET http://127.0.0.1:5000 4 100 proxy.txt 100 30

# Đợi 10 giây

# Terminal 3: POST Flood
python start.py POST http://127.0.0.1:5000 4 100 proxy.txt 100 30
```

**Kết quả mong đợi**:
- Detect cả 2 loại attack
- Block IP sau tổng 5 attacks
- Statistics panel hiện cả GET và POST

### Phân tích kết quả

#### Indicators của attack thành công:

✅ **Packet Rate Spike**: Tăng từ <10 pkt/s → >50 pkt/s
✅ **High Attack %**: >60% packets là attack
✅ **Consistent Detection**: Confidence >70%
✅ **Auto-block Triggered**: IP bị block sau 5 attacks
✅ **403 Errors**: MHDDoS nhận 403 Forbidden

#### Metrics để đánh giá:

1. **Detection Rate**: % packets được classify đúng
2. **Time to Block**: Thời gian từ attack đầu tiên đến khi block
3. **False Positive Rate**: % normal traffic bị classify nhầm
4. **System Performance**: CPU/RAM usage, response time

---

## 🎨 Web Interface Guide

### Stats Bar (Top)

| Metric | Ý nghĩa |
|--------|---------|
| Total | Tổng số packets đã capture |
| Normal | Số packets normal |
| Attack | Số packets attack detected |
| Blocked | Số IPs đã bị block |
| Rate | Packets per second |
| Attack % | Phần trăm attack traffic |
| Uptime | Thời gian chạy |

### Packet List

Các cột:
- **No**: Packet number
- **Time**: Timestamp
- **Source**: Source IP
- **Destination**: Destination IP
- **Proto**: Protocol (HTTP, TCP, UDP)
- **Len**: Packet length (bytes)
- **TTL**: Time to Live
- **Threat**: Normal/Attack/🚫 BLOCKED
- **Conf**: Confidence score (%)

### AI Analysis Panel

- **Threat Level**: Badge màu xanh (Normal) hoặc đỏ (Attack)
- **Confidence**: Độ tin cậy của prediction
- **Attack Probability**: Bar chart hiển thị xác suất attack

### Packet Details

Click vào packet để xem:
- Packet number, timestamp
- Source/Destination IPs
- Protocol, length, TTL
- Threat level, confidence
- Attack probability

### Blocked IPs Panel

Hiển thị:
- Danh sách IPs bị block
- Attack count của mỗi IP
- Nút Unblock để gỡ block

---

## 🔧 Configuration

### Thay đổi Detection Threshold

Edit `website/app.py`, dòng ~50:

```python
# Simple detection - lower threshold
is_attack = rate > 3  # Thay đổi số này (requests/second)
confidence = min(0.95, rate / 15)
```

### Thay đổi Block Threshold

Edit `website/app.py`, dòng ~120:

```python
# Block IP if too many attacks (threshold: 5 attacks)
if ip_attack_count[client_ip] >= 5:  # Thay đổi số này
    blocked_ips.add(client_ip)
```

### Thay đổi Analysis Window

Edit `website/app.py`, dòng ~45:

```python
recent = [r for r in requests_log if (now - r['time']) < 5]  # Thay đổi 5 seconds
```

### Thay đổi Buffer Size

Edit `website/app.py`, dòng ~20:

```python
packets = deque(maxlen=500)  # Tăng để lưu nhiều packets hơn
requests_log = deque(maxlen=100)  # Tăng để analyze window lớn hơn
```

---

## 📡 API Documentation

### WebSocket Events

#### Client → Server

**start**
```javascript
socket.emit('start');
```
Bắt đầu monitoring traffic

**stop**
```javascript
socket.emit('stop');
```
Dừng monitoring

**clear**
```javascript
socket.emit('clear');
```
Xóa tất cả packets và reset stats

**unblock_ip**
```javascript
socket.emit('unblock_ip', { ip: '192.168.1.100' });
```
Unblock một IP

**get_blocked_ips**
```javascript
socket.emit('get_blocked_ips');
```
Lấy danh sách IPs bị block

#### Server → Client

**packet**
```javascript
socket.on('packet', (data) => {
    // data = {no, time, src, dst, proto, len, ttl, threat, conf, prob, blocked}
});
```
Packet mới được detect

**stats**
```javascript
socket.on('stats', (data) => {
    // data = {total, normal, attack, blocked, pps, attack_pct, uptime}
});
```
Statistics update

**ip_blocked**
```javascript
socket.on('ip_blocked', (data) => {
    // data = {ip, count, time}
});
```
IP vừa bị block

**ip_unblocked**
```javascript
socket.on('ip_unblocked', (data) => {
    // data = {ip}
});
```
IP vừa được unblock

**blocked_ips**
```javascript
socket.on('blocked_ips', (list) => {
    // list = [{ip, count}, ...]
});
```
Danh sách IPs bị block

### HTTP Endpoints

**GET /**
- Homepage, render web interface

**GET /test**
- Test endpoint để generate traffic
- Returns: 'OK'

---

## 🔬 Chi tiết kỹ thuật

### Machine Learning Pipeline

#### Phase 1: Data Preprocessing
- **Input**: Raw network/MQTT traffic data
- **Processing**:
  - Feature extraction (33 features cho network, 7 cho MQTT)
  - Data cleaning và normalization
  - Label encoding
  - Train/test split (70/30)
- **Output**: Processed datasets, scalers, encoders

#### Phase 2: Model Training
- **Algorithms tested**:
  - Random Forest
  - XGBoost
  - LightGBM
  - Decision Tree
  - Logistic Regression
- **Best performers**:
  - Network: XGBoost (94.2% accuracy)
  - MQTT: LightGBM (96.8% accuracy)

#### Phase 3: Hyperparameter Optimization
- **Method**: Grid Search với Cross-validation
- **Optimized parameters**:
  - Learning rate
  - Max depth
  - Number of estimators
  - Regularization parameters

#### Phase 4: Decision Engine
- **Real-time prediction**
- **Confidence thresholding**
- **Auto-blocking logic**
- **Performance optimization**

### Feature Engineering

#### Network Traffic Features (33 features)

| Category | Features |
|----------|----------|
| Duration | dur |
| Packet counts | spkts, dpkts |
| Byte counts | sbytes, dbytes |
| Rate | rate |
| TTL | sttl, dttl |
| Load | sload, dload |
| Loss | sloss, dloss |
| Inter-packet | sinpkt, dinpkt |
| Jitter | sjit, djit |
| Window | swin, dwin |
| TCP base | stcpb, dtcpb |
| RTT | tcprtt |
| Flags | synack, ackdat |
| Mean | smean, dmean |
| Connection | trans_depth, ct_srv_src, ct_state_ttl, ct_dst_ltm, ct_src_dport_ltm, ct_dst_sport_ltm, ct_dst_src_ltm |
| Response | response_body_len |

#### MQTT Traffic Features (7 features)

| Feature | Description |
|---------|-------------|
| length | Packet length |
| min | Minimum value |
| max | Maximum value |
| mean | Mean value |
| std | Standard deviation |
| var | Variance |
| mad | Median absolute deviation |

### Detection Algorithm

```python
def detect_attack(request_flow):
    # Step 1: Extract features from flow
    features = extract_features(request_flow)
    
    # Step 2: Normalize features
    features_scaled = scaler.transform(features)
    
    # Step 3: ML Prediction
    prediction = model.predict(features_scaled)
    probability = model.predict_proba(features_scaled)
    
    # Step 4: Confidence thresholding
    if max(probability) < 0.7:
        return "Unknown"
    
    # Step 5: Decision
    if prediction == 1:
        return "Attack"
    else:
        return "Normal"
```

### Auto-blocking Logic

```python
def auto_block(ip_address, attack_count):
    BLOCK_THRESHOLD = 5
    
    if attack_count >= BLOCK_THRESHOLD:
        blocked_ips.add(ip_address)
        log_block_event(ip_address, attack_count)
        notify_clients(ip_address)
        return True
    
    return False
```

---

## 🐛 Troubleshooting

### Vấn đề: Không thấy packets

**Nguyên nhân**: Chưa click "Start" hoặc không có traffic

**Giải pháp**:
1. Verify đã click "▶ Start"
2. Check console (F12) có lỗi không
3. Test với: `python test_simple.py`
4. Refresh browser (F5)

### Vấn đề: Model không load

**Nguyên nhân**: Thiếu model files hoặc sai đường dẫn

**Giải pháp**:
1. Check file tồn tại:
   - `Phase3_Network_Models/network_xgboost_optimized.pkl`
   - `Phase3_Models/mqtt_lightgbm_optimized.pkl`
2. Verify đường dẫn relative từ `website/app.py`
3. Re-train models nếu cần

### Vấn đề: Socket.IO connection error

**Nguyên nhân**: Port conflict hoặc firewall

**Giải pháp**:
1. Check port 5000 không bị chiếm:
   ```bash
   netstat -ano | findstr :5000
   ```
2. Thử port khác: Edit `app.py` dòng cuối
3. Tắt firewall tạm thời
4. Refresh browser

### Vấn đề: MHDDoS không chạy

**Nguyên nhân**: Sai cú pháp hoặc thiếu dependencies

**Giải pháp**:
1. Verify cú pháp:
   ```bash
   python start.py <METHOD> <TARGET> <PARAMS>
   ```
2. Check dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Xem log errors trong terminal

### Vấn đề: Không detect attack

**Nguyên nhân**: Threshold quá cao hoặc attack quá nhẹ

**Giải pháp**:
1. Giảm detection threshold (edit app.py)
2. Tăng số threads MHDDoS (50 → 100 → 200)
3. Dùng `test_attack.py` để verify
4. Check model có load không

### Vấn đề: Quá nhiều false positives

**Nguyên nhân**: Threshold quá thấp

**Giải pháp**:
1. Tăng detection threshold
2. Tăng confidence threshold
3. Tăng block threshold (5 → 10)
4. Retrain model với data cụ thể

### Vấn đề: Server bị crash khi attack

**Nguyên nhân**: Attack quá mạnh, hết RAM

**Giải pháp**:
1. Giảm buffer size (500 → 200)
2. Giảm threads MHDDoS
3. Tăng RAM
4. Optimize code

---

## 📈 Performance Optimization

### Tips để tăng performance

1. **Giảm buffer size**: 
   ```python
   packets = deque(maxlen=200)  # Thay vì 500
   ```

2. **Tăng stats update interval**:
   ```python
   if stats['total'] % 20 == 0:  # Thay vì 5
       socketio.emit('stats', get_stats())
   ```

3. **Disable debug mode**:
   ```python
   socketio.run(app, debug=False)  # Production
   ```

4. **Use production WSGI server**:
   ```bash
   pip install gunicorn
   gunicorn -k eventlet -w 1 app:app -b 0.0.0.0:5000
   ```

5. **Optimize ML inference**:
   - Cache predictions
   - Batch processing
   - Use lighter models

---

## 🔐 Security Considerations

### Trong môi trường production

1. **Change SECRET_KEY**:
   ```python
   app.config['SECRET_KEY'] = 'your-secure-random-key'
   ```

2. **Enable HTTPS**:
   ```python
   socketio.run(app, ssl_context=('cert.pem', 'key.pem'))
   ```

3. **Rate limiting**:
   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app, default_limits=["100 per minute"])
   ```

4. **Authentication**:
   - Add login system
   - Protect admin endpoints
   - Use JWT tokens

5. **Logging**:
   - Log all blocks to file
   - Monitor system health
   - Alert on anomalies

### Whitelist IPs

Edit `app.py`:
```python
WHITELIST = {'127.0.0.1', '192.168.1.100'}

@app.before_request
def log_request():
    if request.remote_addr in WHITELIST:
        return  # Skip analysis for whitelisted IPs
```

---

## 📚 Tài liệu tham khảo

### Datasets

📁 **Download Dataset**: [Google Drive](https://drive.google.com/drive/folders/1zh7I1_MBtyS09OQrIpmt1JAqSGuhVfEq?usp=sharing)

Dataset bao gồm:
- UNSW-NB15 Network Traffic Dataset (training + testing)
- MQTT-IoT-IDS2020 Dataset (train70 + test30)
- Preprocessed data (Phase1_Data, Phase1_Network_Data)
- Trained models (Phase2, Phase3 models)

1. **UNSW-NB15**: 
   - Moustafa, N., & Slay, J. (2015). UNSW-NB15: a comprehensive data set for network intrusion detection systems
   - Link: https://research.unsw.edu.au/projects/unsw-nb15-dataset

2. **MQTT-IoT-IDS2020**:
   - IoT MQTT traffic dataset for intrusion detection
   - Link: https://ieee-dataport.org/

### Papers

1. Machine Learning for DDoS Detection
2. Real-time Network Intrusion Detection using ML
3. XGBoost for Network Security
4. LightGBM for IoT Security

### Tools

1. **MHDDoS**: https://github.com/MatrixTM/MHDDoS
2. **Flask-SocketIO**: https://flask-socketio.readthedocs.io/
3. **XGBoost**: https://xgboost.readthedocs.io/
4. **LightGBM**: https://lightgbm.readthedocs.io/

---

## 🤝 Đóng góp

### Cách đóng góp

1. Fork repository
2. Tạo branch mới: `git checkout -b feature/AmazingFeature`
3. Commit changes: `git commit -m 'Add AmazingFeature'`
4. Push to branch: `git push origin feature/AmazingFeature`
5. Tạo Pull Request

### Ý tưởng cải tiến

- [ ] Thêm Deep Learning models (LSTM, CNN)
- [ ] Support nhiều protocols hơn
- [ ] Dashboard với charts real-time
- [ ] Email/SMS alerts
- [ ] API để integrate với hệ thống khác
- [ ] Docker containerization
- [ ] Distributed deployment
- [ ] Historical data analysis
- [ ] Automatic model retraining

---

## 👥 Team

**AIoTLab - Artificial Intelligence of Things Laboratory**

Khoa Công nghệ Thông tin  
Đại học Đại Nam

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📞 Liên hệ

- **Website**: https://fit.dainam.edu.vn
- **Email**: fit@dainam.edu.vn
- **Lab**: AIoTLab

---

## 🙏 Acknowledgments

- UNSW-NB15 dataset creators
- MQTT-IoT-IDS2020 dataset contributors
- Flask và Flask-SocketIO communities
- XGBoost và LightGBM developers
- Open source community

---

<div align="center">

**Made with ❤️ by AIoTLab**

⭐ Star this repo if you find it useful!

</div>
