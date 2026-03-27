# Hệ thống Phát hiện Tấn công DDoS sử dụng Machine Learning

<div align="center">

<p align="center">
<img src="Images/dnu_logo.png" alt="Logo Đại học Đại Nam" width="200"/>
<img src="Images/aiotlab_logo.png" alt="Logo AIoTLab" width="170"/>
</p>

[![AIoTLab](https://img.shields.io/badge/Made%20by%20AIoTLab-blue?style=for-the-badge)](https://fit.dainam.edu.vn)
[![FIT](https://img.shields.io/badge/Faculty%20of%20IT-green?style=for-the-badge)](https://fit.dainam.edu.vn)
[![DNU](https://img.shields.io/badge/DaiNam%20University-red?style=for-the-badge)](https://dainam.edu.vn)

**Phát hiện DDoS real-time trên MQTT và Network traffic sử dụng Machine Learning**

[Dataset](https://drive.google.com/drive/folders/1zh7I1_MBtyS09OQrIpmt1JAqSGuhVfEq?usp=sharing) •
[Cài đặt](#cài-đặt) •
[Chạy Web App](#chạy-web-app) •
[Testing](#testing)

</div>

---

## Tổng quan

Hệ thống phát hiện và ngăn chặn tấn công DDoS real-time gồm 4 giai đoạn nghiên cứu:

| Giai đoạn | Mô tả |
|-----------|-------|
| Phase 1 | Tiền xử lý dữ liệu (Preprocessing) |
| Phase 2 | Huấn luyện và so sánh 4 thuật toán ML |
| Phase 3 | Tối ưu hóa hyperparameter (RandomizedSearchCV) |
| Phase 4 | Decision Engine với Probability Calibration |

**Kết quả cuối cùng (Phase 4):**

| Dataset | Model | Accuracy | F1-Score |
|---------|-------|----------|----------|
| MQTT-IoT-IDS2020 | LightGBM + Decision Engine | 93.12% | **93.06%** |
| UNSW-NB15 (Network) | XGBoost + Decision Engine | 95.26% | **95.23%** |

---

## Datasets

**Download**: [Google Drive](https://drive.google.com/drive/folders/1zh7I1_MBtyS09OQrIpmt1JAqSGuhVfEq?usp=sharing)

| Dataset | Samples | Features | Classes |
|---------|---------|----------|---------|
| MQTT-IoT-IDS2020 | 330,936 (Train: 231,646 / Test: 99,290) | 34 | 6 (legitimate, dos, bruteforce, malformed, slowite, flood) |
| UNSW-NB15 | 257,673 (Train: 82,332 / Test: 175,341) | 42 | 2 (Normal / Attack) |

---

## Cài đặt

### Yêu cầu
- Python 3.8+
- 8GB RAM minimum

### Clone & cài dependencies

```bash
git clone <repository-url>
cd <project-folder>

pip install jupyter pandas numpy scikit-learn xgboost lightgbm \
            imbalanced-learn matplotlib seaborn flask flask-socketio
```

### Download dataset

Download từ [Google Drive](https://drive.google.com/drive/folders/1zh7I1_MBtyS09OQrIpmt1JAqSGuhVfEq?usp=sharing) và đặt vào:
- `MQTT/` — MQTT-IoT-IDS2020
- `Network/` — UNSW-NB15

---

## Training Pipeline

Chạy theo thứ tự từ Phase 1 đến Phase 4:

```bash
# Phase 1: Preprocessing
jupyter notebook Phase1_MQTT_Preprocessing.ipynb
jupyter notebook Phase1_Network_Preprocessing.ipynb

# Phase 2: Model Training & Comparison
jupyter notebook Phase2_MQTT_Model_Training.ipynb
jupyter notebook Phase2_Network_Model_Training.ipynb

# Phase 3: Hyperparameter Optimization
jupyter notebook Phase3_MQTT_Model_Optimization.ipynb
jupyter notebook Phase3_Network_Model_Optimization.ipynb

# Phase 4: Decision Engine
jupyter notebook Phase4_MQTT_Decision_Engine.ipynb
jupyter notebook Phase4_Network_Decision_Engine.ipynb
```

### Chi tiết từng Phase

**Phase 1 — Preprocessing**
- MQTT: Label Encoding, Feature Encoding, StandardScaler → `Phase1_Data/`, `Phase1_Models/`
- Network: Loại bỏ cột không cần (id, attack_cat), Encoding, Scaling → `Phase1_Network_Data/`, `Phase1_Network_Models/`

**Phase 2 — Model Training**
- So sánh 4 thuật toán: Decision Tree, Random Forest, LightGBM, XGBoost
- MQTT best: **LightGBM** (F1 = 0.9126, Time = 6.88s)
- Network best: **XGBoost** (F1 = 0.9028, Time = 3.22s)

**Phase 3 — Optimization**
- RandomizedSearchCV với StratifiedKFold (2-fold, 6 iterations)
- MQTT: F1 = 0.9126 (không cải thiện — default params đã tốt)
- Network: F1 = 0.9017 (giảm nhẹ — dấu hiệu overfitting)

**Phase 4 — Decision Engine**
- MQTT: Probability Calibration (CalibratedClassifierCV, isotonic) + Smart Decision Logic → F1 = **0.9306** (+1.97%)
- Network: ROC-based Threshold Optimization (optimal = 0.1064) + Calibration → F1 = **0.9523** (+5.48%)

---

## Chạy Web App

### 1. Cài dependencies

```bash
cd website
pip install -r requirements.txt
```

### 2. Chạy server

```bash
python app.py
```

### 3. Truy cập

Mở trình duyệt: **http://localhost:5000** → Click **▶ Start**

---

## Testing

```bash
# Test cơ bản (20 requests)
cd website
python test_simple.py

# Simulate DDoS attack (500 requests, 10 threads)
python test_attack.py
```

**Kết quả mong đợi với test_attack.py:**
- Packets màu đỏ xuất hiện liên tục
- Threat Level hiển thị HIGH / CRITICAL
- IP bị block tự động sau 5 attacks
- Alert: "IP BLOCKED: 127.0.0.1"

---

## Tính năng Web App

- **Real-time monitoring** — Hiển thị packets dạng bảng như Wireshark
- **Threat Level** — NORMAL / LOW / MEDIUM / HIGH / CRITICAL theo confidence và request rate
- **AI Analysis Panel** — Confidence score, attack probability, threat badge
- **Auto-blocking** — Tự động block IP sau 5 attacks, unblock qua UI
- **Export** — Xuất dữ liệu capture ra JSON

---


## Troubleshooting

| Vấn đề | Giải pháp |
|--------|-----------|
| Không thấy packets | Click "▶ Start", sau đó chạy test script |
| Model không load | Download models từ Google Drive |
| Socket.IO lỗi | Refresh trình duyệt (F5) |
| `ModuleNotFoundError` | Chạy lại `pip install -r requirements.txt` |

---

## Tài liệu tham khảo

- **UNSW-NB15 Dataset**: https://research.unsw.edu.au/projects/unsw-nb15-dataset
- **XGBoost**: https://xgboost.readthedocs.io/
- **LightGBM**: https://lightgbm.readthedocs.io/
- **scikit-learn Calibration**: https://scikit-learn.org/stable/modules/calibration.html

---

<div align="center">

**AIoTLab — Khoa Công nghệ Thông tin — Đại học Đại Nam**

</div>
