#!/bin/bash

docker rm -f contextdb

docker pull techterrace/contextdb

docker run --env-file .env --network host -v chroma:/app/chroma -d --name contextdb --restart always techterrace/contextdb

