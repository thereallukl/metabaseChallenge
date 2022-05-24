#!/bin/bash

set -ex


TOOLBOX_CONTAINER="docker run --rm --net=host -v \"${HOME}/.minikube:${HOME}/.minikube\" -v \"${HOME}/.kube:/root/.kube\" -v \"${HOME}/.config/helm:/root/.config/helm\" -v \"${PWD}:/wd\" --workdir /wd quay.io/roboll/helmfile:helm3-v0.135.0"

echo "Deploying components"
eval $TOOLBOX_CONTAINER helmfile sync
echo "Waiting for database"
eval $TOOLBOX_CONTAINER kubectl -n challenge rollout status --watch --timeout=600s statefulset/postgres-postgresql
echo "Database up"
echo "Initializing database"
POSTGRES_PASSWORD=$(eval $TOOLBOX_CONTAINER kubectl get secret --namespace challenge postgres-postgresql -o jsonpath="{.data.postgres-password}" | base64 --decode)
eval $TOOLBOX_CONTAINER kubectl -n challenge delete pod postgres-postgresql-client || true
eval $TOOLBOX_CONTAINER kubectl run postgres-postgresql-client --namespace challenge --image docker.io/bitnami/postgresql:14.3.0-debian-10-r7 --env="PGPASSWORD=$POSTGRES_PASSWORD" \
      --command -- sleep 999999
eval $TOOLBOX_CONTAINER kubectl -n challenge wait --for=condition=ready pod postgres-postgresql-client
eval $TOOLBOX_CONTAINER kubectl -n challenge cp data-seed/pagila-schema.sql postgres-postgresql-client:/tmp/
eval $TOOLBOX_CONTAINER kubectl -n challenge exec postgres-postgresql-client -- psql --host postgres-postgresql -U postgres -f /tmp/pagila-schema.sql
eval $TOOLBOX_CONTAINER kubectl -n challenge cp data-seed/pagila-data.sql postgres-postgresql-client:/tmp/
eval $TOOLBOX_CONTAINER kubectl -n challenge exec postgres-postgresql-client -- psql -U postgres --host postgres-postgresql -f /tmp/pagila-data.sql
eval $TOOLBOX_CONTAINER kubectl -n challenge delete pod postgres-postgresql-client