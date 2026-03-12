import express from "express";
import productRoutes from "./product.routes.js";

const router = express.Router();

// health route (API level)
router.get("/health", (req, res) => {
  res.status(200).json({ status: "OK" });
});

// product routes
router.use("/products", productRoutes);

export default router;
