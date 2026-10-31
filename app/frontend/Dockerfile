# ---- build stage ----
FROM node:20-alpine AS build
WORKDIR /web
COPY package*.json ./
RUN npm install --no-audit --no-fund
COPY . .
RUN npm run build

# ---- runtime stage: unprivileged nginx on 8080 (works with runAsNonRoot) ----
FROM nginxinc/nginx-unprivileged:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /web/dist /usr/share/nginx/html
EXPOSE 8080
