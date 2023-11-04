# Node version should match that of your production environment.
FROM node:20.9.0

# Set the Yarn version.
ENV YARN_VERSION 1.22.19

# Set the work directory for the yarn workspace.
WORKDIR /app

# Copy the root package.json and yarn.lock.
COPY package.json yarn.lock ./

# Set Yarn to the specific version.
RUN yarn policies set-version $YARN_VERSION

# Install all workspace dependencies.
RUN yarn install --frozen-lockfile

# Build arguments to specify the service directory.
ARG SERVICE_DIR

# Change to the specific service directory.
WORKDIR /app/${SERVICE_DIR}

# Set environment variable to avoid creating source maps for production builds.
ENV GENERATE_SOURCEMAP=false

# Start command for each service.
CMD ["yarn", "dev"]
