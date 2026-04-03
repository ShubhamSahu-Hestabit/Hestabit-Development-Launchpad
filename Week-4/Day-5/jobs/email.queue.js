import { Queue } from "bullmq";
import redis from "../config/redis.js";
import logger from "../utils/logger.js";

// Queue name (must be same for worker later)
const EMAIL_QUEUE_NAME = "email-queue";

// Create queue instance
const emailQueue = new Queue(EMAIL_QUEUE_NAME, {
  connection: redis,
  defaultJobOptions: {
    attempts: 3,               // retry 3 times
    backoff: {
      type: "exponential",
      delay: 5000,             // 5 sec initial delay
    },
    removeOnComplete: true,    // auto cleanup
    removeOnFail: false,       // keep failed jobs for debugging
  },
});

/**
 * Add email job to queue
 * @param {Object} data
 */
export const addEmailJob = async (data) => {
  try {
    await emailQueue.add("send-email", data);
    logger.info("Email job added to queue");
  } catch (err) {
    logger.error(`Failed to add email job: ${err.message}`);
  }
};

export default emailQueue;
