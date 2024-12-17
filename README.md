# FieldTrax

A comprehensive field engineering tracking software for managing completions and wellbore intervention operations.

## 🎯 Project Overview

FieldTrax is a robust solution designed to streamline field engineering operations by providing comprehensive tools for well data management, geometry tracking, and operational logistics.

### Key Features

- Well data management and geometry visualization
- Rig and drillstring/BHA management
- Fluids tracking and management
- Job-log and purchase order system
- Time distribution and timesheet tracking
- Service ticket management
- Pipe tally tracking
- Comprehensive reporting capabilities

## 🚀 Getting Started

### Prerequisites

- Node.js (v16 or higher)
- Python (v3.8 or higher)
- Mssql Server
- sqlite

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-organization/fieldtrax.git
cd fieldtrax
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## 🏗️ Project Structure

```
fieldtrax/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   └── services/
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── layouts/
│   │   ├── pages/
│   │   └── services/
│   └── package.json
├── docs/
└── README.md
```

## 💻 Development

### Running the Application

1. Start the backend server:
```bash
cd backend
uvicorn app.main:app --reload
```

2. Start the frontend development server:
```bash
cd frontend
npm start
```

### Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Branch Naming Convention

- `feature/*`: New features
- `bugfix/*`: Bug fixes
- `hotfix/*`: Critical fixes for production
- `release/*`: Release preparation
- `docs/*`: Documentation updates

## 🔄 Git Workflow

We follow a modified GitFlow workflow:

1. `main` branch contains production code
2. `develop` branch for ongoing development
3. Feature branches are created from `develop`
4. Release branches are created from `develop`
5. Hotfixes are created from `main`

## 📦 Deployment

### Staging Environment
```bash
npm run deploy:staging
```

### Production Environment
```bash
npm run deploy:prod
```

## 🔒 Security

Please report any security issues to security@fieldtrax.com

## 📄 License

This project is proprietary and confidential.

## 👥 Team

- DevOps Engineer: [Shola Babalola]
