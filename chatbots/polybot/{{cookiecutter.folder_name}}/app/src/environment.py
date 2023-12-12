import os
from .prettyprint import prettyprint as print, MessageType as mt


class Environment:
    def __init__(self, args: dict = {}) -> None:
        """
        Initializes an instance of the Environment class.
        """

        # If the environment is local, use the local environment variables.
        self.is_local = self._is_local()

        print(
            f"Environment is {'local' if self.is_local else 'Halerium'}", msg_type=mt.INFO
        )

        if not self.is_local:
            self.base_url = self.get_base_url()
            self.tenant = self.get_tenant()
            self.workspace = self.get_workspace()
            self.runner_id = self.get_runner_id()
            self.runner_token = self.get_runner_token()

        elif self.is_local and args:
            self.base_url = args.get("base_url")
            self.tenant = args.get("tenant")
            self.workspace = args.get("workspace")
            self.runner_id = args.get("runner_id")
            self.runner_token = args.get("runner_token")
        else:
            print(
                "Local environment requires arguments. Please provide a dict containing\n- base_url\n- tenant\n- workspace\n- runner_id\n- runner_token",
                msg_type=mt.ERROR,
            )
            raise Exception("Missing arguments for local environment.")

    def _is_local(self) -> bool:
        """
        Returns True if the environment is local.

        Returns:
        bool: True if the environment is local.
        """
        return os.getenv("HALERIUM_BASE_URL") is None

    def get_base_url(self) -> str:
        """
        Returns the base URL for the environment.

        Returns:
        str: The base URL for the environment.
        """
        if self.is_local:
            return "127.0.0.1"
        else:
            return os.getenv("HALERIUM_BASE_URL")

    def get_tenant(self) -> str:
        """
        Returns the tenant key for the environment.

        Returns:
        str: The tenant key for the environment.
        """
        return os.getenv("HALERIUM_TENANT_KEY")

    def get_workspace(self) -> str:
        """
        Returns the project ID for the environment.

        Returns:
        str: The project ID for the environment.
        """
        return os.getenv("HALERIUM_PROJECT_ID")

    def get_runner_id(self) -> str:
        """
        Returns the runner ID for the environment.

        Returns:
        str: The runner ID for the environment.
        """
        return os.getenv("HALERIUM_ID")

    def get_runner_token(self) -> str:
        """
        Returns the runner token for the environment.

        Returns:
        str: The runner token for the environment.
        """
        return os.getenv("HALERIUM_TOKEN")

    def get_prompt_server_url(self) -> str:
        """
        Returns the prompt server URL for the environment.

        Returns:
        str: The prompt server URL for the environment.
        """
        return f"{self.base_url}/api/tenants/{self.tenant}/projects/{self.workspace}/runners/{self.runner_id}/models"

    def build_prompt_server_payload(self, messages: list, model_id: str) -> dict:
        """
        Builds a payload for the prompt server.

        Args:
        messages (list): A list of messages to include in the payload.
        model_id (str): The ID of the model to use for the payload.

        Returns:
        dict: The payload for the prompt server.
        """
        return {
            "model_id": model_id,
            "body": {"messages": messages},
            "tenant": self.tenant,
            "workspace": self.workspace,
        }

    def build_embedding_payload(self, text_chunks: str, model_id: str) -> dict:
        """
        Builds a payload for the prompt server.

        Args:
        text (str): The text to embed.
        model_id (str): The ID of the model to use for the payload.

        Returns:
        dict: The payload for the prompt server.
        """
        return {
            "model_id": model_id,
            "body": {"text_chunks": text_chunks},
            "tenant": self.tenant,
            "workspace": self.workspace,
        }

    def build_prompt_server_headers(self) -> dict:
        """
        Builds headers for the prompt server.

        Returns:
        dict: The headers for the prompt server.
        """
        return {
            "halerium-runner-token": self.runner_token,
            "X-Accel-Buffering": "no"
            }


    def get_app_url(self, port: int | str = None) -> str:
        """
        Returns the app URL for the environment.

        Args:
        port (int | str, optional): The port to use for the URL. Defaults to None.

        Returns:
        str: The app URL for the environment.
        """
        if not self.is_local:
            return f'{self.base_url}/apps/{self.runner_id}{"/" + str(port) if port else "/"}'
        else:
            return f'127.0.0.1{":" + str(port) if port else ":8501"}'

    def get_websocket_url(self, port: int | str = None) -> str:
        """
        Returns the websocket URL for the environment.

        Args:
        port (int | str, optional): The port to use for the URL. Defaults to None.

        Returns:
        str: The websocket URL for the environment.
        """
        if not self.is_local:
            return f'ws{self.base_url.replace("https", "")}/apps/{self.runner_id}{"/" + str(port) + "/" if port else "/"}'
        else:
            return f'ws://127.0.0.1{":" + str(port) + "/" if port else ":8501/"}'


if __name__ == "__main__":
    env = Environment(True)

    print(env.base_url)
    print(env.get_app_url(8501))
    print(env.get_websocket_url(8501))
