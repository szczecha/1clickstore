from dotenv import load_dotenv
import os
from api_client import APIClient
from store_setup import StoreSetup


def main():
    load_dotenv()

    API_URL = os.getenv("API_URL")
    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")

    api_client = APIClient(API_URL, EMAIL, PASSWORD)
    api_client.login()

    # Initialize the StoreSetup with the API client
    store_setup = StoreSetup(api_client)

    # Clean previous data
    # consider search by slug and delete
    channel_id_to_remove = "Q2hhbm5lbDo0Mg=="
    warehouse_id_to_remove = (
        "V2FyZWhvdXNlOjQxMWIyZjRhLWQ3MzctNDIxOC04MjRmLTgyZDM5ZmNjNzFhMg=="
    )

    remove_channel_input = {"id": channel_id_to_remove}
    store_setup.remove_channel(remove_channel_input)
    print(f"Channel removed: {channel_id_to_remove}")

    remove_warehouse_input = {"id": warehouse_id_to_remove}
    store_setup.remove_warehouse(remove_warehouse_input)
    print(f"Warehouse removed: {warehouse_id_to_remove}")

    # Define warehouse input
    warehouse_input = {
        "name": "Main Warehouse",
        "slug": "main-warehouse",
        "email": "warehouse@example.com",
        "address": {
            "country": "US",
            "countryArea": "AL",
            "city": "New Sandraburgh",
            "postalCode": "35969",
            "companyName": "Green Ltd",
            "streetAddress1": "302 Matthew Glen",
            "streetAddress2": "",
        },
        "shippingZones": [],
    }

    # Create the warehouse
    warehouse = store_setup.create_warehouse(warehouse_input)
    warehouse_id = warehouse["id"]
    print(f"Warehouse created: {warehouse_id}")

    # Define channel input
    channel_input = {
        "name": "Test Channel",
        "slug": "test-channel",
        "defaultCountry": "US",
        "currencyCode": "USD",
        "isActive": True,
        "addShippingZones": [],
        "addWarehouses": [warehouse_id],
        "stockSettings": {"allocationStrategy": "PRIORITIZE_SORTING_ORDER"},
        "paymentSettings": {"defaultTransactionFlowStrategy": "AUTHORIZATION"},
        "orderSettings": {
            "allowUnpaidOrders": True,
            "automaticallyConfirmAllNewOrders": True,
            "automaticallyFulfillNonShippableGiftCard": True,
            "expireOrdersAfter": 1440,
            "deleteExpiredOrdersAfter": 120,
            "markAsPaidStrategy": "TRANSACTION_FLOW",
            "includeDraftOrderInVoucherUsage": True,
        },
        "checkoutSettings": {
            "automaticallyCompleteFullyPaidCheckouts": True,
        },
    }

    # Create the channel
    channel = store_setup.create_channel(channel_input)
    channel_id = channel["id"]
    print(f"Channel created: {channel_id}")


if __name__ == "__main__":
    main()
