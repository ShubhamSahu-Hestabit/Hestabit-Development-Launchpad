import express from "express";
import logger from "../utils/logger.js";
import routes from "../routes/index.js";

export default async function appLoader() {
  const app = express();

  // middlewares
  app.use(express.json());
  logger.info("Middlewares loaded");

  // routes
  app.use("/api", routes);

  logger.info("Routes mounted: API routes");

  return app;
}
