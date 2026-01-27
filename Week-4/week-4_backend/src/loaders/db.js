import logger from "../utils/logger.js";

export default async function dbLoader() {
  try {
    // Simulated DB connection
    await new Promise((resolve) => setTimeout(resolve, 500));
    logger.info("Database connected");
  } catch (error) {
    logger.error("Database connection failed");
    process.exit(1);
  }
}
