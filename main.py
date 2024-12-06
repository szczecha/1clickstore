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
    warehouse_id_to_remove = (
        "V2FyZWhvdXNlOjQ4MTRmZDYyLWI0MTktNGQyOS05ZTE1LTM1Y2MzNDcyMGMzMA=="
    )
    channel_id_to_remove = "Q2hhbm5lbDo1MA=="
    shipping_zone_id_to_remove = "U2hpcHBpbmdab25lOjE1"
    shipping_method_id_to_remove = "U2hpcHBpbmdNZXRob2RUeXBlOjI3"

    remove_channel_input = {"id": channel_id_to_remove}
    store_setup.remove_channel(remove_channel_input)
    print(f"Channel removed: {channel_id_to_remove}")

    remove_warehouse_input = {"id": warehouse_id_to_remove}
    store_setup.remove_warehouse(remove_warehouse_input)
    print(f"Warehouse removed: {warehouse_id_to_remove}")

    remove_shipping_zone_input = {"id": shipping_zone_id_to_remove}
    store_setup.remove_shipping_zone(remove_shipping_zone_input)
    print(f"Shipping zone removed: {shipping_zone_id_to_remove}")

    remove_shipping_method_input = {"id": shipping_method_id_to_remove}
    store_setup.remove_shipping_method(remove_shipping_method_input)
    print(f"Shipping method removed: {remove_shipping_method_input['id']}\n")

    # Create the warehouse
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

    warehouse = store_setup.create_warehouse(warehouse_input)
    warehouse_id = warehouse["id"]
    print(f"Warehouse created: {warehouse_id}")

    # Create the channel
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
    channel = store_setup.create_channel(channel_input)
    channel_id = channel["id"]
    print(f"Channel created: {channel_id}")

    # Create the shipping zone
    shipping_zone_input = {
        "name": "US - USA Shipping",
        "description": "",
        "countries": ["US"],
        "default": False,
        "addWarehouses": [warehouse_id],
        "addChannels": [channel_id],
    }
    shipping_zone = store_setup.create_shipping_zone(shipping_zone_input)
    shipping_zone_id = shipping_zone["id"]
    print(f"Shipping zone created: {shipping_zone_id}")

    # Create the shipping method
    shipping_price_input = {
        "input": {
            "shippingZone": shipping_zone_id,
            "name": "USPS Priority Mail",
            "type": "PRICE",
            "description": None,
            "maximumDeliveryDays": None,
            "minimumDeliveryDays": None,
            "addPostalCodeRules": [],
            "deletePostalCodeRules": [],
            "inclusionType": "EXCLUDE",
            "taxClass": "",
        }
    }

    shipping_method = store_setup.create_shipping_method(shipping_price_input)
    shipping_method_id = shipping_method["id"]
    print(f"Shipping method created: {shipping_method_id}")

    # Update shipping method channels and prices
    shipping_method_price_input = {
        "id": shipping_method_id,
        "input": {
            "addChannels": [
                {
                    "channelId": channel_id,
                    "price": 19.99,
                    "minimumOrderPrice": 0,
                    "maximumOrderPrice": 666,
                }
            ],
            "removeChannels": [],
        },
    }
    store_setup.update_shipping_method_channel_listing(shipping_method_price_input)
    print(f"Shipping pricing updated")


if __name__ == "__main__":
    main()
