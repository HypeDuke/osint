FROM node:20-alpine

WORKDIR /app

# Copy package.json and install dependencies
COPY package.json ./
RUN npm install

# Copy rest of the app
COPY . .

# Build Tailwind + Vite app
RUN npm run build

# Serve with a simple static server (optional for dev, you can skip in compose if using dev server)
RUN npm install -g serve

# Expose Vite dev port
EXPOSE 5173

CMD ["serve", "-s", "dist", "-l", "5173"]