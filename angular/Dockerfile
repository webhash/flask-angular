FROM nginx:alpine
copy dist/angular/ /usr/share/nginx/html
COPY nginx.conf /etc/nginx/
EXPOSE 8888
CMD ["nginx", "-g", "daemon off;"]