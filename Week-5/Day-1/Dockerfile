# Use official Node.js image as base
FROM node:18-alpine

# Set working directory inside container
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies (if any)
RUN npm install

# Copy application code
COPY . .

# Expose port 3000
EXPOSE 3000

# Command to run the app
CMD ["node", "app.js"]
