#!/bin/bash

# AI Agent Platform - One-Click Deployment Script
# Deploys all 5 autonomous agents

set -e

echo "========================================="
echo "AI AGENT PLATFORM - ONE-CLICK DEPLOYMENT"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0;no'

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt --quiet

# Create necessary directories
mkdir -p logs data config

# Set up environment
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file...${NC}"
    cp .env.example .env
    echo "⚠️  Please update .env with your credentials"
fi

# Start agents in background
echo -e "${YELLOW}Starting AI agents...${NC}"

# Start orchestrator
echo "Starting Orchestrator..."
python orchestrator.py > logs/orchestrator.log 2>&1 &
ORCH_PID=$!
sleep 2

# Start individual agents
agents=("nova" "axiom" "sentinel" "nexus" "prometheus")
ports=(8001 8002 8003 8004 8005)

for i in "${!agents[@]}"; do
    agent="${agents[$i]}"
    port="${ports[$i]}"
    echo "Starting ${agent^^} agent on port $port..."
    python agents/${agent}.py > logs/${agent}.log 2>&1 &
    sleep 1
done

echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}✓ ALL AGENTS DEPLOYED SUCCESSFULLY!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo "📊 Dashboard: http://localhost:8000"
echo ""
echo "🤖 Agent Endpoints:"
echo "  - NOVA (Infrastructure):     http://localhost:8001"
echo "  - AXIOM (Data Pipeline):     http://localhost:8002"
echo "  - SENTINEL (Testing):        http://localhost:8003"
echo "  - NEXUS (Documentation):     http://localhost:8004"
echo "  - PROMETHEUS (Optimization): http://localhost:8005"
echo ""
echo "📝 Logs are available in ./logs/"
echo ""
echo "To stop all agents: ./scripts/stop_agents.sh"
echo ""

# Save PIDs
echo $ORCH_PID > .pids
ps aux | grep "python agents/" | grep -v grep | awk '{print $2}' >> .pids

# Open browser
if command -v xdg-open > /dev/null; then
    xdg-open http://localhost:8000
elif command -v open > /dev/null; then
    open http://localhost:8000
fi

echo "Press Ctrl+C to stop all agents"

# Wait
wait
