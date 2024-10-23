from dotenv import load_dotenv
import json

from griptape.structures import Agent
from griptape.rules import Rule, Ruleset
from griptape.tools import CalculatorTool

from rich import print as rprint
from rich.markdown import Markdown
from rich.panel import Panel
from rich.style import Style
from rich.prompt import Prompt

load_dotenv()  # Load your environment

#creating rulesets for agents
json_ruleset = Ruleset(
    name='json_ruleset',
    rules=[
        Rule(
            "Respond in plain text only with valid JSON objects that have the following keys: response, continue_chatting."
            ),
        Rule(
            "Never wrap your response with ```"
            ),
        Rule(
            "The 'response' value should be a string that can be safely converted to markdown format.  Use '\\n' for new lines."
            ),
        Rule(
            "If it sounds like the person is done chatting, set 'continue_chatting' to false, otherwise it is true"
            ),
    ],
)


parts_ruleset = Ruleset(
    name='parts_ruleset',
    rules=[
        Rule(
            "Respond in plain text only with valid JSON objects that have the following keys: score, distribution."
            ),
        Rule(
            "Never wrap your response with ```"
            ),
        Rule(
            "'score' is initially 50. Use the users desired budget to decide a score between 50 and 100"
            ),
        Rule(
            "'distribution' should be a float between 0.33 and 0.67."
            ),
    ],
)

question_ruleset = Ruleset(
    name='question_ruleset',
    rules=[
        Rule(
            "Respond in plain text only with valid JSON objects that have the following keys: question, continue_chatting."
            ),
        Rule(
            "Never wrap your response with ```"
            ),
        Rule(
            "The 'question' value should be a string that can be safely converted to markdown format.  Use '\\n' for new lines."
            ),
        Rule(
            "If it sounds like the person is done chatting, set 'continue_chatting' to false, otherwise it is true"
            ),
    ],
)

reader_ruleset = Ruleset(
    name='reader_ruleset',
    rules=[
        Rule(
            "Respond in plain text only with valid JSON objects that have the following keys: summary, continue_chatting."
            ),
        Rule(
            "Never wrap your response with ```"
            ),
        Rule(
            "The 'summary' value should be a string that can be safely converted to markdown format.  Use '\\n' for new lines."
            ),
        Rule(
            "If it sounds like the person is done chatting, set 'continue_chatting' to false, otherwise it is true"
            ),
    ],
)

# Create subclasses for the Agents
class ChatAgent(Agent):
    def respond(self, user_input):
        agent_response = self.run(user_input)
        data = json.loads(agent_response.output_task.output.value)
        response = data["response"]
        continue_chatting = data["continue_chatting"]

        formatted_response = Markdown(response)

        print("")
        rprint(
            Panel.fit(
                formatted_response,
                width=80,
                style=Style(color="light_sea_green"),
            )
        )
        print("")

        return continue_chatting


class QuestionerAgent(Agent):
        
    def question (self, topic):
        agent_response = self.run(topic)
        formatted_response = Markdown(agent_response)

        rprint("")
        rprint(Panel.fit(
            formatted_response,
            width=80,
            style=Style(color="light_sea_green"),
        ))
        rprint("")

        return
    
    def ask(self, topic):
        agent_response = self.run(f"Ask a relevant question to gather more information about: {topic}")
        data = json.loads(agent_response.output_task.output.value)
        question = data["question"]
        continue_chatting = data["continue_chatting"]

        formatted_question = Markdown(question)

        print("")
        rprint(
            Panel.fit(
                formatted_question,
                width=80,
                style=Style(color="light_sea_green"),
            )
        )
        print("")

        return continue_chatting
    
    
# Creating the agents
chat_agent = ChatAgent(
    rulesets=[json_ruleset],
    )

questioner_agent = QuestionerAgent(
    tools=[CalculatorTool()],
    )

# Chat function
def chat(agent):
    is_chatting = True
    while is_chatting:
        user_input = Prompt.ask("[grey50]Chat with the assistant")
        is_chatting = agent.respond(user_input)

# Question function
def question_session(agent):
    is_chatting = True
    while is_chatting:
        agent.ask()

def question(agent, topic):
    is_questioning = True
    while is_questioning:
        is_questioning = agent.ask(topic)
        if is_questioning:
            answer = Prompt.ask("[grey50]Your answer")
            # You can process the answer here if needed

# Introduce the agent
chat_agent.respond("Introduce yourself to the user.")

# Run the agent
chat(chat_agent)