#!/bin/bash
docker exec -it ecommerce-db psql -U postgres -c "
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='auth_db';
DROP DATABASE IF EXISTS auth_db;
CREATE DATABASE auth_db;

DROP DATABASE IF EXISTS catalog_db;
CREATE DATABASE catalog_db;

DROP DATABASE IF EXISTS order_db;
CREATE DATABASE order_db;

DROP DATABASE IF EXISTS marketing_db;
CREATE DATABASE marketing_db;

DROP DATABASE IF EXISTS support_db;
CREATE DATABASE support_db;
"
