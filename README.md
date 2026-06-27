# Makkawi Smart

> B2B SaaS Platform for MikroTik Router Management via VPN  
> **Atbara Market** — Network Infrastructure

## Overview

Makkawi Smart provides centralized control over MikroTik routers via secure VPN connections. Monitor, configure, and manage your entire network infrastructure from a single dark-themed, high-tech dashboard.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (Python), SQLAlchemy (Async) |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Frontend | Jinja2, Bootstrap 5, Vanilla JS |
| Auth | JWT (HTTP-only cookies) |
| Design | Dark futuristic theme (Starlink-inspired) |

## Project Structure

```
makkawi-smart/
├── main.py                 # FastAPI entry point
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in git)
├── app/
│   ├── __init__.py
│   ├── config.py           # Settings & configuration
│   ├── database.py         # Async SQLAlchemy setup
│   ├── auth.py             # JWT + password utilities
│   ├── schemas.py          # Pydantic schemas
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py         # User model (Admin/Customer)
│   │   └── router.py       # Router model
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py         # Login/Register endpoints
│   │   ├── pages.py        # Landing page
│   │   └── dashboard.py    # Dashboard (protected)
│   ├── templates/
│   │   ├── base.html       # Base template
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── dashboard/
│   │   │   └── index.html
│   │   └── pages/
│   │       └── landing.html
│   └── static/
│       ├── css/style.css   # Dark theme CSS
│       ├── js/main.js      # Client-side JS
│       └── images/
└── migrations/
```

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file (copy from .env.example)
cp .env.example .env

# 3. Run the development server
python main.py
# or
uvicorn main:app --reload --port 8000
```

## Features (Step 1)

- [x] Project foundation & folder structure
- [x] User model (Admin/Customer roles)
- [x] Router model (name, VPN IP, API credentials, status)
- [x] JWT-based authentication (register, login, logout)
- [x] Dark, modern landing page with hero & features
- [x] Contact section
- [x] Admin dashboard layout with sidebar
- [x] Responsive design (mobile-friendly)

## Upcoming Steps

- [ ] MikroTik RouterOS API integration
- [ ] Router CRUD operations
- [ ] Real-time monitoring (WebSocket)
- [ ] PPPoE/Hotspot user management
- [ ] Traffic analytics & bandwidth reports
- [ ] Smart alerts & notifications

## License

Proprietary — Makkawi Smart © 2024
