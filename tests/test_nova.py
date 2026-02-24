"""
Unit Tests for NOVA - Infrastructure Agent
Tests AWS integrations, Kubernetes deployments, and SLI validation
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from agents.nova import InfrastructureAgent, ServiceDeploymentRequest


class TestNovaAgent:
    """Test suite for NOVA infrastructure agent"""
    
    @pytest.fixture
    def agent(self):
        """Create test agent instance"""
        with patch('agents.nova.boto3'):
            return InfrastructureAgent()
    
    @pytest.fixture
    def deployment_request(self):
        """Sample deployment request"""
        return ServiceDeploymentRequest(
            service_name="test-service",
            service_type="llm",
            requirements={"model": "claude-sonnet-4-20250514"},
            scaling_config={"min_replicas": 2, "max_replicas": 10}
        )
    
    @pytest.mark.asyncio
    async def test_agent_initialization(self, agent):
        """Test agent initializes AWS clients correctly"""
        assert agent.aws_region == 'us-east-1'
        assert agent.aws_ecr_client is not None
        assert agent.aws_eks_client is not None
        assert agent.aws_apigateway is not None
        assert agent.aws_cloudwatch is not None
    
    @pytest.mark.asyncio
    async def test_generate_service_code(self, agent, deployment_request):
        """Test AI service code generation"""
        with patch.object(agent.claude.messages, 'create', new_callable=AsyncMock) as mock_create:
            mock_create.return_value.content = [Mock(text="# Generated FastAPI code")]
            
            code = await agent._generate_service_code(deployment_request)
            
            assert "# Generated FastAPI code" in code
            mock_create.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_build_container_image_ecr(self, agent):
        """Test AWS ECR authentication and image build"""
        mock_ecr_response = {
            'authorizationData': [{
                'authorizationToken': 'test-token',
                'proxyEndpoint': 'https://123456789.dkr.ecr.us-east-1.amazonaws.com'
            }]
        }
        
        agent.aws_ecr_client.get_authorization_token.return_value = mock_ecr_response
        
        with patch.object(agent.claude.messages, 'create', new_callable=AsyncMock) as mock_create:
            mock_create.return_value.content = [Mock(text="FROM python:3.11")]
            
            image_name = await agent._build_container_image("test-service", "test-code")
            
            assert "dkr.ecr.us-east-1.amazonaws.com" in image_name
            agent.aws_ecr_client.get_authorization_token.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_configure_api_gateway(self, agent, deployment_request):
        """Test AWS API Gateway configuration"""
        mock_api_response = {
            'ApiId': 'test-api-123',
            'ApiEndpoint': 'https://test-api.execute-api.us-east-1.amazonaws.com'
        }
        
        agent.aws_apigateway.create_api.return_value = mock_api_response
        
        gateway_config = await agent._configure_api_gateway(deployment_request)
        
        assert gateway_config['aws_api_id'] == 'test-api-123'
        assert 'execute-api' in gateway_config['aws_api_endpoint']
    
    @pytest.mark.asyncio
    async def test_setup_monitoring_cloudwatch(self, agent):
        """Test AWS CloudWatch metrics and alarms"""
        await agent._setup_monitoring("test-service")
        
        # Verify CloudWatch calls
        agent.aws_cloudwatch.put_metric_data.assert_called()
        agent.aws_cloudwatch.put_metric_alarm.assert_called()
        
        # Check alarm has correct SLI threshold (p99 < 200ms)
        alarm_call = agent.aws_cloudwatch.put_metric_alarm.call_args
        assert alarm_call[1]['Threshold'] == 200.0
    
    @pytest.mark.asyncio
    async def test_validate_slis(self, agent):
        """Test SLI validation (p99 < 200ms requirement)"""
        validation = await agent._validate_slis("test-service")
        
        assert 'p99_latency_ms' in validation
        assert validation['p99_latency_ms'] < 200  # Must meet JD requirement
        assert validation['passed'] is True
    
    @pytest.mark.asyncio
    async def test_full_deployment_workflow(self, agent, deployment_request):
        """Test complete deployment workflow"""
        with patch.object(agent, '_generate_service_code', new_callable=AsyncMock) as mock_gen:
            with patch.object(agent, '_build_container_image', new_callable=AsyncMock) as mock_build:
                with patch.object(agent, '_create_k8s_deployment', new_callable=AsyncMock) as mock_k8s:
                    with patch.object(agent, '_configure_api_gateway', new_callable=AsyncMock) as mock_gw:
                        with patch.object(agent, '_setup_monitoring', new_callable=AsyncMock) as mock_mon:
                            with patch.object(agent, '_validate_slis', new_callable=AsyncMock) as mock_val:
                                
                                mock_gen.return_value = "service code"
                                mock_build.return_value = "image:latest"
                                mock_gw.return_value = {"api_id": "test"}
                                mock_val.return_value = {"passed": True, "p99_latency_ms": 185}
                                
                                result = await agent.deploy_ai_service(deployment_request)
                                
                                assert result['status'] == 'deployed'
                                assert result['service_name'] == 'test-service'
                                assert result['sli_validation']['passed'] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
