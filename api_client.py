import requests
import time


class APIClient:
    MUTATION_LOGIN = """
    mutation login($email: String!, $password: String!) {
      tokenCreate(email: $email, password: $password) {
        token
        refreshToken
        errors {
          field
          message
        }
      }
    }
    """

    MUTATION_TOKEN_REFRESH = """
    mutation token_refresh($refreshToken: String!) {
      tokenRefresh(refreshToken: $refreshToken) {
        token
      }
    }
    """

    def __init__(self, base_url, email, password):
        self.base_url = base_url
        self.email = email
        self.password = password
        self.token = None
        self.refresh_token = None
        self.token_expiry = None
        self.expiration_time = 270

    def is_token_expired(self):
        """Check if the token is expired."""
        return time.time() >= self.token_expiry

    def execute_graphql_query(self, query, variables):
        response = requests.post(
            f"{self.base_url}",
            json={"query": query, "variables": variables},
            headers={"Authorization": f"Bearer {self.token}"} if self.token else {},
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def execute_query_with_retries(self, query, variables):
        """Executes the query, refreshing the token if necessary."""
        try:
            if self.is_token_expired():
                self.refresh_user_token()
            return self.execute_graphql_query(query, variables)
        except Exception as e:
            if "Signature has expired" in str(e):
                print("Token expired. Refreshing and retrying...")
                self.refresh_user_token()
                return self.execute_graphql_query(query, variables)
            raise

    def login(self):
        variables = {"email": self.email, "password": self.password}
        result = self.execute_graphql_query(self.MUTATION_LOGIN, variables)

        data = result.get("data", {}).get("tokenCreate", {})
        if data.get("errors"):
            raise ValueError(f"Login failed: {data['errors']}")

        self.token = data["token"]
        self.refresh_token = data["refreshToken"]
        self.token_expiry = time.time() + self.expiration_time

    def refresh_user_token(self):
        if not self.refresh_token:
            self.login()
            return

        variables = {"refreshToken": self.refresh_token}
        result = self.execute_graphql_query(self.MUTATION_TOKEN_REFRESH, variables)

        data = result.get("data", {}).get("tokenRefresh", {})
        if "token" in data:
            self.token = data["token"]
            self.token_expiry = time.time() + self.expiration_time
        else:
            self.login()
