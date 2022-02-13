FROM nginx

# RUN ["rm","/etc/nginx/conf/default.conf"]
RUN ["rm","/etc/nginx/conf.d/default.conf"]

COPY uwsgi_params /etc/nginx/conf.d/
COPY django_tg_bot_nginx.conf /etc/nginx/conf/sites-available/
RUN ["ln", "-s", "/etc/nginx/sites-available/django_tg_bot_nginx.conf", "/etc/nginx/sites-enabled"]

# RUN ["ln", "-s", "code/conf/django_tg_bot_nginx.conf", "/etc/nginx/conf/"]
# RUN ["ln", "-s", "code/conf/django_tg_bot_nginx.conf", "/etc/nginx/conf.d/"]
CMD ["nginx", "-g", "daemon off;"]