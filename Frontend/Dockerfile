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

# ก็อปปี้ไฟล์จากโฟลเดอร์ dist (ของ Vite) ไปที่ Nginx
COPY --from=build-stage /app/dist /usr/share/nginx/html

# (สำคัญมากสำหรับ React) ก็อปปี้ไฟล์ config ของ Nginx เพื่อให้รองรับการทำ Routing
# ถ้าคุณยังไม่มีไฟล์ nginx.conf พื้นฐาน Nginx จะเปิดหน้าแรกได้ปกติ 
# แต่ถ้ากด Refresh ในหน้าอื่น (เช่น /login) จะเจอ 404

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]