from utils import (
    WAREHOUSE_CREATE_MUTATION,
    CHANNEL_CREATE_MUTATION,
    CHANNEL_DELETE_MUTATION,
    WAREHOUSE_DELETE_MUTATION,
    SHIPPING_ZONE_CREATE_MUTATION,
    SHIPPING_ZONE_DELETE_MUTATION,
    SHIPPING_PRICE_CREATE_MUTATION,
    SHIPPING_METHOD_CHANNEL_LISTING_MUTATION,
    SHIPPING_PRICE_DELETE_MUTATION,
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

    def create_shipping_zone(self, input_data):
        """
        Create a new shipping zone with the specified input data.
        """
        variables = {"input": input_data}

        result = self.api_client.execute_query_with_retries(
            SHIPPING_ZONE_CREATE_MUTATION, variables
        )
        data = result.get("data", {}).get("shippingZoneCreate", {})
        errors = data.get("errors", [])
        if errors:
            raise ValueError(f"Failed to create shipping zone: {errors}")

        shipping_zone = data.get("shippingZone")
        return shipping_zone

    def create_shipping_method(self, input_data):
        """
        Create a new shipping price with the specified input data.
        """
        variables = input_data

        result = self.api_client.execute_query_with_retries(
            SHIPPING_PRICE_CREATE_MUTATION, variables
        )

        data = result.get("data", {}).get("shippingPriceCreate", {})
        errors = data.get("errors", [])
        if errors:
            raise ValueError(f"Failed to create shipping price: {errors}")

        shipping_method = data.get("shippingMethod")
        return shipping_method

    def update_shipping_method_channel_listing(self, input_data):
        variables = input_data

        result = self.api_client.execute_query_with_retries(
            SHIPPING_METHOD_CHANNEL_LISTING_MUTATION, variables
        )

        data = result.get("data", {}).get("shippingMethodChannelListingUpdate", {})
        errors = data.get("errors", [])
        if errors:
            raise ValueError(
                f"Failed to update shipping method channel listing: {errors}"
            )

        shipping_method_channel_listing = data.get("shippingMethod")
        return shipping_method_channel_listing

    def remove_item(self, mutation, item_type, input_data):
        """
        Remove an item using the provided mutation. Skips deletion if the item is not found.
        """
        variables = input_data

        result = self.api_client.execute_query_with_retries(mutation, variables)
        print(f"Response from {item_type} deletion:", result)

        data_key = f"{item_type}Delete"
        data = result.get("data", {}).get(data_key, {})
        errors = data.get("errors", [])
        if errors:
            for error in errors:
                if error.get("code") == "NOT_FOUND":
                    print(
                        f"{item_type.capitalize()} not found. Skipping deletion. Details: {error}"
                    )
                    return None
            raise ValueError(f"Failed to delete {item_type}: {errors}")

        return data.get(item_type)

    def remove_channel(self, input_data):
        """
        Remove a channel. Skips if not found.
        """
        return self.remove_item(CHANNEL_DELETE_MUTATION, "channel", input_data)

    def remove_warehouse(self, input_data):
        """
        Remove a warehouse. Skips if not found.
        """
        return self.remove_item(WAREHOUSE_DELETE_MUTATION, "warehouse", input_data)

    def remove_shipping_zone(self, input_data):
        """
        Remove a shipping zone. Skips if not found.
        """
        return self.remove_item(
            SHIPPING_ZONE_DELETE_MUTATION, "shippingZone", input_data
        )

    def remove_shipping_method(self, input_data):
        """
        Remove a shipping method. Skips if not found.
        """
        return self.remove_item(
            SHIPPING_PRICE_DELETE_MUTATION, "shippingMethod", input_data
        )
