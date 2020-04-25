# solution for installation k8s with flannel on bare-metal ( avoid flannel issues !!! )
install k8s master
```bash
# reset admin 
sudo kubeadm reset
ifconfig | grep -e "cni" -e "flan"
sudo ip link del cni0
sudo ip link del flannel.1
sudo systemctl restart network

# init for using flannel
sudo kubeadm init --pod-network-cidr=10.244.0.0/16
sudo rm -rf $HOME/.kube
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# !!! install flannel ( or weave.... )
sudo kubectl apply -f kube-flannel.yml

# check installation
kubectl get nodes
kubectl get pods --all-namespaces
ifconfig | grep --after 2 -e "cni" -e "flan"
```
