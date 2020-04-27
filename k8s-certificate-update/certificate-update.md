Solution:  
https://www.ibm.com/support/knowledgecenter/SSCKRH_1.0.3/platform/t_certificate_renewal.html

Steps:
* check version of K8S  
```sh
kubeadm version 
```
* configuration file 
```sh
sudo cat /etc/root/kubeadm.yaml
# sudo touch /etc/root/kubeadm.yaml
sudo vim /etc/root/kubeadm.yaml
```
file contains
```yaml
apiVersion: kubeadm.k8s.io/v1alpha1
kind: MasterConfiguration
api:
  advertiseAddress: 10.143.126.120
kubernetesVersion: v1.11.1
```
* create archive folder
```bash
ARCHIVE_FOLDER='/home/vitalii/k8s_archive_2020_04_24'
mkdir $ARCHIVE_FOLDER
```
* save old configuration files
```bash
sudo cp /etc/kubernetes/pki/apiserver.key $ARCHIVE_FOLDER/
sudo cp /etc/kubernetes/pki/apiserver.crt $ARCHIVE_FOLDER/
sudo cp /etc/kubernetes/pki/apiserver-kubelet-client.crt $ARCHIVE_FOLDER/
sudo cp /etc/kubernetes/pki/apiserver-kubelet-client.key $ARCHIVE_FOLDER/
sudo cp /etc/kubernetes/pki/front-proxy-client.crt $ARCHIVE_FOLDER/
sudo cp /etc/kubernetes/pki/front-proxy-client.key $ARCHIVE_FOLDER/
ls $ARCHIVE_FOLDER
```

* remove old configuration files
```bash
sudo rm /etc/kubernetes/pki/apiserver.key
sudo rm /etc/kubernetes/pki/apiserver.crt
sudo rm /etc/kubernetes/pki/apiserver-kubelet-client.crt
sudo rm /etc/kubernetes/pki/apiserver-kubelet-client.key
sudo rm /etc/kubernetes/pki/front-proxy-client.crt
sudo rm /etc/kubernetes/pki/front-proxy-client.key
```

* create new certificates
```bash
sudo kubeadm --config /etc/root/kubeadm.yaml alpha phase certs apiserver
sudo kubeadm --config /etc/root/kubeadm.yaml alpha phase certs apiserver-kubelet-client
sudo kubeadm --config /etc/root/kubeadm.yaml alpha phase certs front-proxy-client
```

