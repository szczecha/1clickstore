WAREHOUSE_CREATE_MUTATION = """
mutation createWarehouse($input: WarehouseCreateInput!) {
  createWarehouse(input: $input) {
    errors {
      message
      field
      code
    }
    warehouse {
      id
      name
      slug
      isPrivate
      shippingZones(first: 10) {
        edges {
          node {
            id
            countries {
              code
            }
          }
        }
      }
      clickAndCollectOption
    }
  }
}
"""

CHANNEL_CREATE_MUTATION = """
mutation ChannelCreate($input: ChannelCreateInput!) {
  channelCreate(input: $input) {
    errors {
      field
      message
      code
    }
    channel {
      id
      name
      slug
      currencyCode
      defaultCountry {
        code
      }
      warehouses {
        id
        slug
        shippingZones(first: 10) {
          edges {
            node {
              id
            }
          }
        }
      }
      stockSettings {
        allocationStrategy
      }
      isActive
      orderSettings {
        markAsPaidStrategy
        automaticallyConfirmAllNewOrders
        allowUnpaidOrders
        automaticallyConfirmAllNewOrders
        expireOrdersAfter
        deleteExpiredOrdersAfter
      }
      checkoutSettings {
        automaticallyCompleteFullyPaidCheckouts
      }
    }
  }
}
"""

SHIPPING_ZONE_CREATE_MUTATION = """
mutation createShipping($input: ShippingZoneCreateInput!) {
  shippingZoneCreate(input: $input) {
    errors {
      field
      code
      message
    }
    shippingZone {
      id
      name
    }
  }
}
"""


SHIPPING_PRICE_CREATE_MUTATION = """
mutation CreateShippingRate($input: ShippingPriceInput!) {
  shippingPriceCreate(input: $input) {
    errors {
      field
      code
      message
    }
    shippingZone {
      id
    }
    shippingMethod {
      id
    }
  }
}
"""


SHIPPING_METHOD_CHANNEL_LISTING_MUTATION = """
mutation ShippingMethodChannelListingUpdate(
    $id: ID!, $input: ShippingMethodChannelListingInput!
) {
  shippingMethodChannelListingUpdate(id: $id, input: $input) {
    errors {
      field
      code
      message
    }
    shippingMethod {
        id
        channelListings {
            minimumOrderPrice {
                amount
            }
            maximumOrderPrice {
                amount
            }
            price {
                amount
            }
            channel {
                id
            }
        }
    }
  }
}
"""


SHOP_SETTING_UPDATE_MUTATION = """
mutation ShopSettingsUpdate($input: ShopSettingsInput!) {
  shopSettingsUpdate(input: $input) {
    errors {
      field
      message
      code
    }
    shop {
      enableAccountConfirmationByEmail
      fulfillmentAutoApprove
      fulfillmentAllowUnpaid
    }
  }
}
"""


TAX_CONFIGURATIONS_QUERY = """
query TaxConfigurationsList($first: Int) {
  taxConfigurations(first: $first) {
    edges {
      node {
        id
        channel {
          id
          slug
        }
        displayGrossPrices
        pricesEnteredWithTax
        chargeTaxes
        taxCalculationStrategy
      }
    }
  }
}

"""


TAX_CONFIGURATION_UPDATE_MUTATION = """
mutation TaxConfigurationUpdate($id: ID!, $input: TaxConfigurationUpdateInput!) {
  taxConfigurationUpdate(id: $id, input: $input) {
    errors {
      field
      code
      message
      countryCodes
    }
    taxConfiguration {
      id
      channel {
        id
        name
      }
      displayGrossPrices
      pricesEnteredWithTax
      chargeTaxes
      taxCalculationStrategy
      countries {
        country {
          code
        }
        chargeTaxes
        taxCalculationStrategy
        displayGrossPrices
      }
    }
  }
}
"""


TAX_CLASS_CREATE_MUTATION = """
mutation TaxClassCreate($input: TaxClassCreateInput!) {
  taxClassCreate(input: $input) {
    errors {
      field
      message
      code
    }
    taxClass {
      id
      name
      countries {
        country {
          code
        }
        rate
        taxClass {
          id
        }
      }
    }
  }
}
"""


TAX_CLASS_UPDATE_MUTATION = """
mutation taxClassUpdate($id:ID!, $input:TaxClassUpdateInput!){
  taxClassUpdate(id:$id, input:$input) {
    errors {
        field
        message
    }
    taxClass {
        id
        countries {
            country {
                code
                }
                rate
                taxClass { id }
            }
        }
  }
}
"""


TAX_COUNTRY_CONFIGURATION_UPDATE_MUTATION = """
mutation TaxCountryConfigurationUpdate($countryCode: CountryCode!,
 $updateTaxClassRates: [TaxClassRateInput!]!) {
  taxCountryConfigurationUpdate(
    countryCode: $countryCode
    updateTaxClassRates: $updateTaxClassRates
  ) {
    errors {
      code
      field
      message
      taxClassIds
    }
    taxCountryConfiguration {
      country{
        code
      }
      taxClassCountryRates{
        country{
          code
        }
        rate
        taxClass{
          id
        }
      }
    }
  }
}
"""


SHIPPING_PRICE_UPDATE_MUTATION = """
mutation ShippingPriceUpdate($id: ID!, $input: ShippingPriceInput!) {
  shippingPriceUpdate(id: $id, input: $input) {
    errors {
      field
      message
      code
    }
    shippingMethod {
      id
      name
      type
      taxClass {
        id
      }
      channelListings {
        channel {
          id
          slug
        }
        price {
          amount
        }
        maximumOrderPrice {
          amount
        }
        minimumOrderPrice {
          amount
        }
      }
      maximumDeliveryDays
      postalCodeRules {
        id
        start
        end
        inclusionType
      }
      excludedProducts(first: 10) {
        edges {
          node {
            id
          }
        }
      }
    }
  }
}
"""

WAREHOUSE_DELETE_MUTATION = """
mutation WarehouseDelete($id: ID!) {
  deleteWarehouse(id: $id) {
    errors {
      code
      field
      message
    }
  }
}
"""

CHANNEL_DELETE_MUTATION = """
mutation ChannelDelete($id: ID!) {
  channelDelete(id: $id) {
    errors {
      code
      field
      message
    }
  }
}
"""

SHIPPING_ZONE_DELETE_MUTATION = """
mutation DeleteShippingZone($id: ID!) {
  shippingZoneDelete(id: $id) {
    errors {
      code
      field
      message
    }
  }
}
"""

SHIPPING_PRICE_DELETE_MUTATION = """
mutation DeleteShippingRate($id: ID!) {
  shippingPriceDelete(id: $id) {
    errors {
      field
      code
      message
    }
  }
}
"""
