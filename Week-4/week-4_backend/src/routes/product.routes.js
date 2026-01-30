import express from "express";
import productController from "../controllers/product.controller.js";
import { validate } from "../middlewares/validate.js";
import { apiRateLimiter } from "../middlewares/security.js";
import {
  productCreateSchema,
  productUpdateSchema,
  productQuerySchema,
  productIdSchema
} from "../validators/product.validator.js";

const router = express.Router();

router.get(
  "/",
  apiRateLimiter,
  validate(productQuerySchema, 'query'),
  productController.getProducts
);

router.get(
  "/:id",
  validate(productIdSchema, 'params'),
  productController.getById
);

router.post(
  "/",
  validate(productCreateSchema, 'body'),
  productController.create
);

router.put(
  "/:id",
  validate(productIdSchema, 'params'),
  validate(productUpdateSchema, 'body'),
  productController.update
);

router.delete(
  "/:id",
  validate(productIdSchema, 'params'),
  productController.remove
);

export default router;