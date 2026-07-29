# Projet DevOps - Gestion des Taches

Application de gestion de taches type Trello, deployee avec Ansible + Jenkins + Kubernetes.

## Structure
- `app/` : application Flask
- `ansible/` : playbooks de provisioning
- `k8s/` : fichiers YAML Kubernetes
- `Vagrantfile` : creation des VM locales

## Lancer en local
cd app
venv\Scripts\activate
python app.py
