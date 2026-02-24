# 📁 Project Structure

```
ai-agent-platform-databricks-aws/
├── 📄 README.md                          # Main documentation
├── 📄 LICENSE                            # MIT License
├── 📄 .env.example                       # Environment variables template
├── 📄 .gitignore                         # Git ignore rules
├── 📄 requirements.txt                   # Python dependencies
├── 📄 orchestrator.py                    # Main orchestrator service
├── 📄 index.html                         # Interactive UI
│
├── 🤖 agents/                            # AI Agent implementations
│   ├── nova.py                           # Infrastructure agent (AWS EKS, ECR, API Gateway)
│   ├── axiom.py                          # Data pipeline agent (S3, Delta Lake, Databricks)
│   ├── sentinel.py                       # Testing & red team agent
│   ├── nexus.py                          # Documentation agent
│   └── prometheus.py                     # Optimization & monitoring agent
│
├── 🏗️ infrastructure/                    # Infrastructure as Code
│   ├── docker/                           # Docker configurations
│   │   ├── Dockerfile.orchestrator
│   │   ├── Dockerfile.nova
│   │   ├── Dockerfile.axiom
│   │   ├── Dockerfile.sentinel
│   │   ├── Dockerfile.nexus
│   │   └── Dockerfile.prometheus
│   │
│   ├── kubernetes/                       # Kubernetes manifests
│   │   ├── namespace.yaml
│   │   ├── deployments/
│   │   │   ├── orchestrator.yaml
│   │   │   ├── nova.yaml
│   │   │   ├── axiom.yaml
│   │   │   ├── sentinel.yaml
│   │   │   ├── nexus.yaml
│   │   │   └── prometheus.yaml
│   │   ├── services/
│   │   │   └── *.yaml
│   │   ├── configmaps/
│   │   ├── secrets/
│   │   └── hpa/                          # Horizontal Pod Autoscalers
│   │
│   └── terraform/                        # Terraform IaC
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       ├── eks/                          # EKS cluster
│       ├── rds/                          # PostgreSQL database
│       ├── s3/                           # S3 buckets
│       └── networking/                   # VPC, subnets, security groups
│
├── 📚 docs/                              # Documentation
│   ├── architecture.md                   # System architecture
│   ├── aws-integration.md                # AWS services guide
│   ├── databricks-setup.md               # Databricks configuration
│   ├── api-reference.md                  # API documentation
│   ├── deployment.md                     # Deployment guide
│   ├── monitoring.md                     # Monitoring & observability
│   ├── security.md                       # Security best practices
│   ├── troubleshooting.md                # Common issues & solutions
│   └── diagrams/                         # Architecture diagrams
│
├── 🧪 tests/                             # Test suites
│   ├── unit/                             # Unit tests
│   │   ├── test_nova.py
│   │   ├── test_axiom.py
│   │   ├── test_sentinel.py
│   │   ├── test_nexus.py
│   │   └── test_prometheus.py
│   ├── integration/                      # Integration tests
│   │   ├── test_orchestrator.py
│   │   ├── test_agent_collaboration.py
│   │   └── test_aws_integration.py
│   ├── e2e/                              # End-to-end tests
│   │   ├── test_deployment_workflow.py
│   │   └── test_data_pipeline.py
│   └── fixtures/                         # Test data & mocks
│
├── 🔧 scripts/                           # Utility scripts
│   ├── launch_ui.py                      # Start interactive UI
│   ├── deploy.sh                         # One-click deployment
│   ├── stop_agents.sh                    # Stop all agents
│   ├── setup_aws.sh                      # AWS infrastructure setup
│   ├── setup_databricks.sh               # Databricks configuration
│   └── run_tests.sh                      # Run all tests
│
├── ⚙️ config/                            # Configuration files
│   ├── nova.yaml                         # NOVA agent config
│   ├── axiom.yaml                        # AXIOM agent config
│   ├── sentinel.yaml                     # SENTINEL agent config
│   ├── nexus.yaml                        # NEXUS agent config
│   ├── prometheus.yaml                   # PROMETHEUS agent config
│   └── logging.yaml                      # Logging configuration
│
├── 🖼️ images/                            # README images & logos
│   ├── header-banner.png                 # Main banner
│   ├── nova-icon.png                     # NOVA agent icon
│   ├── axiom-icon.png                    # AXIOM agent icon
│   ├── sentinel-icon.png                 # SENTINEL agent icon
│   ├── nexus-icon.png                    # NEXUS agent icon
│   ├── prometheus-icon.png               # PROMETHEUS agent icon
│   ├── architecture-diagram.png          # System architecture
│   └── deployment-flow.png               # Deployment workflow
│
├── 📋 examples/                          # Example code & tutorials
│   ├── quickstart.py                     # Quick start example
│   ├── deploy_service.py                 # Service deployment example
│   ├── create_pipeline.py                # Data pipeline example
│   ├── run_tests.py                      # Testing example
│   └── notebooks/                        # Jupyter notebooks
│       ├── 01_getting_started.ipynb
│       ├── 02_deploying_services.ipynb
│       ├── 03_data_pipelines.ipynb
│       └── 04_monitoring.ipynb
│
└── 🔄 .github/                           # GitHub configuration
    ├── workflows/                        # GitHub Actions
    │   ├── deploy.yml                    # Deployment pipeline
    │   ├── test.yml                      # Testing pipeline
    │   ├── security-scan.yml             # Security scanning
    │   └── docs.yml                      # Documentation generation
    ├── ISSUE_TEMPLATE/
    │   ├── bug_report.md
    │   └── feature_request.md
    ├── PULL_REQUEST_TEMPLATE.md
    └── CODEOWNERS
```

## 🎯 Key Directories Explained

### `/agents`
Contains the 5 autonomous AI agents. Each agent is a FastAPI microservice that can be deployed independently.

### `/infrastructure`
All Infrastructure as Code (IaC) for AWS deployment:
- **Docker**: Container definitions for each service
- **Kubernetes**: K8s manifests for EKS deployment
- **Terraform**: AWS infrastructure provisioning

### `/docs`
Comprehensive documentation for developers, operators, and architects.

### `/tests`
Complete test coverage:
- **unit**: Individual component tests
- **integration**: Service interaction tests
- **e2e**: Full workflow tests

### `/scripts`
Utility scripts for common operations:
- Deployment automation
- Development environment setup
- Testing runners

### `/config`
Configuration files for each agent and system component.

### `/images`
Assets for README and documentation (logos, diagrams, screenshots).

### `/examples`
Working code examples and tutorials for learning the platform.

## 🚀 Quick Navigation

| Need to... | Go to... |
|------------|----------|
| Deploy the platform | `/scripts/deploy.sh` |
| Understand architecture | `/docs/architecture.md` |
| Configure AWS | `/docs/aws-integration.md` |
| Add a new agent | `/agents/` and `/docs/agent-patterns.md` |
| Run tests | `/scripts/run_tests.sh` |
| View API docs | `/docs/api-reference.md` |
| Troubleshoot issues | `/docs/troubleshooting.md` |

## 📝 File Naming Conventions

- **Python files**: `snake_case.py`
- **Configuration**: `kebab-case.yaml`
- **Documentation**: `kebab-case.md`
- **Scripts**: `snake_case.sh`
- **Tests**: `test_*.py`

## 🔍 Finding Things

```bash
# Find all agent code
find agents/ -name "*.py"

# Find all Kubernetes configs
find infrastructure/kubernetes/ -name "*.yaml"

# Find all tests
find tests/ -name "test_*.py"

# Find all documentation
find docs/ -name "*.md"
```

## 📦 What Goes Where?

| File Type | Location |
|-----------|----------|
| Agent code | `/agents/` |
| Infrastructure code | `/infrastructure/` |
| Documentation | `/docs/` |
| Tests | `/tests/` |
| Scripts | `/scripts/` |
| Configuration | `/config/` |
| Examples | `/examples/` |
| Images/Assets | `/images/` |
| CI/CD | `/.github/workflows/` |

---

This structure follows industry best practices for:
- ✅ Microservices architecture
- ✅ Infrastructure as Code
- ✅ Test-Driven Development
- ✅ Documentation-First approach
- ✅ GitOps workflows
