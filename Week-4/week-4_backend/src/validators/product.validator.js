import Joi from 'joi';

// Product Create Schema
const productCreateSchema = Joi.object({
  name: Joi.string()
    .min(3)
    .max(200)
    .required()
    .messages({
      'string.min': 'Product name must be at least 3 characters',
      'string.max': 'Product name cannot exceed 200 characters',
      'any.required': 'Product name is required'
    }),
  
  description: Joi.string()
    .min(10)
    .max(2000)
    .optional()
    .messages({
      'string.min': 'Description must be at least 10 characters',
      'string.max': 'Description cannot exceed 2000 characters'
    }),
  
  price: Joi.number()
    .positive()
    .precision(2)
    .required()
    .messages({
      'number.positive': 'Price must be a positive number',
      'any.required': 'Price is required'
    }),
  
  category: Joi.string()
    .valid('electronics', 'clothing', 'food', 'books', 'toys', 'sports', 'home', 'beauty', 'other')
    .optional()
    .messages({
      'any.only': 'Invalid category'
    }),
  
  stock: Joi.number()
    .integer()
    .min(0)
    .optional()
    .default(0)
    .messages({
      'number.min': 'Stock cannot be negative'
    }),
  
  tags: Joi.array()
    .items(Joi.string().min(2).max(50))
    .max(10)
    .optional()
    .messages({
      'array.max': 'Maximum 10 tags allowed'
    }),
  
  brand: Joi.string()
    .min(2)
    .max(100)
    .optional(),
  
  sku: Joi.string()
    .alphanum()
    .min(5)
    .max(50)
    .optional(),
  
  images: Joi.array()
    .items(Joi.string().uri())
    .max(5)
    .optional()
    .messages({
      'array.max': 'Maximum 5 images allowed'
    }),
  
  status: Joi.string()
    .valid('active', 'inactive')
    .default('active')
    .optional()
});

// Product Update Schema
const productUpdateSchema = Joi.object({
  name: Joi.string()
    .min(3)
    .max(200)
    .optional(),
  
  description: Joi.string()
    .min(10)
    .max(2000)
    .optional(),
  
  price: Joi.number()
    .positive()
    .precision(2)
    .optional(),
  
  category: Joi.string()
    .valid('electronics', 'clothing', 'food', 'books', 'toys', 'sports', 'home', 'beauty', 'other')
    .optional(),
  
  stock: Joi.number()
    .integer()
    .min(0)
    .optional(),
  
  tags: Joi.array()
    .items(Joi.string().min(2).max(50))
    .max(10)
    .optional(),
  
  brand: Joi.string()
    .min(2)
    .max(100)
    .optional(),
  
  sku: Joi.string()
    .alphanum()
    .min(5)
    .max(50)
    .optional(),
  
  images: Joi.array()
    .items(Joi.string().uri())
    .max(5)
    .optional(),
  
  status: Joi.string()
    .valid('active', 'inactive')
    .optional()
}).min(1);

// Product Query Schema
const productQuerySchema = Joi.object({
  search: Joi.string()
    .max(200)
    .optional(),
  
  minPrice: Joi.number()
    .positive()
    .optional(),
  
  maxPrice: Joi.number()
    .positive()
    .optional()
    .when('minPrice', {
      is: Joi.exist(),
      then: Joi.number().greater(Joi.ref('minPrice'))
        .messages({
          'number.greater': 'maxPrice must be greater than minPrice'
        })
    }),
  
  category: Joi.string()
    .valid('electronics', 'clothing', 'food', 'books', 'toys', 'sports', 'home', 'beauty', 'other')
    .optional(),
  
  tags: Joi.alternatives()
    .try(
      Joi.string(),
      Joi.array().items(Joi.string())
    )
    .optional(),
  
  brand: Joi.string()
    .optional(),
  
  status: Joi.string()
    .valid('active', 'inactive')
    .optional(),
  
  sort: Joi.string()
    .pattern(/^[a-zA-Z]+:(asc|desc)$/)
    .optional()
    .messages({
      'string.pattern.base': 'Sort format must be field:asc or field:desc'
    }),
  
  page: Joi.number()
    .integer()
    .min(1)
    .default(1)
    .optional(),
  
  limit: Joi.number()
    .integer()
    .min(1)
    .max(100)
    .default(10)
    .optional()
    .messages({
      'number.max': 'Limit cannot exceed 100'
    }),
  
  includeDeleted: Joi.boolean()
    .default(false)
    .optional()
});

// Product ID Param Schema
const productIdSchema = Joi.object({
  id: Joi.string()
    .pattern(/^[0-9a-fA-F]{24}$/)
    .required()
    .messages({
      'string.pattern.base': 'Invalid product ID format'
    })
});

export {
  productCreateSchema,
  productUpdateSchema,
  productQuerySchema,
  productIdSchema
};