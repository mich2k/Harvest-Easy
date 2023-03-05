FROM node:18-alpine AS builder
WORKDIR /app
COPY package.json ./
COPY yarn.lock ./
COPY tsconfig.json .
COPY tailwind.config.js .


RUN yarn install --frozen-lockfile
COPY . .
RUN yarn build

FROM nginx:1.19-alpine AS server

COPY --from=builder ./app/build /usr/share/nginx/html


RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx/nginx.conf /etc/nginx/conf.d


EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]