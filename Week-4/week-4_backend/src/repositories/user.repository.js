import User from "../models/User.js";

class UserRepository {
  async create(data) {
    return User.create(data);
  }

  async findById(id) {
    return User.findById(id);
  }

  async findPaginated({ page = 1, limit = 10 }) {
    const skip = (page - 1) * limit;

    const data = await User.find()
      .skip(skip)
      .limit(limit)
      .sort({ createdAt: -1 });

    const total = await User.countDocuments();

    return { total, page, limit, data };
  }

  async update(id, data) {
    return User.findByIdAndUpdate(id, data, { new: true });
  }

  async delete(id) {
    return User.findByIdAndDelete(id);
  }
}

export default new UserRepository();
