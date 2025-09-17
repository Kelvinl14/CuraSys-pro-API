Write-Host "🚨 Resetando containers, volumes e migrations..."

# Derruba containers e remove volumes
docker-compose down -v

# Remove pasta de migrações
if (Test-Path "migrations") {
    Remove-Item -Recurse -Force "migrations"
}

# Sobe containers novamente
docker-compose up -d --build

Write-Host "⏳ Esperando o banco inicializar..."
Start-Sleep -Seconds 5

# Recria migrações
docker-compose exec api-curasys-pro flask db init
docker-compose exec api-curasys-pro flask db migrate -m "Initial migration"
docker-compose exec api-curasys-pro flask db upgrade

Write-Host "✅ Reset completo! Banco recriado do zero."
