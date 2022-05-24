# Dependencies
- bash
- docker
- minikube (optional)

# Deployment
1. Prepare kubernetes cluster
2. Login to your cluster and set it as current context
3. Run deployment script ./deploy.sh
4. Api is protected with basic auth, with username == `api` and default password == `SecRetPass`


# Prepare environment on Ubuntu
1. Install minikube
2. Create minikube cluster `minikube start --driver=kvm2`
3. Get minikube ip `minikube ip`
4. Get interface of minikube `ip r | grep <minikube_ip>`
5. Configure DNS 
```bash
resolvectl dns <interface name> 10.96.0.10
resolvectl domain  <interface_name> "~cluster.local"
```
6. Run minikube tunnel `minikube tunnel`
7. After deploying the API go to `minio.challenge.svc.cluster.local` to verify if minio website is opening successfully