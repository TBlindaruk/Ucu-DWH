### Lab for second 

#### 4 tasks

Build container via `docker build -f Dockerfile -t sample-app .`
![img](./files/4-1-build.png)

Run container via ` docker run -d -p 8051:8050 sample-app`
![img](./files/4-2-run.png)

So as a result we can see in `127.0.0.1:8051` our app
![img](./files/4-3-result.png)

#### 5 tasks

Build container with entry point `docker build -f Dockerfile -t sample-app-2 .`
![img](./files/5-1-build.png)

Then ran a new container with shared data `docker run -it -p 8052:8050 -v ./temp:/app/temp-inside sample-app-2 /app/temp-inside/obj_dependency_data2.csv`
![img](./files/5-2-run.png)

As a result on 8052 host we can see app with modified data
![img](./files/5-3-app.png)