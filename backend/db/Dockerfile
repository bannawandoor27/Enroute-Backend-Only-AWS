
FROM postgres:15.2-alpine


ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD banna
ENV POSTGRES_DB enroute

COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432


CMD ["postgres"]