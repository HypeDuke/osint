# Base image
FROM node:20-alpine

# Create app directory
WORKDIR /app

# Install dependencies
#COPY package.json package-lock.json ./
COPY package.json ./
RUN npm install

# Copy source code
COPY . .

# Expose Vite dev server port
EXPOSE 5173

# Start app
CMD ["npm", "run", "dev"]
