import Product from "../models/Product.js";

class ProductRepository {
  async create(data) {
    return Product.create(data);
  }

  // ❌ DO NOT use this for GET-by-ID
  async findById(id) {
    return Product.findById(id);
  }

  // ✅ USE THIS for GET-by-ID
  async findByIdActive(id) {
    return Product.findOne({
      _id: id,
      deletedAt: null
    });
  }

  async findAll({ filters, sort, skip, limit }) {
    const data = await Product.find(filters)
      .sort(sort)
      .skip(skip)
      .limit(limit);

    const total = await Product.countDocuments(filters);
    return { total, data };
  }

  async update(id, data) {
    return Product.findByIdAndUpdate(id, data, { new: true });
  }

  async softDelete(id) {
    return Product.findByIdAndUpdate(
      id,
      { deletedAt: new Date() },
      { new: true }
    );
  }
}

export default new ProductRepository();
