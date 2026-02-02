import { Worker } from "bullmq";
import redis from "../config/redis.js";
import logger from "../utils/logger.js";

const EMAIL_QUEUE_NAME = "email-queue";

// Create worker
const emailWorker = new Worker(
  EMAIL_QUEUE_NAME,
  async (job) => {
    logger.info(`Processing email job: ${job.id}`);

    const { to, subject, message } = job.data;

    // 🔴 Simulate email sending
    await new Promise((resolve) => setTimeout(resolve, 2000));

    logger.info(
      `Email sent successfully to ${to} | Subject: ${subject}`
    );

    return {
      success: true,
    };
  },
  {
    connection: redis,
  }
);

// Worker lifecycle events
emailWorker.on("completed", (job) => {
  logger.info(`Email job completed: ${job.id}`);
});

emailWorker.on("failed", (job, err) => {
  logger.error(
    `Email job failed: ${job?.id} | Reason: ${err.message}`
  );
});

export default emailWorker;
