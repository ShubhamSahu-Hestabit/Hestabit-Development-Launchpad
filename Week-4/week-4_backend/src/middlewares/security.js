import helmet from 'helmet';
import cors from 'cors';
import rateLimit from 'express-rate-limit';
import mongoSanitize from 'express-mongo-sanitize';
import xss from 'xss-clean';
import hpp from 'hpp';
import express from 'express';
import logger from '../utils/logger.js';

/**
 * Helmet Configuration
 */
const helmetConfig = helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", 'data:', 'https:'],
    },
  },
  crossOriginEmbedderPolicy: false,
  crossOriginResourcePolicy: { policy: 'cross-origin' },
});

/**
 * CORS Configuration
 */
const corsOptions = {
  origin: function (origin, callback) {
    const allowedOrigins = [
      'http://localhost:3000',
      'http://localhost:3001',
      'http://localhost:5173',
      'http://localhost:5174',
    ];

    if (!origin) return callback(null, true);

    if (allowedOrigins.indexOf(origin) !== -1 || process.env.NODE_ENV === 'development') {
      callback(null, true);
    } else {
      logger.warn('CORS blocked request from origin', { origin });
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true,
  optionsSuccessStatus: 200,
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Request-ID'],
  exposedHeaders: ['X-Request-ID', 'X-RateLimit-Limit', 'X-RateLimit-Remaining'],
  maxAge: 86400,
};

/**
 * Global Rate Limiter
 */
const globalRateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  message: {
    success: false,
    message: 'Too many requests from this IP, please try again later.',
    retryAfter: '15 minutes'
  },
  standardHeaders: true,
  legacyHeaders: false,
  handler: (req, res) => {
    logger.warn('Rate limit exceeded', {
      ip: req.ip,
      path: req.path
    });
    res.status(429).json({
      success: false,
      message: 'Too many requests from this IP, please try again later.',
      retryAfter: '15 minutes',
      timestamp: new Date().toISOString(),
      path: req.originalUrl
    });
  },
  skip: (req) => {
    return req.path === '/health' || req.path === '/api/health';
  }
});

/**
 * Auth Rate Limiter
 */
const authRateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  message: {
    success: false,
    message: 'Too many authentication attempts, please try again later.',
    retryAfter: '15 minutes'
  },
  skipSuccessfulRequests: true,
  handler: (req, res) => {
    logger.warn('Auth rate limit exceeded', {
      ip: req.ip,
      path: req.path
    });
    res.status(429).json({
      success: false,
      message: 'Too many authentication attempts, please try again later.',
      retryAfter: '15 minutes',
      timestamp: new Date().toISOString(),
      path: req.originalUrl
    });
  }
});

/**
 * API Rate Limiter
 */
const apiRateLimiter = rateLimit({
  windowMs: 1 * 60 * 1000,
  max: 30,
  message: {
    success: false,
    message: 'Too many API requests, please try again later.',
    retryAfter: '1 minute'
  },
  standardHeaders: true,
  legacyHeaders: false,
});

/**
 * NoSQL Injection Protection
 */
const noSqlInjectionProtection = mongoSanitize({
  replaceWith: '_',
  onSanitize: ({ req, key }) => {
    logger.warn('Potential NoSQL injection attempt detected', {
      ip: req.ip,
      key
    });
  }
});

/**
 * XSS Protection
 */
const xssProtection = xss();

/**
 * HPP Protection
 */
const hppProtection = hpp({
  whitelist: [
    'tags',
    'categories',
    'sort',
  ]
});

/**
 * Payload Size Limiter
 */
const payloadSizeLimiter = (req, res, next) => {
  const maxSize = 10 * 1024 * 1024; // 10MB
  
  if (req.headers['content-length'] && parseInt(req.headers['content-length']) > maxSize) {
    logger.warn('Payload too large', {
      ip: req.ip,
      size: req.headers['content-length']
    });
    
    return res.status(413).json({
      success: false,
      message: 'Payload too large. Maximum allowed size is 10MB.',
      timestamp: new Date().toISOString(),
      path: req.originalUrl
    });
  }
  
  next();
};

/**
 * Security Headers Middleware
 */
const securityHeaders = (req, res, next) => {
  res.removeHeader('X-Powered-By');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  next();
};

/**
 * Apply all security middleware
 */
const applySecurity = (app) => {
  logger.info('Loading security middleware...');

  app.use(helmetConfig);
  app.use(securityHeaders);
  app.use(cors(corsOptions));
  app.use(globalRateLimiter);
  
  // Body parsers with size limits
  app.use(express.json({ limit: '10mb' }));
  app.use(express.urlencoded({ extended: true, limit: '10mb' }));
  
  app.use(payloadSizeLimiter);
  app.use(noSqlInjectionProtection);
  app.use(xssProtection);
  app.use(hppProtection);

  logger.info('✔ Security middleware loaded successfully');
};

export {
  applySecurity,
  helmetConfig,
  corsOptions,
  globalRateLimiter,
  authRateLimiter,
  apiRateLimiter,
  noSqlInjectionProtection,
  xssProtection,
  hppProtection,
  payloadSizeLimiter,
  securityHeaders
};