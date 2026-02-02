import productRepository from "../repositories/product.repository.js";
import ApiError from "../utils/apiError.js";
import { addEmailJob } from "../jobs/email.queue.js";

const getProducts = async (query) => {
  const {
    search,
    minPrice,
    maxPrice,
    tags,
    sort,
    page = 1,
    limit = 10,
    includeDeleted
  } = query;

  // ------------------
  // FILTERS
  // ------------------
  const filters = {};

  if (!includeDeleted) {
    filters.deletedAt = null;
  }

  if (search) {
    filters.$or = [
      { name: { $regex: search, $options: "i" } },
      { description: { $regex: search, $options: "i" } }
    ];
  }

  if (minPrice || maxPrice) {
    filters.price = {};
    if (minPrice) filters.price.$gte = Number(minPrice);
    if (maxPrice) filters.price.$lte = Number(maxPrice);
  }

  if (tags) {
    filters.tags = { $in: tags.split(",") };
  }

  // ------------------
  // SORTING
  // ------------------
  let sortObj = { createdAt: -1 };

  if (sort) {
    const [field, order] = sort.split(":");
    sortObj = { [field]: order === "desc" ? -1 : 1 };
  }

  // ------------------
  // PAGINATION
  // ------------------
  const skip = (page - 1) * limit;

  return productRepository.findAll({
    filters,
    sort: sortObj,
    skip,
    limit: Number(limit)
  });
};

const getById = async (id) => {
  const product = await productRepository.findById(id);

  if (!product || product.deletedAt) {
    throw new ApiError("Product not found", "PRODUCT_NOT_FOUND", 404);
  }

  return product;
};

const create = async (data) => {
  const product = await productRepository.create(data);

  // 🔴 ASYNC BACKGROUND JOB (NON-BLOCKING)
  await addEmailJob({
    to: "admin@example.com",
    subject: "New Product Created",
    message: `Product "${product.name}" was created successfully`,
  });

  return product;
};

const update = async (id, data) => {
  const updated = await productRepository.update(id, data);

  if (!updated) {
    throw new ApiError("Product not found", "PRODUCT_NOT_FOUND", 404);
  }

  return updated;
};

const softDelete = async (id) => {
  const deleted = await productRepository.softDelete(id);

  if (!deleted) {
    throw new ApiError("Product not found", "PRODUCT_NOT_FOUND", 404);
  }

  return deleted;
};

export default {
  getProducts,
  getById,
  create,
  update,
  softDelete
};
