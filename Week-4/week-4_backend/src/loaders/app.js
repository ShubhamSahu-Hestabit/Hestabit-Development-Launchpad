import express from "express";
import logger from "../utils/logger.js";
import routes from "../routes/index.js";
import { applySecurity } from "../middlewares/security.js";

export default async function appLoader() {
  const app = express();

  // Apply security middleware FIRST
  applySecurity(app);

  logger.info("Middlewares loaded");

  // routes
  app.use("/api", routes);

  logger.info("Routes mounted: API routes");

  return app;
}