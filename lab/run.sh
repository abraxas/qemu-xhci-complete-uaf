#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-qemu-xhci-complete-uaf}"
export PYTHONUNBUFFERED=1
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

LABEL="qemu-xhci-complete-uaf"
WITNESS="QEMU-XHCI-COMPLETE-UAF-WITNESS"
QTEST_HOST="127.0.0.1"
QTEST_PORT="18700"

mkdir -p work

down() {
  echo "== docker compose down -v =="
  docker compose -p "${COMPOSE_PROJECT_NAME}" down -v --remove-orphans || true
}

fail_setup() {
  local reason="$1"
  echo "FAIL ${LABEL} ${reason} ${WITNESS}" | tee poc-last-run.txt
  exit 1
}

trap down EXIT

echo "== docker compose down (clean) =="
down

echo "== docker compose up --build =="
up_ok=0
for attempt in $(seq 1 3); do
  if docker compose -p "${COMPOSE_PROJECT_NAME}" up --build -d; then
    up_ok=1
    break
  fi
  echo "compose-up-retry attempt=${attempt}"
  sleep 8
  down
done
if [[ "${up_ok}" != 1 ]]; then
  fail_setup "compose-up-failed"
fi

echo "== wait qtest ${QTEST_HOST}:${QTEST_PORT} =="
ok=0
for i in $(seq 1 90); do
  if python3 - <<PY
import socket
import sys

try:
    with socket.create_connection(("${QTEST_HOST}", int("${QTEST_PORT}")), timeout=2):
        sys.exit(0)
except OSError:
    sys.exit(1)
PY
  then
    ok=1
    echo "qtest-ready attempt=${i}"
    break
  fi
  echo "qtest-wait attempt=${i}"
  sleep 1
done
if [[ "${ok}" != 1 ]]; then
  echo "== compose logs (not ready) =="
  docker compose -p "${COMPOSE_PROJECT_NAME}" logs --no-color --tail=160 || true
  fail_setup "qtest-not-ready"
fi

echo "== poc.py =="
set +e
python3 ./poc.py | tee poc-last-run.txt
rc=${PIPESTATUS[0]}
set -e

if ! tail -n1 poc-last-run.txt 2>/dev/null | grep -qE '^(SUCCESS|FAIL) '; then
  echo "FAIL ${LABEL} poc-exit=${rc} ${WITNESS}" >> poc-last-run.txt
  rc=1
fi

exit "${rc}"
