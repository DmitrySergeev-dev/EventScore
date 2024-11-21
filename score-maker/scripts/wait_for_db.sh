#!/bin/bash
until (echo > /dev/tcp/score_maker_db/5432) &>/dev/null; do
  echo "Waiting for database connection..."
  sleep 1
done
echo "Database is up - executing command"
exec "$@"
