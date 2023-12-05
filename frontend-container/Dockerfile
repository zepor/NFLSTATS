# Stage 1: Build the application
FROM node:16-alpine as build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Stage 2: Set up the Express server to serve the build directory
FROM node:16-alpine
WORKDIR /app
COPY --from=build /app/dist ./dist
# If you have an Express server file at the root of your project, copy it here
COPY server.js ./
# Install Express
RUN npm install express
EXPOSE 3000
CMD ["node", "server.js"]