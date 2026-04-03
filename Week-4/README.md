
## Folder Structure

```text
Week-4/
├── Day-1/
│   ├── screenshot/
│   ├── src/
│   │   ├── loaders/
│   │   │   ├── app.js
│   │   │   └── db.js
│   │   └── utils/
│   │       └── logger.js
│   └── ARCHITECTURE.md
├── Day-2/
│   ├── models/
│   │   ├── Product.js
│   │   └── User.js
│   ├── repositories/
│   │   ├── product.repository.js
│   │   └── user.repository.js
│   ├── screenshot/
│   └── README.md
├── Day-3/
│   ├── controllers/
│   │   └── product.controller.js
│   ├── images/
│   ├── middlewares/
│   │   └── error.middleware.js
│   ├── services/
│   │   └── product.service.js
│   └── QUERY-ENGINE-DOC.md
├── Day-4/
│   ├── middlewares/
│   │   ├── security.js
│   │   └── validate.js
│   ├── screenshots/
│   └── SECURITY-REPORT.md
├── Day-5/
│   ├── jobs/
│   │   ├── email.queue.js
│   │   └── email.worker.js
│   ├── logs/
│   ├── utils/
│   │   └── tracing.js
│   ├── DEPLOYMENT-NOTES.md
│   └── My Collection.postman_collection.json
├── README.md
└── week-4_backend/
    ├── node_modules/
    ├── src/
    │   ├── config/
    │   │   ├── index.js
    │   │   └── redis.js
    │   ├── controllers/
    │   │   └── product.controller.js
    │   ├── jobs/
    │   │   ├── email.queue.js
    │   │   └── email.worker.js
    │   ├── loaders/
    │   │   ├── app.js
    │   │   └── db.js
    │   ├── logs/
    │   │   ├── app.log
    │   │   └── error.log
    │   ├── middlewares/
    │   │   ├── error.middleware.js
    │   │   ├── security.js
    │   │   └── validate.js
    │   ├── models/
    │   │   ├── Product.js
    │   │   └── User.js
    │   ├── repositories/
    │   │   ├── product.repository.js
    │   │   └── user.repository.js
    │   ├── routes/
    │   │   ├── index.js
    │   │   └── product.routes.js
    │   ├── scripts/
    │   │   └── seed.js
    │   ├── services/
    │   │   └── product.service.js
    │   ├── utils/
    │   │   ├── apiError.js
    │   │   ├── logger.js
    │   │   └── tracing.js
    │   └── validators/
    │       ├── product.validator.js
    │       └── user.validator.js
    ├── seed.js
    ├── server.js
    ├── .env.dev
    ├── .env.local
    ├── .env.prod
    ├── package-lock.json
    └── package.json
```

---

## How the Week Was Structured

The structure was intentionally divided into two views:

### 1. Day-wise learning view
This shows what was delivered each day and makes the weekly progression easy to understand.

### 2. Final integrated backend view
The `week-4_backend/` folder contains the consolidated implementation where all backend pieces come together into one proper project structure.

This approach is useful because:

- it documents daily deliverables clearly
- it keeps the final working structure organized
- it shows incremental learning without losing the final architecture
- it is easier for review, presentation, and GitHub documentation

---
