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

assistant_ruleset = Ruleset(
    name="Assistant",
    rules=[
           
    ]
)

json_ruleset = Ruleset(
    name='json_ruleset',
    rules=[
        Rule(
            "Respond in plain text only with valid JSON objects that have the following keys: response, continue_chatting, score, distribution."
            ),
        Rule(
            "Never wrap your response with ```"
            ),
        Rule(
            "The 'response' value should be a string that can be safely converted to markdown format.  Use '\\n' for new lines."
            ),
        Rule(
            "'score' is initially 50. Use the users desired budget to decide a score between 50 and 100"
            ),
        Rule(
            "'distribution' should be a float between 0.33 and 0.67. If the user intends to use the computer for graphics card intensive activities, 'distribution' should be increased. if the user intends to use the computer forcpu intensive activities, score should be decreased."
            ),
        Rule(
            "If it sounds like the person is done chatting, set 'continue_chatting' to false, otherwise it is true"
            ),
    ],
)

# Create a subclass for the Agent
class MyAgent(Agent):

    def respond (self, user_input):
        agent_response = agent.run(user_input)
        data = json.loads(agent_response.output_task.output.value)
        response = data["response"]
        continue_chatting = data["continue_chatting"]
        score = data["score"]
        distribution = data["distribution"]

        formatted_response = Markdown(response)

        rprint("")
        rprint(Panel.fit(
            formatted_response,
            width=80,
            style=Style(color="light_sea_green"),
        ))
        rprint("")

        return [continue_chatting, score, distribution]

# Create the agent
agent = MyAgent(
    rulesets=[assistant_ruleset, json_ruleset],
    tools=[CalculatorTool()]
    )

# Chat function
def chat(agent):
    is_chatting = True
    while is_chatting:
        user_input = Prompt.ask("[grey50]Chat with the assistant")
        chat_output = agent.respond(user_input)
        is_chatting = chat_output[0]

# Introduce the agent
agent.respond("Introduce yourself to the user.")

# Run the agent
chat(agent)