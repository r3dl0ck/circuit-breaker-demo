# Circuit Breaker demo

## Build container image

```
$ docker build . -t docker.io/devopstestaccount/circuit-breaker:1.0
$ docker push docker.io/devopstestaccount/circuit-breaker:1.0

$ docker build . -t quay.io/mmqaz/circuit-breaker:1.0
$ docker push quay.io/mmqaz/circuit-breaker:1.0
```

## Start
```
docker run -it --rm --net=host docker.io/devopstestaccount/circuit-breaker:1.0
```

## TEST
```
while true ; do curl localhost:8080; sleep 5; done
```
