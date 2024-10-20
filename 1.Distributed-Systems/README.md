## Up app
`docker-compose up --build` or `docke-compose up -d` it depends from your needs


## Send request
curl -X POST http://localhost:5000/messages -H "Content-Type: application/json" -d '{"data": {"text": "Hello, world"}, "meta" : {"concern": 3 }}'

## Logs
If you do not want to run app, then you can see just ./logs-for-teacher