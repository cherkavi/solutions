---
# K8S master
```bash
/usr/bin/kubelet
    --bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf
    --kubeconfig=/etc/kubernetes/kubelet.conf
    --config=/var/lib/kubelet/config.yaml
    --cgroup-driver=cgroupfs
    --cni-bin-dir=/opt/cni/bin
    --cni-conf-dir=/etc/cni/net.d
    --network-plugin=cni
    --resolv-conf=/run/systemd/resolve/resolv.conf
    --feature-gates=DevicePlugins=true

etcd
    --advertise-client-urls=https://127.0.0.1:2379
    --cert-file=/etc/kubernetes/pki/etcd/server.crt
    --client-cert-auth=true
    --data-dir=/var/lib/etcd
    --initial-advertise-peer-urls=https://127.0.0.1:2380
    --initial-cluster=gtxmachine0-ev=https://127.0.0.1:2380
    --key-file=/etc/kubernetes/pki/etcd/server.key
    --listen-client-urls=https://127.0.0.1:2379
    --listen-peer-urls=https://127.0.0.1:2380
    --name=gtxmachine0-ev
    --peer-cert-file=/etc/kubernetes/pki/etcd/peer.crt
    --peer-client-cert-auth=true
    --peer-key-file=/etc/kubernetes/pki/etcd/peer.key
    --peer-trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
    --snapshot-count=10000
    --trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt

kube-controller-manager
 --address=127.0.0.1
 --cluster-signing-cert-file=/etc/kubernetes/pki/ca.crt
 --cluster-signing-key-file=/etc/kubernetes/pki/ca.key
 --controllers=*,bootstrapsigner,tokencleaner
 --kubeconfig=/etc/kubernetes/controller-manager.conf
 --leader-elect=true
 --root-ca-file=/etc/kubernetes/pki/ca.crt
 --service-account-private-key-file=/etc/kubernetes/pki/sa.key
 --use-service-account-credentials=true

kube-scheduler
 --address=127.0.0.1
 --kubeconfig=/etc/kubernetes/scheduler.conf
 --leader-elect=true

kube-apiserver
 --authorization-mode=Node,RBAC
 --advertise-address=10.143.226.20
 --allow-privileged=true
 --client-ca-file=/etc/kubernetes/pki/ca.crt
 --disable-admission-plugins=PersistentVolumeLabel
 --enable-admission-plugins=NodeRestriction
 --enable-bootstrap-token-auth=true
 --etcd-cafile=/etc/kubernetes/pki/etcd/ca.crt
 --etcd-certfile=/etc/kubernetes/pki/apiserver-etcd-client.crt
 --etcd-keyfile=/etc/kubernetes/pki/apiserver-etcd-client.key
 --etcd-servers=https://127.0.0.1:2379
 --insecure-port=0
 --kubelet-client-certificate=/etc/kubernetes/pki/apiserver-kubelet-client.crt
 --kubelet-client-key=/etc/kubernetes/pki/apiserver-kubelet-client.key
 --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname
 --proxy-client-cert-file=/etc/kubernetes/pki/front-proxy-client.crt
 --proxy-client-key-file=/etc/kubernetes/pki/front-proxy-client.key
 --requestheader-allowed-names=front-proxy-client
 --requestheader-client-ca-file=/etc/kubernetes/pki/front-proxy-ca.crt
 --requestheader-extra-headers-prefix=X-Remote-Extra-
 --requestheader-group-headers=X-Remote-Group
 --requestheader-username-headers=X-Remote-User
 --secure-port=6443
 --service-account-key-file=/etc/kubernetes/pki/sa.pub
 --service-cluster-ip-range=10.96.0.0/12
 --tls-cert-file=/etc/kubernetes/pki/apiserver.crt
 --tls-private-key-file=/etc/kubernetes/pki/apiserver.key

/usr/local/bin/kube-proxy
 --config=/var/lib/kube-proxy/config.conf

/opt/bin/flanneld
 --ip-masq
 --kube-subnet-mgr
```

---
# K8S working node
```bash
/usr/bin/kubelet 
    --bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf 
    --kubeconfig=/etc/kubernetes/kubelet.conf 
    --config=/var/lib/kubelet/config.yaml 
    --cgroup-driver=cgroupfs 
    --cni-bin-dir=/opt/cni/bin 
    --cni-conf-dir=/etc/cni/net.d 
    --network-plugin=cni 
    --resolv-conf=/run/systemd/resolve/resolv.conf 
    --feature-gates=DevicePlugins=true

/usr/local/bin/kube-proxy 
    --config=/var/lib/kube-proxy/config.conf

/opt/bin/flanneld 
    --ip-masq 
    --kube-subnet-mgr
```
