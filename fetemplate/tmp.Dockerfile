# Use the official Node.js 16 Alpine image as a base
FROM node:20-alpine

# Set the working directory inside the container to /app
WORKDIR /app

# Add `/app/node_modules/.bin` to the PATH environment variable
ENV PATH /app/node_modules/.bin:$PATH

# Copy package.json and package-lock.json files to the working directory
COPY package.json ./
COPY package-lock.json ./

# Install dependencies in the container
RUN npm install -g npm@10.2.3

# Copy the rest of the application's code to the working directory
COPY . .
RUN chown -R node:node /app
USER node
# Expose port 3000 for the application
EXPOSE 3005

# Run the application using npm start
CMD ["npm", "start"]

