import logger from '../utils/logger.js';

/**
 * Validation middleware factory
 */
const validate = (schema, property = 'body') => {
  return (req, res, next) => {
    const dataToValidate = req[property];

    const { error, value } = schema.validate(dataToValidate, {
      abortEarly: false,
      stripUnknown: true,
      errors: {
        wrap: {
          label: ''
        }
      }
    });

    if (error) {
      const errors = error.details.map(detail => ({
        field: detail.path.join('.'),
        message: detail.message
      }));

      logger.warn('Validation failed', {
        property,
        errors,
        path: req.originalUrl
      });

      return res.status(400).json({
        success: false,
        message: 'Validation failed',
        errors,
        timestamp: new Date().toISOString(),
        path: req.originalUrl
      });
    }

    req[property] = value;

    logger.debug('Validation passed', {
      property,
      path: req.originalUrl
    });

    next();
  };
};

/**
 * Validate multiple properties at once
 */
const validateMultiple = (schemas) => {
  return async (req, res, next) => {
    const errors = [];

    for (const [property, schema] of Object.entries(schemas)) {
      const { error, value } = schema.validate(req[property], {
        abortEarly: false,
        stripUnknown: true,
        errors: {
          wrap: {
            label: ''
          }
        }
      });

      if (error) {
        error.details.forEach(detail => {
          errors.push({
            property,
            field: detail.path.join('.'),
            message: detail.message
          });
        });
      } else {
        req[property] = value;
      }
    }

    if (errors.length > 0) {
      logger.warn('Multiple validation failed', {
        errors,
        path: req.originalUrl
      });

      return res.status(400).json({
        success: false,
        message: 'Validation failed',
        errors,
        timestamp: new Date().toISOString(),
        path: req.originalUrl
      });
    }

    logger.debug('Multiple validation passed', {
      path: req.originalUrl
    });

    next();
  };
};

export { validate, validateMultiple };