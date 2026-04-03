import productService from "../services/product.service.js";
import logger from "../utils/logger.js";

const getProducts = async (req, res, next) => {
  try {
    logger.info({
      message: "Fetching products",
      requestId: req.requestId,
      query: req.query
    });

    const result = await productService.getProducts(req.query);
    
    logger.info({
      message: "Products fetched successfully",
      requestId: req.requestId,
      count: result.data?.length || 0
    });

    res.status(200).json({ success: true, data: result });
  } catch (err) {
    logger.error({
      message: "Error fetching products",
      requestId: req.requestId,
      error: err.message
    });
    next(err);
  }
};

const getById = async (req, res, next) => {
  try {
    logger.info({
      message: "Fetching product by ID",
      requestId: req.requestId,
      productId: req.params.id
    });

    const product = await productService.getById(req.params.id);
    
    logger.info({
      message: "Product fetched successfully",
      requestId: req.requestId,
      productId: req.params.id
    });

    res.status(200).json({ success: true, data: product });
  } catch (err) {
    logger.error({
      message: "Error fetching product",
      requestId: req.requestId,
      productId: req.params.id,
      error: err.message
    });
    next(err);
  }
};

const create = async (req, res, next) => {
  try {
    logger.info({
      message: "Creating product",
      requestId: req.requestId,
      body: req.body
    });

    const product = await productService.create(req.body);
    
    logger.info({
      message: "Product created successfully",
      requestId: req.requestId,
      productId: product._id
    });

    res.status(201).json({ success: true, data: product });
  } catch (err) {
    logger.error({
      message: "Error creating product",
      requestId: req.requestId,
      error: err.message
    });
    next(err);
  }
};

const update = async (req, res, next) => {
  try {
    logger.info({
      message: "Updating product",
      requestId: req.requestId,
      productId: req.params.id,
      updates: req.body
    });

    const product = await productService.update(req.params.id, req.body);
    
    logger.info({
      message: "Product updated successfully",
      requestId: req.requestId,
      productId: req.params.id
    });

    res.status(200).json({ success: true, data: product });
  } catch (err) {
    logger.error({
      message: "Error updating product",
      requestId: req.requestId,
      productId: req.params.id,
      error: err.message
    });
    next(err);
  }
};

const remove = async (req, res, next) => {
  try {
    logger.info({
      message: "Soft deleting product",
      requestId: req.requestId,
      productId: req.params.id
    });

    await productService.softDelete(req.params.id);
    
    logger.info({
      message: "Product deleted successfully",
      requestId: req.requestId,
      productId: req.params.id
    });

    res.status(200).json({
      success: true,
      message: "Product deleted successfully"
    });
  } catch (err) {
    logger.error({
      message: "Error deleting product",
      requestId: req.requestId,
      productId: req.params.id,
      error: err.message
    });
    next(err);
  }
};

export default {
  getProducts,
  getById,
  create,
  update,
  remove
};