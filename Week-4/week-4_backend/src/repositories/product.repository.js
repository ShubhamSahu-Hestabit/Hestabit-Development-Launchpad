import Product from "../models/Product.js";

class ProductRepository {
  async create(data) {
    return Product.create(data);
  }

  async findById(id) {
    return Product.findById(id);
  }

  async findPaginated({ page = 1, limit = 10 }) {
    const skip = (page - 1) * limit;

    const data = await Product.find()
      .skip(skip)
      .limit(limit)
      .sort({ createdAt: -1 });

    const total = await Product.countDocuments();

    return { total, page, limit, data };
  }

  async update(id, data) {
    return Product.findByIdAndUpdate(id, data, { new: true });
  }

  async delete(id) {
    return Product.findByIdAndDelete(id);
  }
}

export default new ProductRepository();
