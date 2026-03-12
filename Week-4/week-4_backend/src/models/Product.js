import mongoose from "mongoose";

const productSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: true,
      trim: true,
    },
    description: {
      type: String,
      trim: true,
    },
    price: {
      type: Number,
      required: true,
      min: 0,
    },
    category: {
      type: String,
      enum: ['electronics', 'clothing', 'food', 'books', 'toys', 'sports', 'home', 'beauty', 'other'],
    },
    stock: {
      type: Number,
      default: 0,
      min: 0,
    },
    tags: [{
      type: String,
    }],
    brand: {
      type: String,
    },
    sku: {
      type: String,
    },
    images: [{
      type: String,
    }],
    status: {
      type: String,
      enum: ["active", "inactive"],
      default: "active",
    },
    ratingCount: {
      type: Number,
      default: 0,
    },
    totalRating: {
      type: Number,
      default: 0,
    },
    deletedAt: {
      type: Date,
      default: null,
    }
  },
  {
    timestamps: true,
    toJSON: { virtuals: true },
  }
);

/* Virtual rating */
productSchema.virtual("rating").get(function () {
  return this.ratingCount === 0
    ? 0
    : this.totalRating / this.ratingCount;
});

/* Compound index */
productSchema.index({ status: 1, createdAt: -1 });

export default mongoose.model("Product", productSchema);