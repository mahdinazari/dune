#### Member

- Register
```
curl -X POST localhost:5000/api/v1/member/register --data '{"email": "mehdi.nazari.3727@gmail.com", "password": "123456", "fullname": "mehdi"}' -H "Content-Type: application/json"
```

- Login
```
curl -X POST localhost:5000/api/v1/member/login --data '{"email": "mehdi.nazari.3727@gmail.com", "password": "123456"}' -H "Content-Type: application/json"
```

- List
```
curl localhost:5000/api/v1/member/list --header "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NDAyMDc1NTEsIm5iZiI6MTY0MDIwNzU1MSwianRpIjoiZjE3ZTYzN2QtMWRjMi00YmQ4LTgzZDktY2E4ODYwMTU3OWZkIiwiZXhwIjoxNjQwMjA5MzUxLCJpZGVudGl0eSI6eyJpZCI6ImQ5NmU3ZjFiLTRkMjktNGM4Ny1hZjFhLTFlYTFmM2IwN2U1ZiIsImVtYWlsIjoibWVoZGkubmF6YXJpLjM3MjdAZ21haWwuY29tIn0sImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.uc4BHQ2LZP3CtK2yxjpPfSfksoL1cqwgwwMFveY5Iak"
```
