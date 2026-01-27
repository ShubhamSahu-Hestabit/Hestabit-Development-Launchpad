import express from "express";
import logger from "../utils/logger.js";

export default async function appLoader() {
  const app = express();

  app.use(express.json());
  logger.info("Middlewares loaded");

  app.get("/health", (_, res) => res.send("OK"));

  logger.info("Routes mounted: 1 endpoints");

  return app;
}
