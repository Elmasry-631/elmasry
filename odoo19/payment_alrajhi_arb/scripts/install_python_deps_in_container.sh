#!/bin/sh
# Run from the same directory as docker-compose.yml (e.g. /opt/odoo17new).
# Replace "odoo" with your compose service name if different (see: docker compose ps).
#
# After this, use ONLY: docker compose restart odoo
# Do NOT run:            docker compose down -v
# or pip packages are gone (new container from image). For persistence, use Dockerfile.odoo17-arb-deps.

set -e
SERVICE="${ODOO_SERVICE:-odoo}"

docker compose exec -u root "$SERVICE" pip3 install --no-cache-dir requests pycryptodome
docker compose restart "$SERVICE"
docker compose exec "$SERVICE" python3 -c "import pkg_resources; pkg_resources.get_distribution('pycryptodome'); print('pycryptodome OK')"
