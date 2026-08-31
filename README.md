# Projet DevOps - Gestion des Taches

App Kanban (Flask) deployee automatiquement via Ansible + Jenkins + Kubernetes.

**Stack** : Flask/SQLite-Postgres, 2 VM Vagrant (jenkins-server 192.168.56.10, k8s-server 192.168.56.11), Jenkins CI/CD, Minikube.

## Demarrage rapide

```bash
git clone https://github.com/morafikhajar/Projet-devops.git
cd Projet-devops
vagrant up                          # provisionne les 2 VM (Ansible)

vagrant ssh k8s-server
minikube start --driver=docker --memory=4000 --cpus=2   # demarrage manuel volontaire (evite de relancer le cluster a chaque vagrant up)
kubectl get nodes                   # doit etre Ready
```

Jenkins : `http://192.168.56.10:8080` — recuperer le mot de passe initial via
`sudo cat /var/lib/jenkins/secrets/initialAdminPassword` en SSH sur jenkins-server.
Ajouter les credentials DockerHub (`dockerhub-creds`) et SSH k8s (`k8s-ssh-creds`),
puis creer un pipeline (Pipeline script from SCM, Jenkinsfile a la racine).

Lancer le build → clone, tests pytest, build+push Docker, deploiement K8s automatique.

Acceder a l'app (NodePort non accessible directement avec le driver Docker de
minikube — voir "Difficultes" — donc port-forward requis) :
```bash
kubectl port-forward --address 0.0.0.0 svc/todo-service 5000:5000
```
Puis `http://192.168.56.11:5000`

## Lancer en local (dev, sans Docker/K8s)

```bash
cd app
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
python app.py           # lancer l'app
pytest -v                # lancer les tests
```

## Difficultes rencontrees

- **RAM insuffisante (8 Go hote)** → minikube timeout au demarrage (`kubeadm init timed out`), cause des echecs Jenkins #1-9. Resolu en liberant des VM VirtualBox inutilisees et en reduisant l'allocation minikube a 4 Go.
- **Cle GPG Jenkins** → `signed-by` echouait malgre une cle valide, contourne via `apt-key add`.
- **Jenkins/Java trop anciens** → mise a jour manuelle vers Jenkins 2.568.2 et Java 21.
- **SSH desactive par defaut** → config surchargee dans `/etc/ssh/sshd_config.d/60-cloudimg-settings.conf`, corrigee.
- **NodePort inaccessible** (driver Docker minikube) → contourne avec `kubectl port-forward`.

## Structure
ansible/ playbooks Jenkins + K8s
app/ Flask app + tests
k8s/ manifestes deployment/service/pvc/secret
Jenkinsfile pipeline CI/CD
Vagrantfile 2 VM

## Autrice
Hajar Morafik - FSAC, Universite Hassan 2