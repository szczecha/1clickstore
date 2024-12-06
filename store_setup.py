from utils import (
    WAREHOUSE_CREATE_MUTATION,
    CHANNEL_CREATE_MUTATION,
    CHANNEL_DELETE_MUTATION,
    WAREHOUSE_DELETE_MUTATION,
)


class StoreSetup:
    def __init__(self, api_client):
        """
        Initialize the StoreSetup with an API client.
        """
        self.api_client = api_client

    def create_warehouse(self, input_data):
        """
        Create a new warehouse with the specified input data.
        """
        variables = {"input": input_data}

        result = self.api_client.execute_query_with_retries(
            WAREHOUSE_CREATE_MUTATION, variables
        )

        data = result.get("data", {}).get("createWarehouse", {})

        errors = data.get("errors", [])
        if errors:
            raise ValueError(f"Failed to create warehouse: {errors}")

        warehouse = data.get("warehouse")

        return warehouse

    def create_channel(self, input_data):
        """
        Create a new channel with the specified input data.
        """
        variables = {"input": input_data}

        result = self.api_client.execute_query_with_retries(
            CHANNEL_CREATE_MUTATION, variables
        )

        data = result.get("data", {}).get("channelCreate", {})
        errors = data.get("errors", [])
        if errors:
            raise ValueError(f"Failed to create channel: {errors}")

        channel = data.get("channel")
        return channel

    def remove_channel(self, input_data):
        """
        Create a new channel with the specified input data.
        """
        variables = input_data

        result = self.api_client.execute_query_with_retries(
            CHANNEL_DELETE_MUTATION, variables
        )

        data = result.get("data", {}).get("channelDelete", {})
        errors = data.get("errors", [])
        if errors:
            raise ValueError(f"Failed to delete channel: {errors}")

        channel = data.get("channel")
        return channel

    def remove_warehouse(self, input_data):
        """
        Create a new channel with the specified input data.
        """
        variables = input_data

        result = self.api_client.execute_query_with_retries(
            WAREHOUSE_DELETE_MUTATION, variables
        )

        data = result.get("data", {}).get("warehouseDelete", {})
        errors = data.get("errors", [])
        if errors:
            raise ValueError(f"Failed to delete warehouse: {errors}")

        warehouse = data.get("warehouse")
        return warehouse
