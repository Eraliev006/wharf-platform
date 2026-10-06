#!/bin/bash

set -e

# runs once on empty volume via docker-entrypoint-initdb.d; not re-runnable
: "${TEST_POSTGRES_DB:?TEST_POSTGRES_DB environment variable is required.}"

psql --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<EOF
CREATE DATABASE $TEST_POSTGRES_DB;
EOF

psql --username "$POSTGRES_USER" --dbname "$TEST_POSTGRES_DB" <<EOF
REVOKE ALL ON SCHEMA public FROM PUBLIC;

CREATE SCHEMA api;
CREATE SCHEMA auth;

GRANT ALL ON SCHEMA auth TO auth_user;
GRANT ALL ON SCHEMA api TO api_user;

EOF
