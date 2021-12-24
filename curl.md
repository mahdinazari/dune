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
- Get
```
curl localhost:5001/api/v1/member/get/a31c9897-f082-4795-a60f-0d392c8b981c  --header "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NDAyODg2MTQsIm5iZiI6MTY0MDI4ODYxNCwianRpIjoiNDM0NWRjMDctYWQwMy00ZDA2LTg3ODUtMWExM2YzMGYwYzRjIiwiZXhwIjoxNjQwMzAwNjE0LCJpZGVudGl0eSI6eyJpZCI6ImQ5NmU3ZjFiLTRkMjktNGM4Ny1hZjFhLTFlYTFmM2IwN2U1ZiIsImVtYWlsIjoibWVoZGkubmF6YXJpLjM3MjdAZ21haWwuY29tIn0sImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9._MHBwa6upehanki5TYVYS_c1VJIT3bLEiI-aefTyXHk"
```
---

#### Role
- Create
```
curl -X POST localhost:5000/api/v1/role/create --data '{"title": "admin"}' --header "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NDAyODY5MDYsIm5iZiI6MTY0MDI4NjkwNiwianRpIjoiMmYyNjEwNGItY2EyYi00YTQ1LTlkNWMtMmExN2Q1ZTdiOTBjIiwiZXhwIjoxNjQwMjg4NzA2LCJpZGVudGl0eSI6eyJpZCI6ImQ5NmU3ZjFiLTRkMjktNGM4Ny1hZjFhLTFlYTFmM2IwN2U1ZiIsImVtYWlsIjoibWVoZGkubmF6YXJpLjM3MjdAZ21haWwuY29tIn0sImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.lG4o46DCMtQ-kCcPLuwIoaRL-E-obJ-WR-wldSomDpg" -H "Content-Type: application/json"
```
- Assign
```
curl localhost:5001/api/v1/role/assign/47de602a-9daf-4cd0-b716-8f2fb682714b/member/a31c9897-f082-4795-a60f-0d392c8b981c  --header "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NDAyODg2MTQsIm5iZiI6MTY0MDI4ODYxNCwianRpIjoiNDM0NWRjMDctYWQwMy00ZDA2LTg3ODUtMWExM2YzMGYwYzRjIiwiZXhwIjoxNjQwMzAwNjE0LCJpZGVudGl0eSI6eyJpZCI6ImQ5NmU3ZjFiLTRkMjktNGM4Ny1hZjFhLTFlYTFmM2IwN2U1ZiIsImVtYWlsIjoibWVoZGkubmF6YXJpLjM3MjdAZ21haWwuY29tIn0sImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9._MHBwa6upehanki5TYVYS_c1VJIT3bLEiI-aefTyXHk"
```
- List
```
url localhost:5000/api/v1/role/list -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NDAzNjU4MTYsIm5iZiI6MTY0MDM2NTgxNiwianRpIjoiMmI2YjZlMDQtMDk1My00NmYxLTk4OGYtZjcyYmVkY2FhMTA2IiwiZXhwIjoxNjQwMzc3ODE2LCJpZGVudGl0eSI6eyJpZCI6ImQ5NmU3ZjFiLTRkMjktNGM4Ny1hZjFhLTFlYTFmM2IwN2U1ZiIsImVtYWlsIjoibWVoZGkubmF6YXJpLjM3MjdAZ21haWwuY29tIn0sImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.KoMmC_0RDOZbSe18NtSpvqeNIzp00pTZgSJCY2gL8kM"
```