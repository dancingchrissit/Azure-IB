
from __future__ import print_function

import datetime
import time

from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import ibConnection, message


class ExecutionHandler(object):
    """
    Handles order execution via the Interactive Brokers API
    """

    def __init__(
        self, ib_conn, currency="USD"
    ):
        # initialize
        self.ib_conn = ib_conn
        # self.order_routing = order_routing
        self.currency = currency
        self.fill_dict = {}

        self.order_id = self.create_initial_order_id()
        self.register_handlers()

    def _error_handler(self, msg):
        # error handling
        print("Server Error: %s" % msg)

    def _reply_handler(self, msg):
        # Handle open order orderId processing
        if msg.typeName == "openOrder" and \
            msg.orderId == self.order_id and \
            not self.fill_dict.has_key(msg.orderId):
            self.create_fill_dict_entry(msg)
        # Handle Fills
        if msg.typeName == "orderStatus" and \
            msg.status == "Filled" and \
            self.fill_dict[msg.orderId]["filled"] == False:
            self.create_fill(msg)
        print("Server Response: %s, %s\n" % (msg.typeName, msg))

    def create_initial_order_id(self):
        return 1
# not necessary, besides your using another connection
#    def register_handlers(self):
#
#        # Assign the error handling function
#        self.tws_conn.register(self._error_handler, 'Error')
#
#        # Assign all of the server reply messages
#        self.tws_conn.registerAll(self._reply_handler)

    def create_contract(self, symbol, sec_type, exch, prim_exch, curr):
        """Create a Contract object defining what will
        be purchased, at which exchange and in which currency.

        symbol - The ticker symbol for the contract
        sec_type - The security type for the contract ('FUT' = Future)
        exch - The exchange to carry out the contract on
        prim_exch - The primary exchange to carry out the contract on
        curr - The currency in which to purchase the contract"""
        contract = Contract()
        contract.m_symbol = symbol
        contract.m_secType = sec_type
        contract.m_exchange = exch
        contract.m_primaryExch = prim_exch
        contract.m_currency = curr
        return contract

    def create_order(self, order_type, quantity, action):
        """Create an Order object (Market/Limit) to go long/short.

        order_type - 'MKT', 'LMT' for Market or Limit orders
        quantity - Integral number of assets to order
        action - 'BUY' or 'SELL'"""
        order = Order()
        order.m_orderType = order_type
        order.m_totalQuantity = quantity
        order.m_action = action
        return order

    def create_trailing_order(self, quantity, action, trail_threshold, parent_id):
        """
        Creates the trailing order
        quantity: quantity of contracts to trade
        action: "BUY" or "SELL"
        trail_threshold: amount to trail the price by
        parent_id: order ID of the parent fill

        return: order object
        """
        order = Order()
        order.m_orderType = "TRAIL"  # "TRAIL" = Trailing Stop "TRAIL LIMIT" = Trailing stop limit
        order.m_totalQuantity = quantity
        order.m_auxPrice = trail_threshold  # trailing amount
        order.m_action = action
        order.m_triggerMethod = 8  # midpoint method
        order.m_parentId = parent_id

        return order

    def create_fill_dict_entry(self, msg):
        """
        Creates an entry in the Fill Dictionary that lists
        orderIds and provides security information. This is
        needed for the event-driven behaviour of the IB
        server message behaviour.
        """
        self.fill_dict[msg.orderId] = {
            "symbol": msg.contract.m_symbol,
            "exchange": msg.contract.m_exchange,
            "direction": msg.order.m_action,
            "filled": False
        }

    def create_fill(self, msg):
        """
        Places a fill in the fill dictionary
        """
        fd = self.fill_dict[msg.orderId]

        # Check for fill and no duplicates
        self.fill_dict[msg.orderId]["filled"] = True


    def execute_order(self, ib_contract, ib_order):
        """
        Execute the order through IB API
        """
        # send the order to IB
        self.ib_conn.placeOrder(
            self.order_id, ib_contract, ib_order
        )


        # order goes through!
        time.sleep(1)

        # Increment the order ID
        self.order_id += 1

    def save_pickle(self):
        state = {"order_id": self.order_id,
                "fill_dict": self.fill_dict

        }

    def load_pickle(self):
        pass

        def __register_data_handlers(self,
                                     tick_event_handler,
                                     universal_event_handler):


# register Ib connection
model_conn= ibConnection()
model_conn.create(port=4001, clientId=130)

#registeringg handlers
model_conn.registerAll(universal_event_handler)
model_conn.unregister(universal_event_handler,
                     ib_message_type.tickSize,
                     ib_message_type.tickPrice,
                     ib_message_type.tickString,
                     ib_message_type.tickGeneric,
                     ib_message_type.tickOptionComputation)
model_conn.register(tick_event_handler,
                   ib_message_type.tickPrice,
                   ib_message_type.tickSize,
                   ib_message_type.orderStatus)

#event handler
def __event_handler(self, msg):
    if msg.typeName == datatype.MSG_TYPE_HISTORICAL_DATA:

        self.__on_historical_data(msg)


    elif msg.typeName == datatype.MSG_TYPE_UPDATE_PORTFOLIO:

        self.__on_portfolio_update(msg)

    elif msg.typeName == datatype.MSG_TYPE_MANAGED_ACCOUNTS:
        pass

    # self.account_code = msg.accountsList

    elif msg.typeName == datatype.MSG_TYPE_NEXT_ORDER_ID:
        self.order_id = msg.orderId

    elif msg.typeName == datatype.MSG_ORDER_STATUS:
        if msg.filled != 0:
            self.monitor.update_trade(float(msg.lastFillPrice))
            print
            msg.LastFillPrice + "filled"
            print
            msg.id

    else:
        print
        msg