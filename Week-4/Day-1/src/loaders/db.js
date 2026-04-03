import mongoose from "mongoose";
import config from "../config/index.js";
import logger from "../utils/logger.js";

export default async function dbLoader() {
  try {
    if (!config.dbUrl) {
      throw new Error("DB_URL is missing in environment variables");
    }

    await mongoose.connect(config.dbUrl, {
      serverSelectionTimeoutMS: 5000,
    });

    logger.info("Database connected");
  } catch (error) {
    logger.error("Database connection failed");
    logger.error(error.message);
    process.exit(1);
  }
}
