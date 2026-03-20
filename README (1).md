# 🏠 MLOps House Price Predictor

[![CI/CD](https://github.com/workgarimaswami/mlops-house-price/actions/workflows/deploy.yml/badge.svg)](https://github.com/workgarimaswami/mlops-house-price/actions)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![AWS](https://img.shields.io/badge/AWS-Elastic%20Beanstalk-FF9900?logo=amazonaws&logoColor=white)](https://aws.amazon.com/elasticbeanstalk/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Production-ready ML application** that predicts house prices — deployed on AWS with an 80% reduction in deployment time through full CI/CD automation.

🌐 **Live Demo:** [house-price-env.eba-g63resv2.eu-north-1.elasticbeanstalk.com](http://house-price-env.eba-g63resv2.eu-north-1.elasticbeanstalk.com)

---

## 📌 Overview

This project demonstrates an **end-to-end MLOps pipeline** — from raw data ingestion and model training to containerized API deployment and real-time monitoring on AWS. It serves as a blueprint for productionizing machine learning models with modern DevOps practices.

### Key Highlights

- 🚀 **80% faster deployments** via automated CI/CD with GitHub Actions
- 🐳 **Dockerized** application for consistent, reproducible environments
- ☁️ **AWS-native** infrastructure using Elastic Beanstalk, EC2, S3, IAM & CloudWatch
- 📊 **Model monitoring** with drift detection and performance tracking
- ✅ **Automated testing** suite covering unit and integration tests

---

## 🏗️ Architecture

```
Data Ingestion → Feature Engineering → Model Training → Model Registry (S3)
                                                                  ↓
User Request → Frontend → REST API (Flask/FastAPI) → Prediction ← Loaded Model
                                                         ↓
                                               CloudWatch Monitoring
```

### Full Pipeline: `Data → Model → API → Deployment`

```
GitHub Push
    │
    ▼
GitHub Actions CI/CD
    │
    ├── Run Tests (pytest)
    ├── Build Docker Image
    ├── Push to ECR / S3
    └── Deploy to AWS Elastic Beanstalk
                │
                ▼
         Live Endpoint 🌐
```

---

## 📁 Project Structure

```
mlops-house-price/
│
├── .ebextensions/          # AWS Elastic Beanstalk configuration files
├── frontend/               # Web UI for interacting with the prediction API
├── model/                  # Trained model artifacts and serialization
├── monitoring/             # Model performance & data drift monitoring scripts
├── src/                    # Core source code
│   ├── data/               #   Data ingestion & preprocessing
│   ├── features/           #   Feature engineering pipeline
│   ├── train/              #   Model training & evaluation
│   └── api/                #   REST API (prediction endpoint)
├── tests/                  # Unit & integration tests
│
├── Dockerfile              # Docker image definition
├── .dockerignore           # Docker build exclusions
├── .gitignore
└── README.md
```

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| **ML / Data** | Python, Scikit-learn, Pandas, NumPy |
| **API** | Flask / FastAPI |
| **Containerization** | Docker |
| **CI/CD** | GitHub Actions |
| **Cloud** | AWS Elastic Beanstalk, EC2, S3, IAM |
| **Monitoring** | AWS CloudWatch |
| **Testing** | pytest |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Docker
- AWS CLI (for cloud deployment)

### 1. Clone the Repository

```bash
git clone https://github.com/workgarimaswami/mlops-house-price.git
cd mlops-house-price
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Train the Model

```bash
python src/train/train.py
```

### 4. Run Locally

```bash
python src/api/app.py
```

The API will be available at `http://localhost:5000`.

### 5. Run with Docker

```bash
# Build the image
docker build -t mlops-house-price .

# Run the container
docker run -p 5000:5000 mlops-house-price
```

---

## 🔌 API Usage

### Predict House Price

**POST** `/predict`

```json
{
  "bedrooms": 3,
  "bathrooms": 2,
  "sqft_living": 1800,
  "sqft_lot": 5000,
  "floors": 1,
  "waterfront": 0,
  "condition": 3,
  "grade": 7,
  "yr_built": 1990,
  "zipcode": 98001
}
```

**Response:**

```json
{
  "predicted_price": 425000.00,
  "confidence_interval": [390000, 460000]
}
```

---

## ☁️ AWS Deployment

This project is deployed on **AWS Elastic Beanstalk** with the following services:

| Service | Usage |
|---|---|
| **Elastic Beanstalk** | Application hosting & auto-scaling |
| **EC2** | Underlying compute instances |
| **S3** | Model artifact storage |
| **IAM** | Role-based access control |
| **CloudWatch** | Logs, metrics & alerts |

### Deploy to AWS

```bash
# Install EB CLI
pip install awsebcli

# Initialize Elastic Beanstalk app
eb init -p docker mlops-house-price

# Create environment & deploy
eb create house-price-env
eb deploy
```

---

## 🔄 CI/CD Pipeline

On every push to `main`, GitHub Actions automatically:

1. ✅ Runs the test suite (`pytest tests/`)
2. 🐳 Builds the Docker image
3. 📦 Packages the application
4. 🚀 Deploys to AWS Elastic Beanstalk

See `.github/workflows/deploy.yml` for the full pipeline definition.

---

## 📊 Monitoring

The `monitoring/` module tracks:

- **Prediction drift** — detects shifts in model output distribution
- **Data drift** — monitors changes in input feature distributions
- **Latency & error rates** — via AWS CloudWatch dashboards
- **Model performance** — periodic re-evaluation against new data

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

---

## 📈 Results

| Metric | Value |
|---|---|
| Model | Gradient Boosting / XGBoost |
| RMSE | ~$28,000 |
| R² Score | ~0.88 |
| Deployment Time Reduction | **80%** |
| API Response Time | < 200ms |

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 👩‍💻 Author

**Garima Swami**
- GitHub: [@workgarimaswami](https://github.com/workgarimaswami)

---

⭐ *If you found this project useful, please give it a star!*
