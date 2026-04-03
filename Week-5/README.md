
## Folder Structure

```text
Week-5/
│
├── Day-1/
│   ├── images/
│   ├── app.js
│   ├── Dockerfile
│   ├── linux-in-container.md
│   └── package.json
│
├── Day-2/
│   ├── client/
│   │   ├── public/
│   │   ├── src/
│   │   ├── Dockerfile
│   │   ├── package.json
│   │   └── package-lock.json
│   │
│   ├── server/
│   │   ├── node_modules/
│   │   ├── Dockerfile
│   │   ├── index.js
│   │   ├── package.json
│   │   └── package-lock.json
│   │
│   ├── screenshots/
│   ├── docker-compose.yml
│   └── service-architecture.md
│
├── Day-3/
│   ├── backend/
│   │   ├── node_modules/
│   │   ├── Dockerfile
│   │   ├── index.js
│   │   ├── package.json
│   │   └── package-lock.json
│   │
│   ├── nginx/
│   │   └── nginx.conf
│   │
│   ├── screenshots/
│   ├── docker-compose.yml
│   └── reverse-proxy-readme.md
│
├── Day-4/
│   ├── certs/
│   │   ├── myapp.local-key.pem
│   │   └── myapp.local.pem
│   │
│   ├── nginx/
│   │   ├── nginx.conf
│   │   └── ssl/
│   │       ├── server.crt
│   │       └── server.key
│   │
│   ├── screenshots/
│   ├── docker-compose.yml
│   └── ssl-setup.md
│
├── Day-5/
│   ├── apps/
│   │   ├── backend/
│   │   │   ├── Dockerfile
│   │   │   ├── index.js
│   │   │   └── package.json
│   │   │
│   │   └── frontend/
│   │       ├── Dockerfile
│   │       └── index.html
│   │
│   ├── nginx/
│   │   ├── ssl/
│   │   │   ├── myapp.local-key.pem
│   │   │   └── myapp.local.pem
│   │   └── default.conf
│   │
│   ├── scripts/
│   │   └── deploy.sh
│   │
│   ├── screenshots/
│   ├── .env
│   ├── docker-compose.prod.yml
│   ├── Demo_video.webm
│   └── production-guide.md
│
└── README.md
```

## Overview

- Docker basics to production deployment
- Full stack (frontend + backend)
- Reverse proxy using Nginx
- SSL setup (HTTPS)
- Production-ready deployment

## Notes

- Follows Week-wise → Day-wise structure
- Each day contains code + configs + docs
- Clear progression from basics → production
