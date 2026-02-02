import dotenv from "dotenv";

const env = process.env.NODE_ENV || "local";

dotenv.config({ path: `.env.${env}` });

export default {
  env,
  port: process.env.PORT,
  dbUrl: process.env.DB_URL,
  redisUrl: process.env.REDIS_URL,
};
