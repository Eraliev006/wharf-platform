#!/bin/bash

set -e

psql --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<EOF
REVOKE ALL ON SCHEMA public FROM PUBLIC;

GRANT ALL ON SCHEMA auth TO auth_user;
GRANT ALL ON SCHEMA api TO api_user;

ALTER ROLE auth_user SET search_path TO auth;
ALTER ROLE api_user SET search_path TO api;

EOF
