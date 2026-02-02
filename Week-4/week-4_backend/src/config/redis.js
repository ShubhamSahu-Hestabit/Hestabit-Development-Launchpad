import IORedis from "ioredis";
import config from "./index.js";
import logger from "../utils/logger.js";

const redis = new IORedis(config.redisUrl, {
  maxRetriesPerRequest: null, // 🔴 REQUIRED by BullMQ
  enableReadyCheck: false,
});

redis.on("connect", () => {
  logger.info("Redis connected successfully");
});

redis.on("error", (err) => {
  logger.error(`Redis connection error: ${err.message}`);
});

export default redis;
