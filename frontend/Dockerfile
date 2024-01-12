# ./frontend/Dockerfile
FROM node:14

WORKDIR /app

COPY . ./

RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
