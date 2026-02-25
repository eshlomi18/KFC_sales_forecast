# Build the React/Vite application
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the code and build the project
COPY . .
RUN npm run build

# Serve the application with Nginx
FROM nginx:alpine

# Copy the built files from the previous stage to Nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port 80 inside the container
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]