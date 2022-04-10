# Build
```
PREFIX=firefish
docker build -t "$PREFIX/languagetool:5.7.0" .
docker push "$PREFIX/languagetool:5.7.0"
```

# Run
```
PREFIX=firefish
docker run -p 127.0.0.1:8081:8081 --name lt "$PREFIX/languagetool:5.7.0"
```