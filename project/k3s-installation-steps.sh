# Steps to install k3s kubernetes distribution on opensuse/Leap server.
sudo zypper install -y apparmor-parser
curl -sfL https://get.k3s.io | sh -
mkdir $HOME/.kube
sudo cp /etc/rancher/k3s/k3s.yaml $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
echo 'export KUBECONFIG=$KUBECONFIG:$HOME/.kube/config' >> $HOME/.profile
source $HOME/.profile
kubectl completion bash > $HOME/.kubectl_bash_completion
echo 'source $HOME/.kubectl_bash_completion' >> $HOME/.profile
source $HOME/.profile
