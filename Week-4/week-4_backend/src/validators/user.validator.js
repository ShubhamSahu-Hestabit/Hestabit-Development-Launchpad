import Joi from 'joi';

// User Registration Schema
const userRegistrationSchema = Joi.object({
  firstName: Joi.string()
    .min(2)
    .max(50)
    .required()
    .messages({
      'string.min': 'First name must be at least 2 characters',
      'string.max': 'First name cannot exceed 50 characters',
      'any.required': 'First name is required'
    }),
  
  lastName: Joi.string()
    .min(2)
    .max(50)
    .optional()
    .allow(''),
  
  email: Joi.string()
    .email()
    .required()
    .lowercase()
    .messages({
      'string.email': 'Please provide a valid email address',
      'any.required': 'Email is required'
    }),
  
  password: Joi.string()
    .min(8)
    .max(128)
    .pattern(new RegExp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]'))
    .required()
    .messages({
      'string.min': 'Password must be at least 8 characters long',
      'string.pattern.base': 'Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character',
      'any.required': 'Password is required'
    }),
  
  phone: Joi.string()
    .pattern(/^[0-9]{10}$/)
    .optional()
    .messages({
      'string.pattern.base': 'Phone number must be 10 digits'
    }),
  
  age: Joi.number()
    .integer()
    .min(13)
    .max(120)
    .optional()
    .messages({
      'number.min': 'Age must be at least 13',
      'number.max': 'Age cannot exceed 120'
    })
});

// User Login Schema
const userLoginSchema = Joi.object({
  email: Joi.string()
    .email()
    .required()
    .lowercase()
    .messages({
      'string.email': 'Please provide a valid email address',
      'any.required': 'Email is required'
    }),
  
  password: Joi.string()
    .required()
    .messages({
      'any.required': 'Password is required'
    })
});

// User Update Schema
const userUpdateSchema = Joi.object({
  firstName: Joi.string()
    .min(2)
    .max(50)
    .optional(),
  
  lastName: Joi.string()
    .min(2)
    .max(50)
    .optional(),
  
  phone: Joi.string()
    .pattern(/^[0-9]{10}$/)
    .optional(),
  
  age: Joi.number()
    .integer()
    .min(13)
    .max(120)
    .optional()
}).min(1);

// User ID Param Schema
const userIdSchema = Joi.object({
  id: Joi.string()
    .pattern(/^[0-9a-fA-F]{24}$/)
    .required()
    .messages({
      'string.pattern.base': 'Invalid user ID format'
    })
});

export {
  userRegistrationSchema,
  userLoginSchema,
  userUpdateSchema,
  userIdSchema
};