from decimal import Decimal
import logging
from typing import List, Dict, Any
from hummingbot.core.clock import Clock
from hummingbot.logger import HummingbotLogger
from hummingbot.strategy.strategy_py_base import StrategyPyBase
from hummingbot.strategy.market_trading_pair_tuple import MarketTradingPairTuple
NaN = float("nan")
s_decimal_zero = Decimal(0)
s_decimal_nan = Decimal("NaN")
lms_logger = None


class CodejamStrategy(StrategyPyBase):

    @classmethod
    def logger(cls) -> HummingbotLogger:
        global lms_logger
        if lms_logger is None:
            lms_logger = logging.getLogger(__name__)
        return lms_logger

    def __init__(self,
                 market_infos: List[MarketTradingPairTuple],
                 parameters: Dict[str, Any]
                 ):
        super().__init__()
        self._market_infos = market_infos
        self._parameters = parameters
        self._ready_to_trade = False
        self._exchange = market_infos[0].market
        self.add_markets([self._exchange])

    @property
    def active_orders(self):
        limit_orders = self.order_tracker.active_limit_orders
        return [o[1] for o in limit_orders]

    def tick(self, timestamp: float):
        """
        Clock tick entry point, is run every second (on normal tick setting).
        :param timestamp: current tick timestamp
        """
        if not self._ready_to_trade:
            # Check if there are restored orders, they should be canceled before strategy starts.
            self._ready_to_trade = self._exchange.ready
            if not self._exchange.ready:
                self.logger().warning(f"{self._exchange.name} is not ready. Please wait...")
                return
            else:
                self.logger().info(f"{self._exchange.name} is ready. Trading started.")

        self._last_timestamp = timestamp

    async def format_status(self) -> str:
        if not self._ready_to_trade:
            return "Market connectors are not ready."
        return "to be implemented"

    def start(self, clock: Clock, timestamp: float):
        pass

    def stop(self, clock: Clock):
        pass