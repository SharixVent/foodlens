FROM node:20-alpine
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci || npm i
COPY . .
ENV PORT=3000 HOST=0.0.0.0
CMD ["npm","run","dev"]
