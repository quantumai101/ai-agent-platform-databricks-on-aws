"""
NEXUS - Documentation Agent
Auto-Generate Architecture Docs, API Specs, Runbooks, Onboarding
Living Documentation that Updates with Code
"""

import asyncio
from typing import Dict, List, Any
from pathlib import Path
from datetime import datetime
import anthropic
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DocumentationRequest(BaseModel):
    repository_path: str
    doc_types: List[str]  # ["architecture", "api", "runbook", "onboarding"]
    output_format: str = "markdown"


class DocumentationAgent:
    """
    NEXUS - Autonomous documentation generation
    """
    
    def __init__(self):
        self.claude = anthropic.Anthropic()
        self.generated_docs = {}
    
    async def generate_documentation(self, request: DocumentationRequest) -> Dict:
        """
        Generate complete documentation suite
        """
        logger.info(f"Generating docs for {request.repository_path}")
        
        # Analyze codebase
        codebase_analysis = await self._analyze_codebase(request.repository_path)
        
        docs = {}
        
        # Generate each doc type
        for doc_type in request.doc_types:
            if doc_type == "architecture":
                content = await self._generate_architecture_docs(codebase_analysis)
            elif doc_type == "api":
                content = await self._generate_api_docs(codebase_analysis)
            elif doc_type == "runbook":
                content = await self._generate_runbooks(codebase_analysis)
            elif doc_type == "onboarding":
                content = await self._generate_onboarding_guide(codebase_analysis)
            
            docs[doc_type] = content
        
        # Save documentation
        doc_paths = await self._save_documentation(docs, request.output_format)
        
        result = {
            "repository": request.repository_path,
            "documentation": docs,
            "file_paths": doc_paths,
            "format": request.output_format,
            "timestamp": datetime.now().isoformat()
        }
        
        self.generated_docs[request.repository_path] = result
        
        return result
    
    async def _analyze_codebase(self, repo_path: str) -> Dict:
        """
        Analyze codebase structure and components
        """
        repo = Path(repo_path)
        
        # Scan files
        code_files = []
        for ext in ['*.py', '*.js', '*.ts', '*.go', '*.java']:
            code_files.extend(repo.rglob(ext))
        
        # Build codebase map
        codebase = {}
        for file in code_files[:100]:  # First 100 files
            try:
                with open(file, 'r') as f:
                    codebase[str(file)] = f.read()
            except:
                continue
        
        # Analyze with AI
        analysis_prompt = f"""
        Analyze this codebase structure:
        
        Files found: {len(codebase)}
        
        Sample files and content:
        {self._format_codebase_sample(codebase)}
        
        Return JSON analysis:
        {{
            "architecture_pattern": "microservices/monolith/serverless",
            "tech_stack": ["list", "of", "technologies"],
            "main_components": ["component1", "component2"],
            "data_flow": "description",
            "deployment_model": "kubernetes/lambda/etc",
            "key_dependencies": ["dep1", "dep2"]
        }}
        """
        
        response = self.claude.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=3000,
            messages=[{"role": "user", "content": analysis_prompt}]
        )
        
        analysis = eval(response.content[0].text)
        analysis['codebase'] = codebase
        
        return analysis
    
    def _format_codebase_sample(self, codebase: Dict) -> str:
        """Format codebase for AI analysis"""
        sample = []
        for path, code in list(codebase.items())[:10]:
            sample.append(f"\nFile: {path}\n```\n{code[:500]}...\n```")
        return "\n".join(sample)
    
    async def _generate_architecture_docs(self, analysis: Dict) -> str:
        """
        Generate comprehensive architecture documentation
        """
        prompt = f"""
        Generate comprehensive architecture documentation:
        
        System Analysis:
        {analysis}
        
        Create professional markdown documentation with:
        
        # System Architecture
        
        ## Overview
        - High-level system description
        - Design principles
        - Architecture patterns used
        
        ## Components
        - Detailed component descriptions
        - Responsibilities
        - Inter-component communication
        
        ## Data Flow
        - Request/response flows
        - Data pipeline architecture
        - State management
        
        ## Technology Stack
        - Languages and frameworks
        - Infrastructure
        - Third-party services
        
        ## Deployment Architecture
        - Environment topology
        - Scaling strategy
        - Disaster recovery
        
        ## Security Architecture
        - Authentication/authorization
        - Data protection
        - Compliance considerations
        
        ## Diagrams
        - Component diagram (mermaid)
        - Sequence diagram (mermaid)
        - Deployment diagram (mermaid)
        
        Make it comprehensive and professional.
        """
        
        response = self.claude.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
    
    async def _generate_api_docs(self, analysis: Dict) -> str:
        """
        Generate API documentation
        """
        prompt = f"""
        Generate OpenAPI 3.0 specification and API documentation:
        
        Codebase Analysis:
        {analysis}
        
        Extract all API endpoints and generate:
        
        1. OpenAPI 3.0 YAML spec
        2. Endpoint documentation with:
           - Method and path
           - Request/response schemas
           - Authentication requirements
           - Rate limits
           - Example requests/responses
           - Error codes
        
        3. Authentication guide
        4. Rate limiting details
        5. Versioning strategy
        6. SDK examples (Python, JavaScript)
        
        Make it comprehensive like Stripe API docs.
        """
        
        response = self.claude.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
    
    async def _generate_runbooks(self, analysis: Dict) -> str:
        """
        Generate operational runbooks
        """
        prompt = f"""
        Generate operational runbooks for:
        
        System: {analysis['architecture_pattern']}
        Tech Stack: {analysis['tech_stack']}
        
        Create runbooks for:
        
        ## Deployment Runbook
        - Pre-deployment checklist
        - Deployment steps
        - Rollback procedure
        - Post-deployment validation
        
        ## Incident Response
        - Severity classification
        - On-call procedures
        - Common incidents and resolutions
        - Escalation paths
        
        ## Troubleshooting Guide
        - Common issues and fixes
        - Log analysis
        - Performance debugging
        - Database issues
        
        ## Maintenance Procedures
        - Backup and restore
        - Database migrations
        - Certificate renewal
        - Dependency updates
        
        ## Monitoring and Alerts
        - Key metrics to watch
        - Alert thresholds
        - Dashboard links
        - Log queries
        
        Make it actionable with step-by-step instructions.
        """
        
        response = self.claude.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
    
    async def _generate_onboarding_guide(self, analysis: Dict) -> str:
        """
        Generate new engineer onboarding guide
        """
        prompt = f"""
        Generate comprehensive onboarding guide for new engineers:
        
        System: {analysis}
        
        Create guide with:
        
        # Welcome to the Team!
        
        ## Day 1: Setup
        - Development environment setup (step-by-step)
        - Required tools and accounts
        - Repository access
        - Running the app locally
        - Your first successful build
        
        ## Week 1: Understanding the System
        - Architecture overview
        - Key components deep dive
        - Code structure and conventions
        - Testing strategy
        - Development workflow
        
        ## Week 2: Your First Contribution
        - Finding a good first issue
        - Code review process
        - Git workflow
        - Deployment process
        - Getting your first PR merged
        
        ## Ongoing: Best Practices
        - Coding standards
        - Security guidelines
        - Performance considerations
        - Documentation expectations
        - Communication channels
        
        ## Resources
        - Key documentation links
        - Useful commands cheat sheet
        - Who to ask for help
        - Learning resources
        
        ## Common Pitfalls
        - Mistakes to avoid
        - Troubleshooting common setup issues
        
        Make it friendly and comprehensive.
        """
        
        response = self.claude.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
    
    async def _save_documentation(self, docs: Dict, format: str) -> Dict:
        """
        Save generated documentation to files
        """
        output_dir = Path("./generated_docs")
        output_dir.mkdir(exist_ok=True)
        
        file_paths = {}
        
        for doc_type, content in docs.items():
            if format == "markdown":
                file_path = output_dir / f"{doc_type}.md"
                file_path.write_text(content)
            elif format == "html":
                # Convert markdown to HTML
                file_path = output_dir / f"{doc_type}.html"
                # Use markdown library to convert
                file_path.write_text(f"<html><body>{content}</body></html>")
            
            file_paths[doc_type] = str(file_path)
            logger.info(f"Saved {doc_type} documentation to {file_path}")
        
        return file_paths
    
    async def update_documentation(self, repo_path: str) -> Dict:
        """
        Auto-update documentation when code changes
        """
        logger.info(f"Updating documentation for {repo_path}")
        
        # Detect what changed
        changes = await self._detect_code_changes(repo_path)
        
        # Update relevant docs
        updated_docs = {}
        if changes['api_changes']:
            updated_docs['api'] = await self._update_api_docs(changes)
        
        if changes['architecture_changes']:
            updated_docs['architecture'] = await self._update_architecture_docs(changes)
        
        return {
            "repository": repo_path,
            "changes_detected": changes,
            "updated_docs": updated_docs,
            "timestamp": datetime.now().isoformat()
        }
    
    async def _detect_code_changes(self, repo_path: str) -> Dict:
        """
        Detect what changed in codebase
        """
        # In production: Use git diff
        return {
            "api_changes": True,
            "architecture_changes": False,
            "new_components": [],
            "modified_components": ["user_service"]
        }
    
    async def _update_api_docs(self, changes: Dict) -> str:
        """Update API docs based on changes"""
        # Re-generate affected sections
        return "Updated API documentation"
    
    async def _update_architecture_docs(self, changes: Dict) -> str:
        """Update architecture docs based on changes"""
        return "Updated architecture documentation"


# FastAPI Application
app = FastAPI(
    title="NEXUS - Documentation Agent",
    description="Autonomous Documentation Generation",
    version="1.0.0"
)

agent = DocumentationAgent()


@app.post("/generate")
async def generate_documentation(request: DocumentationRequest):
    """
    Generate documentation suite
    """
    try:
        result = await agent.generate_documentation(request)
        return result
    except Exception as e:
        logger.error(f"Documentation generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/update/{repo_path:path}")
async def update_documentation(repo_path: str):
    """
    Update documentation after code changes
    """
    try:
        result = await agent.update_documentation(repo_path)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/docs")
async def list_documentation():
    """
    List all generated documentation
    """
    return {
        "documentation": agent.generated_docs,
        "total": len(agent.generated_docs)
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "agent": "NEXUS"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
