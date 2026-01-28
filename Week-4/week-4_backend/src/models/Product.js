import mongoose from "mongoose";

const productSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: true,
      trim: true,
    },
    price: {
      type: Number,
      required: true,
      min: 0,
    },
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
  },
  {
    timestamps: true,
    toJSON: { virtuals: true },
  }
);

/* 🔹 Virtual rating */
productSchema.virtual("rating").get(function () {
  return this.ratingCount === 0
    ? 0
    : this.totalRating / this.ratingCount;
});

/* 🔹 Compound index (Day-2 requirement) */
productSchema.index({ status: 1, createdAt: -1 });

export default mongoose.model("Product", productSchema);
