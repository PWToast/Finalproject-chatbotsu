# Stage 1: Build
FROM node:22-alpine as build-stage

WORKDIR /app

# ติดตั้ง dependencies
COPY package*.json ./
RUN npm install

# Build โปรเจค
COPY . .
RUN npm run build

# Stage 2: Serve ด้วย Nginx
FROM nginx:stable-alpine as production-stage

# ก็อปปี้ไฟล์จากโฟลเดอร์ dist ของ Vite ไปที่ Nginx
COPY --from=build-stage /app/dist /usr/share/nginx/html

# แต่ถ้ากด Refresh ในหน้าอื่น (เช่น /login) จะเจอ 404

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]