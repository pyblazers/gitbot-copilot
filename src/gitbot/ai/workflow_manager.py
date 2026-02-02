"""Workflow management using LangChain."""

import logging
from typing import Dict, List, Optional, Any

from gitbot.config.settings import Settings

logger = logging.getLogger(__name__)


class WorkflowManager:
    """Workflow Manager for handling complex workflows using LangChain."""

    def __init__(self, settings: Settings):
        """Initialize Workflow Manager.
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.workflows = {}
        self._initialize_langchain()

    def _initialize_langchain(self):
        """Initialize LangChain components."""
        try:
            from langchain.chains import LLMChain
            from langchain.prompts import PromptTemplate
            from langchain_openai import ChatOpenAI
            
            if self.settings.openai_api_key:
                self.llm = ChatOpenAI(
                    api_key=self.settings.openai_api_key,
                    model=self.settings.openai_model,
                    temperature=0.7
                )
                logger.info("LangChain initialized with OpenAI")
            else:
                logger.warning("No API key provided for LangChain")
                self.llm = None
        except ImportError:
            logger.warning("LangChain not installed. Install with: pip install langchain langchain-openai")
            self.llm = None
        except Exception as e:
            logger.error(f"Failed to initialize LangChain: {e}")
            self.llm = None

    async def create_workflow(self, workflow_name: str, steps: List[Dict]) -> Dict:
        """Create a new workflow.
        
        Args:
            workflow_name: Name of the workflow
            steps: List of workflow steps
            
        Returns:
            dict: Workflow configuration
        """
        workflow = {
            "name": workflow_name,
            "steps": steps,
            "status": "created"
        }
        self.workflows[workflow_name] = workflow
        logger.info(f"Workflow '{workflow_name}' created with {len(steps)} steps")
        return workflow

    async def execute_workflow(self, workflow_name: str, context: Dict = None) -> Dict:
        """Execute a workflow.
        
        Args:
            workflow_name: Name of the workflow to execute
            context: Execution context
            
        Returns:
            dict: Execution results
        """
        if workflow_name not in self.workflows:
            return {"error": f"Workflow '{workflow_name}' not found"}
        
        workflow = self.workflows[workflow_name]
        results = []
        
        for step in workflow["steps"]:
            step_result = await self._execute_step(step, context)
            results.append(step_result)
            
            # Update context with step results
            if context is None:
                context = {}
            context[f"step_{step['name']}_result"] = step_result
        
        return {
            "workflow": workflow_name,
            "results": results,
            "status": "completed"
        }

    async def _execute_step(self, step: Dict, context: Dict = None) -> Dict:
        """Execute a single workflow step.
        
        Args:
            step: Step configuration
            context: Execution context
            
        Returns:
            dict: Step execution result
        """
        step_type = step.get("type", "unknown")
        
        if step_type == "assign":
            return await self._assign_task(step, context)
        elif step_type == "analyze":
            return await self._analyze_content(step, context)
        elif step_type == "route":
            return await self._route_request(step, context)
        else:
            logger.warning(f"Unknown step type: {step_type}")
            return {"error": f"Unknown step type: {step_type}"}

    async def _assign_task(self, step: Dict, context: Dict = None) -> Dict:
        """Assign task based on workflow step.
        
        Args:
            step: Step configuration
            context: Execution context
            
        Returns:
            dict: Assignment result
        """
        if not self.llm:
            return {"error": "LangChain not initialized"}
        
        try:
            from langchain.chains import LLMChain
            from langchain.prompts import PromptTemplate
            
            template = """Based on the following information, determine the best assignee:
            
            Task: {task}
            Context: {context}
            Available assignees: {assignees}
            
            Provide the assignee name and reasoning."""
            
            prompt = PromptTemplate(
                input_variables=["task", "context", "assignees"],
                template=template
            )
            
            chain = LLMChain(llm=self.llm, prompt=prompt)
            
            result = await chain.arun(
                task=step.get("task", ""),
                context=str(context),
                assignees=step.get("assignees", [])
            )
            
            return {"assignee": result, "status": "assigned"}
        except Exception as e:
            logger.error(f"Failed to assign task: {e}")
            return {"error": str(e)}

    async def _analyze_content(self, step: Dict, context: Dict = None) -> Dict:
        """Analyze content using LangChain.
        
        Args:
            step: Step configuration
            context: Execution context
            
        Returns:
            dict: Analysis result
        """
        if not self.llm:
            return {"error": "LangChain not initialized"}
        
        try:
            from langchain.chains import LLMChain
            from langchain.prompts import PromptTemplate
            
            template = """Analyze the following content:
            
            {content}
            
            Provide: {analysis_type}"""
            
            prompt = PromptTemplate(
                input_variables=["content", "analysis_type"],
                template=template
            )
            
            chain = LLMChain(llm=self.llm, prompt=prompt)
            
            result = await chain.arun(
                content=step.get("content", ""),
                analysis_type=step.get("analysis_type", "general analysis")
            )
            
            return {"analysis": result, "status": "completed"}
        except Exception as e:
            logger.error(f"Failed to analyze content: {e}")
            return {"error": str(e)}

    async def _route_request(self, step: Dict, context: Dict = None) -> Dict:
        """Route request based on workflow step.
        
        Args:
            step: Step configuration
            context: Execution context
            
        Returns:
            dict: Routing result
        """
        if not self.llm:
            return {"error": "LangChain not initialized"}
        
        try:
            from langchain.chains import LLMChain
            from langchain.prompts import PromptTemplate
            
            template = """Determine the best route for this request:
            
            Request: {request}
            Context: {context}
            Available routes: {routes}
            
            Provide the route and reasoning."""
            
            prompt = PromptTemplate(
                input_variables=["request", "context", "routes"],
                template=template
            )
            
            chain = LLMChain(llm=self.llm, prompt=prompt)
            
            result = await chain.arun(
                request=step.get("request", ""),
                context=str(context),
                routes=step.get("routes", [])
            )
            
            return {"route": result, "status": "routed"}
        except Exception as e:
            logger.error(f"Failed to route request: {e}")
            return {"error": str(e)}

    async def link_queries(self, queries: List[str]) -> Dict:
        """Link multiple queries together.
        
        Args:
            queries: List of related queries
            
        Returns:
            dict: Linked query results
        """
        if not self.llm:
            return {"error": "LangChain not initialized"}
        
        try:
            from langchain.chains import LLMChain
            from langchain.prompts import PromptTemplate
            
            template = """Given these related queries, provide a comprehensive response:
            
            {queries}
            
            Synthesize the information and provide a unified answer."""
            
            prompt = PromptTemplate(
                input_variables=["queries"],
                template=template
            )
            
            chain = LLMChain(llm=self.llm, prompt=prompt)
            
            queries_text = "\n".join([f"{i+1}. {q}" for i, q in enumerate(queries)])
            result = await chain.arun(queries=queries_text)
            
            return {"linked_response": result, "status": "completed"}
        except Exception as e:
            logger.error(f"Failed to link queries: {e}")
            return {"error": str(e)}
