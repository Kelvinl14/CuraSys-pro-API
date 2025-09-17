#!/usr/bin/env bash
# wait-for-it.sh - aguarda até que um host:porta esteja disponível

set -e

host="$1"
shift
port="$1"
shift

echo "⏳ Aguardando $host:$port estar disponível..."

while ! nc -z "$host" "$port"; do
  sleep 1
done

echo "✅ $host:$port está pronto. Executando comando..."
exec "$@"
