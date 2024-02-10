FROM node:latest


ENV APP=/app

# Change the workdir.
WORKDIR $APP

# Install the requirements
COPY package.json $APP

RUN npm install

# Copy the rest of the files
COPY . $APP

EXPOSE 3000

CMD ["node","get-dealership.js"]