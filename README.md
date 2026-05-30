# SimplCash — End-to-End DevSecOps Pipeline on AWS EKS

> A production-style DevSecOps showcase: full CI/CD pipeline with security scanning, GitOps deployment to Kubernetes, and complete observability — built around a real working full-stack expense tracker application.

[![CI/CD](https://img.shields.io/badge/CI%2FCD-Jenkins-D24939?logo=jenkins&logoColor=white)](https://www.jenkins.io/)
[![GitOps](https://img.shields.io/badge/GitOps-ArgoCD-EF7B4D?logo=argo&logoColor=white)](https://argo-cd.readthedocs.io/)
[![Container](https://img.shields.io/badge/Container-Docker-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Orchestration](https://img.shields.io/badge/Orchestration-Kubernetes-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Cloud](https://img.shields.io/badge/Cloud-AWS%20EKS-FF9900?logo=amazonaws&logoColor=white)](https://aws.amazon.com/eks/)
[![Security](https://img.shields.io/badge/SAST-SonarQube-4E9BCD?logo=sonarqube&logoColor=white)](https://www.sonarqube.org/)
[![Scanning](https://img.shields.io/badge/Scanning-Trivy%20%7C%20OWASP-1904DA)](https://www.aquasec.com/products/trivy/)
[![Monitoring](https://img.shields.io/badge/Monitoring-Prometheus%20%7C%20Grafana-E6522C?logo=prometheus&logoColor=white)](https://prometheus.io/)

---

## 🎯 What this project demonstrates

This isn't a "Hello World" CI/CD demo. SimplCash is a complete reference implementation of a modern DevSecOps pipeline — from code commit to production deployment on Kubernetes — with security gates, observability, and GitOps practices wired in end-to-end.

The application (an expense tracker with auth) is intentionally simple. **The platform around it is the actual portfolio piece.**

---

## 🏗️ Architecture

```
┌─────────────┐    Push code    ┌─────────────────────────────────────────────────┐
│   GitHub    │ ──────────────► │            Jenkins CI Pipeline                  │
└─────────────┘                 │  ┌─────────────────────────────────────────┐    │
                                │  │ Validate → Workspace cleanup            │    │
                                │  │     ↓                                   │    │
                                │  │ Git Checkout                            │    │
                                │  │     ↓                                   │    │
                                │  │ Trivy Filesystem Scan                   │    │
                                │  │     ↓                                   │    │
                                │  │ OWASP Dependency Check                  │    │
                                │  │     ↓                                   │    │
                                │  │ SonarQube Code Analysis + Quality Gate  │    │
                                │  │     ↓                                   │    │
                                │  │ Docker Build (app + db images)          │    │
                                │  │     ↓                                   │    │
                                │  │ Docker Push → DockerHub                 │    │
                                │  │     ↓                                   │    │
                                │  │ Trigger Jenkins CD Pipeline             │    │
                                │  └─────────────────────────────────────────┘    │
                                └────────────────────┬────────────────────────────┘
                                                     │
                                                     ▼
                                ┌─────────────────────────────────────────────────┐
                                │           Jenkins CD Pipeline (GitOps/)         │
                                │  ┌─────────────────────────────────────────┐    │
                                │  │ Verify Docker Image Tags                │    │
                                │  │     ↓                                   │    │
                                │  │ Update Kubernetes manifests             │    │
                                │  │     ↓                                   │    │
                                │  │ Push updated manifests → GitHub         │    │
                                │  └─────────────────────────────────────────┘    │
                                └────────────────────┬────────────────────────────┘
                                                     │
                                                     ▼
┌─────────────┐                 ┌─────────────────────────────────────────────────┐
│   GitHub    │ ──── Pull ────► │              ArgoCD (GitOps)                    │
│ (manifests) │                 │   Auto-sync enabled • Self-healing              │
└─────────────┘                 └────────────────────┬────────────────────────────┘
                                                     │
                                                     ▼ Deploy
                                ┌─────────────────────────────────────────────────┐
                                │              AWS EKS Cluster                    │
                                │                                                 │
                                │   ┌──────────────┐      ┌──────────────────┐    │
                                │   │ frontend-pod │ ───► │ mysql-deployment │    │
                                │   │ (Flask app)  │      │  + PV / PVC      │    │
                                │   └──────────────┘      └──────────────────┘    │
                                │                                                 │
                                │   Monitoring stack:                             │
                                │   ┌──────────────┐      ┌──────────────────┐    │
                                │   │  Prometheus  │ ───► │     Grafana      │    │
                                │   └──────────────┘      └──────────────────┘    │
                                └────────────────────┬────────────────────────────┘
                                                     │
                                                     ▼ Notify
                                              ┌──────────────┐
                                              │ Email (SMTP) │
                                              └──────────────┘
```

---

## 🔧 Tech Stack

| Layer | Tools |
|---|---|
| **Source Control** | GitHub |
| **CI Pipeline** | Jenkins (declarative pipeline, parameterized) |
| **Security Scanning** | Trivy (filesystem + image), OWASP Dependency-Check, SonarQube (SAST + Quality Gates) |
| **Container Registry** | DockerHub |
| **CD Pipeline** | Jenkins CD job + ArgoCD (GitOps) |
| **Orchestration** | Kubernetes on AWS EKS |
| **Workloads** | Flask frontend, MySQL database, PV/PVC for persistent storage |
| **Observability** | Prometheus (kube-prometheus-stack), Grafana dashboards, Alertmanager |
| **Notifications** | Email on build success/failure |
| **Application** | Python (Flask), HTML/CSS, MySQL |

---

## 📂 Repository Structure

```
simplcash/
├── Database/
│   └── Dockerfile                    # MySQL container image
│
├── GitOps/
│   └── Jenkinsfile                   # CD pipeline — updates manifests, triggers ArgoCD sync
│
├── kubernetes/
│   ├── README.md                     # Kubernetes deployment notes
│   ├── frontend.yaml                 # Flask app Deployment + Service
│   ├── mongodb.yaml                  # MySQL Deployment + Service
│   ├── persistentVolume.yaml         # PV for MySQL data
│   ├── persistentVolumeClaim.yaml    # PVC bound to MySQL pod
│   └── assets/                       # Supporting K8s assets
│
├── static/                           # Frontend static files
│   ├── logo.svg
│   └── style.css
│
├── templates/                        # Flask HTML templates (Jinja2)
│
├── app.py                            # Flask application entrypoint
├── requirements.txt                  # Python dependencies
├── Dockerfile                        # App container image
├── docker-compose.yml                # Local dev: app + DB orchestration
├── Jenkinsfile                       # CI pipeline (build, scan, push)
├── .gitignore
└── README.md
```

---

## 🚀 The CI Pipeline (`Simplcash-CI`)

The root `Jenkinsfile` defines a multi-stage Jenkins declarative pipeline with security gates baked in:

| Stage | Purpose |
|---|---|
| **Validate Parameters** | Sanity check input parameters before running |
| **Workspace Cleanup** | Ensure a clean build environment |
| **Git Checkout** | Pull latest code from GitHub |
| **Trivy Filesystem Scan** | Scan source repo for known vulnerabilities |
| **OWASP Dependency Check** | Analyze `requirements.txt` for CVEs |
| **SonarQube Code Analysis** | Static analysis: bugs, vulnerabilities, code smells, coverage |
| **SonarQube Quality Gate** | Fail the build if quality gate doesn't pass |
| **Docker: Build Images** | Build both `simplcash` (app) and `simplcash-db` (database) images |
| **Docker: Push to DockerHub** | Push tagged images (versioned, e.g. `v5`) |
| **Trigger CD** | Kick off `Simplcash-CD` downstream job |

Every commit goes through **3 independent security checks** before an image ever reaches the registry.

---

## 🚢 The CD Pipeline (`Simplcash-CD`) + GitOps

The `GitOps/Jenkinsfile` handles the CD half:

1. **Verifies Docker image tags** exist in the registry
2. **Updates Kubernetes manifests** (image tag bump in `kubernetes/frontend.yaml`, `kubernetes/mongodb.yaml`)
3. **Pushes updated manifests back to GitHub**
4. **ArgoCD detects the change** (auto-sync enabled) and applies it to the EKS cluster
5. **Email notification** sent with build log attached

Average pipeline runtime: **~5 seconds** for the CD job — the actual deploy is handled by ArgoCD's reconciliation loop.

**Why GitOps?** Git is the single source of truth. Rollback = `git revert`. Cluster state always matches the repo. No `kubectl apply` ever runs from a CI server.

---

## ☸️ Kubernetes Resources

Deployed to the `simplcash` namespace on AWS EKS via the manifests in `kubernetes/`:

| Resource | File | Purpose |
|---|---|---|
| `frontend-deployment` | `frontend.yaml` | Flask app pods (scalable replicas) |
| `frontend-service` | `frontend.yaml` | NodePort service (port 5000 → 31000) |
| `mysql-deployment` | `mongodb.yaml` | MySQL database backend |
| `mysql-service` | `mongodb.yaml` | ClusterIP service (port 3306) for DB access |
| `mysql-pv` | `persistentVolume.yaml` | Persistent Volume for MySQL data |
| `mysql-pvc` | `persistentVolumeClaim.yaml` | PVC binding the volume to the MySQL pod |

Verify with:
```bash
kubectl get all -n simplcash
```

---

## 📊 Observability Stack

### Prometheus
Deployed via `kube-prometheus-stack` Helm chart. Service monitors scraping:
- ArgoCD components (application-controller, dex-server, repo-server, applicationset-controller)
- Kubernetes API server
- CoreDNS
- Grafana itself
- Alertmanager
- Node-level metrics via node-exporter

### Grafana
Pre-built dashboards for:
- **Kubernetes / Compute Resources / Namespace (Pods)** — CPU/memory per pod in any namespace
- **Kubernetes / Compute Resources / Pod** — Per-pod deep dive (CPU usage gauge, memory RSS/cache, bandwidth in/out)
- **ArgoCD-specific metrics** — controller workload, repo-server sync times

Dashboards visualize live metrics for both `simplcash` and `argocd` namespaces.

---

## 🔐 Security Practices

- ✅ **Shift-left scanning** — Trivy + OWASP run *before* Docker build
- ✅ **SAST gating** — SonarQube quality gate blocks builds with new vulnerabilities
- ✅ **Image scanning** — Trivy on both source code and built containers
- ✅ **Dependency CVE tracking** — OWASP Dependency-Check on every build
- ✅ **Secrets externalized** — DockerHub credentials via Jenkins credentials store (`${dockerhubpass}`), never hardcoded
- ✅ **Quality gates enforced** — Build fails on regressions in reliability, security, maintainability ratings
- ✅ **GitOps audit trail** — Every deployment is a Git commit, fully traceable

---

## 📈 Pipeline Quality Gates (Latest Run)

SonarQube quality gate status: **Passed** ✅

| Metric | Result |
|---|---|
| New Bugs | 0 |
| New Vulnerabilities | 0 |
| New Security Hotspots | 0 |
| New Code Smells | 0 |
| Reliability Rating | A |
| Security Rating | A |
| Maintainability Rating | A |

---

## 🖥️ The Application — SimplCash

A simple expense tracker built to provide a realistic CRUD workload to deploy:

- **Sign Up / Login** flow (auth)
- **Add Expense** — amount + description
- **View Expenses** — list with amount, description, timestamp
- **Logout**

Built with Python (Flask) + Jinja2 templates + HTML/CSS + MySQL.

---

## 🧪 Run It Locally

Using the included `docker-compose.yml`:

```bash
# Clone the repo
git clone https://github.com/arpitj105/Docker-Projects.git
cd Docker-Projects/simplcash

# Spin up app + database together
docker-compose up --build

# Visit http://localhost:5000
```

Or use the published images directly:

```bash
docker pull arpitj105/simplcash:latest
docker pull arpitj105/simplcash-db:latest
```

---

## ☁️ Deploy to Kubernetes (manual, for testing)

GitOps via ArgoCD is the recommended path, but for ad-hoc testing:

```bash
kubectl create namespace simplcash
kubectl apply -f kubernetes/persistentVolume.yaml
kubectl apply -f kubernetes/persistentVolumeClaim.yaml -n simplcash
kubectl apply -f kubernetes/mongodb.yaml -n simplcash
kubectl apply -f kubernetes/frontend.yaml -n simplcash

# Verify
kubectl get all -n simplcash

# Access the app
kubectl get svc frontend-service -n simplcash
# Visit http://<node-ip>:31000
```

---

## 🎓 What I Learned Building This

- **GitOps changes everything.** Once ArgoCD was wired in, "deploying" became "merging a PR." Drift detection alone is worth the setup cost.
- **Quality gates have to be enforcing, not advisory.** A SonarQube scan that doesn't fail the build is just decoration.
- **Multi-image pipelines need careful tagging.** Both the app and DB image tags must be synced or you get version skew across pods.
- **Observability isn't a deploy-time concern.** Prometheus + Grafana had to be in place *before* I needed them — debugging without metrics is debugging blind.
- **Email notifications matter more than dashboards.** Engineers don't check Jenkins; they check Gmail.


---

## 📫 Contact

**Arpit Jain** — Senior DevOps Engineer
- LinkedIn: [arpit-jain-devops](https://linkedin.com/in/arpit-jain-devops)
- GitHub: [@arpitj105](https://github.com/arpitj105)
- Email: arpitayush99@gmail.com

---

*Built as a personal portfolio project to demonstrate end-to-end DevSecOps practices. Not affiliated with any employer.*
