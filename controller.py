from app.agent.graph import create_agent_graph
from app.agent.database import Database
from app.agent.tool_executor import execute_tool
from app.agent.response_formatter import format_tool_response



class AgentController:


    def __init__(self):

        self.agent = create_agent_graph()

        self.database = Database()

        self.state = None

        self.activity_log = []

        self.pending_action = None


        # ----------------------------------
        # Requirement 9 : Execution Limits
        # ----------------------------------

        # Maximum number of tool executions
        # during one user request

        self.max_tool_calls = 5

        self.tool_calls = 0


        # Maximum stored conversation history

        self.max_history = 30




    # ----------------------------
    # Activity Logger
    # ----------------------------

    def log_activity(self, message):

        self.activity_log.append(message)



    def get_activity_log(self):

        return self.activity_log





    # ----------------------------
    # Main Runner
    # ----------------------------

    def run(self, message: str):


        original_message = message.strip()

        message = message.lower().strip()



        self.activity_log = []



        self.log_activity(
            f"User request received: {original_message}"
        )





        # ----------------------------
        # APPROVAL YES
        # ----------------------------

        if message in ["yes", "y"]:


            self.log_activity(
                "Approval response detected"
            )


            if self.pending_action:


                tool_name = self.pending_action.get(
                    "tool"
                )


                arguments = self.pending_action.get(
                    "arguments",
                    {}
                )



                print(
                    "EXECUTING APPROVED TOOL:",
                    tool_name,
                    arguments
                )



                # skip_approval=True: the user just approved this
                # exact action, so tool_executor must not re-trigger
                # the approval gate.

                result = execute_tool(
                    tool_name,
                    arguments,
                    skip_approval=True
                )



                # Only clear pending_action once the tool actually
                # ran successfully. If it failed for some other
                # reason (bad arguments, tool bug, etc.), keep the
                # pending action so we don't lose approval state
                # on a real failure.

                if result.get("success"):

                    self.pending_action = None


                    self.log_activity(
                        "Approved action executed"
                    )


                else:

                    self.log_activity(
                        "Approved action execution failed"
                    )



                return format_tool_response(
                    result
                )



            return "No pending approval action found."







        # ----------------------------
        # APPROVAL NO
        # ----------------------------

        if message in ["no", "n"]:


            self.pending_action = None


            self.log_activity(
                "Action cancelled"
            )


            return "Action cancelled."








        # ----------------------------
        # SIMPLE TASK COMMANDS
        # ----------------------------


        if message.startswith("add task:"):


            task = original_message[9:].strip()


            self.database.add(

                {

                    "title": task,

                    "completed": False,

                    "note": ""

                }

            )


            return f"Task added successfully: {task}"








        if message == "show tasks":


            tasks = self.database.get_all()



            if not tasks:

                return "No tasks found."



            output = []



            for task in tasks:


                output.append(

                    f"{task['id']}. "
                    f"{task['title']} - "
                    f"{task.get('status','Pending')}"

                )



            return "\n".join(output)









        # ----------------------------
        # LANGGRAPH EXECUTION
        # ----------------------------


        self.log_activity(
            "Routing request to LangGraph"
        )




        if self.state:


            self.state["messages"].append(

                {

                    "role": "user",

                    "content": original_message

                }

            )



        else:


            self.state = {


                "messages": [

                    {

                        "role": "user",

                        "content": original_message

                    }

                ],


                "pending_action": {},


                "approved": False,


                "approval_required": False

            }






        result = self.agent.invoke(
            self.state
        )



        self.state = result



        print(
            "LANGGRAPH RESULT:",
            result
        )





        # Save approval action

        if result.get("pending_action"):


            self.pending_action = result["pending_action"]



            print(
                "SAVED PENDING ACTION:",
                self.pending_action
            )





        response = result["messages"][-1]



        if isinstance(response, dict):


            return response.get(
                "content",
                "No response generated."
            )



        return str(response)