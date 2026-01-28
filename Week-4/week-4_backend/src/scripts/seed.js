import mongoose from "mongoose";
import config from "../config/index.js";
import User from "../models/User.js";
import Product from "../models/Product.js";

(async () => {
  try {
    await mongoose.connect(config.dbUrl);
    console.log("✅ DB connected");

    const user = await User.create({
      firstName: "ABC",
      lastName: "DEF",
      email: "abc@test.com",
      password: "password123",
    });

    console.log("👤 User created:", user.fullName);

    const product = await Product.create({
      name: "iPhone 17",
      price: 120000,
      ratingCount: 9,
      totalRating: 45,
    });

    console.log("📦 Product created:", product.name);
    console.log("⭐ Product rating (virtual):", product.rating);

  } catch (err) {
    console.error("❌ Seeding failed:", err);
  } finally {
    await mongoose.connection.close();
    process.exit(0);
  }
})();
