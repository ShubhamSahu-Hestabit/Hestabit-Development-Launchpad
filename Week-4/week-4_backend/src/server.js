import config from "./config/index.js";
import logger from "./utils/logger.js";
import appLoader from "./loaders/app.js";
import dbLoader from "./loaders/db.js";

// 🔴 START BACKGROUND WORKERS (DEV MODE)
import "./jobs/email.worker.js";

async function startServer() {
  await dbLoader();
  const app = await appLoader();

  app.listen(config.port, () => {
    logger.info(`Server started on port ${config.port}`);
  });
}

startServer();
