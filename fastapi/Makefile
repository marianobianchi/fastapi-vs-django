

startdb:
	docker run -d \
	           --name fastapi-books \
			   -e POSTGRES_PASSWORD=fastapi \
			   -e PGDATA=/var/lib/postgresql/data/pgdata \
    		   -v fastapi-postgres:/var/lib/postgresql/data \
			   -p 5440:5432 \
			   postgres

startapp:
	uvicorn sql_app.main:app --reload
