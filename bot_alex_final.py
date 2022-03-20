#!/usr/bin/env python3
# ~~~~~==============   HOW TO RUN   ==============~~~~~
# 1) Configure things in CONFIGURATION section
# 2) Change permissions: chmod +x bot.py
# 3) Run in loop: while true; do ./bot.py --test prod-like; sleep 1; done
# real exchange)))) Run in loop: while true; do ./bot.py --prod; sleep 1; done

import argparse
from collections import deque
from enum import Enum
import time
import socket
import json

# ~~~~~============== CONFIGURATION  ==============~~~~~
# Replace "REPLACEME" with your team name!
team_name = "PEACOCK"

# ~~~~~============== MAIN LOOP ==============~~~~~

# You should put your code here! We provide some starter code as an example,
# but feel free to change/remove/edit/update any of it as you'd like. If you
# have any questions about the starter code, or what to do next, please ask us!
#
# To help you get started, the sample code below tries to buy BOND for a low
# price, and it prints the current prices for VALE every second. The sample
# code is intended to be a working example, but it needs some improvement
# before it will start making good trades!


def main():
    args = parse_arguments()

    exchange = ExchangeConnection(args=args)

    # Store and print the "hello" message received from the exchange. This
    # contains useful information about your positions. Normally you start with
    # all positions at zero, but if you reconnect during a round, you might
    # have already bought/sold symbols and have non-zero positions.
    hello_message = exchange.read_message()
    print("First message from exchange:", hello_message)

    global id 
    id = 1

    # Set up some variables to track the bid and ask price of a symbol. Right
    # now this doesn't track much information, but it's enough to get a sense
    # of the VALE market.
    positions = {"BOND": 0,"VALE": 0,"VALBZ": 0,"GS": 0,"MS": 0,"WFC": 0,"XLF": 0}

    vale_bid_price, vale_ask_price = None, None
    vale_last_print_time = time.time()

    valbz_bid_price, valbz_ask_price = None, None
    valbz_last_print_time = time.time()

    bond_bid_price, bond_ask_price = None, None
    bond_last_print_time = time.time()

    gs_bid_price, gs_ask_price = None, None
    gs_last_print_time = time.time()

    ms_bid_price, ms_ask_price = None, None
    ms_last_print_time = time.time()

    wfc_bid_price, wfc_ask_price = None, None
    wfc_last_print_time = time.time()

    xlf_bid_price, xlf_ask_price = None, None
    xlf_last_print_time = time.time()

    # ========================= helper methods =================================
    # example: exchange_add("VALE","BUY",425,5)
    def exchange_add(sym,direction,prc,count):
        global id
        id+=1
        if(direction=="BUY"):
            exchange.send_add_message(order_id=id,symbol=sym,dir=Dir.BUY,price=prc,size=count)
        if(direction=="SELL"):
            exchange.send_add_message(order_id=id,symbol=sym,dir=Dir.SELL,price=prc,size=count)

    def exchange_convert(sym,direction,count):
        global id
        id+=1
        if(direction=="BUY"):
            exchange.send_convert_message(order_id=id, symbol= sym, dir=Dir.BUY, size=count)
        if(direction=="SELL"):
            exchange.send_convert_message(order_id=id, symbol= sym, dir=Dir.SELL, size=count)

    # Here is the main loop of the program. It will continue to read and
    # process messages in a loop until a "close" message is received. You
    # should write to code handle more types of messages (and not just print
    # the message). Feel free to modify any of the starter code below.
    #
    # Note: a common mistake people make is to call write_message() at least
    # once for every read_message() response.
    #
    # Every message sent to the exchange generates at least one response
    # message. Sending a message in response to every exchange message will
    # cause a feedback loop where your bot's messages will quickly be
    # rate-limited and ignored. Please, don't do that!
    while True:
        message = exchange.read_message()

        # Some of the message types below happen infrequently and contain
        # important information to help you understand what your bot is doing,
        # so they are printed in full. We recommend not always printing every
        # message because it can be a lot of information to read. Instead, let
        # your code handle the messages and just print the information
        # important for you!
        if message["type"] == "close":
            print("The round has ended")
            break
        elif message["type"] == "error":
            print(message)
        elif message["type"] == "reject":
            print(message)
            #exchange.send_convert_message(type="cancel", order_id=message["id"])
        elif message["type"] == "fill":
             print(message)

        # UPDATE POSITIONS
        elif message["type"] == "fill":
            sym=message["symbol"]
            if message["dir"] == "BUY":
                positions[sym] += message["size"]
            else:
                positions[sym] -= message["size"]
        
        elif message["type"] == "book":
             # ===================== begin Trading XLF = (3 * BOND + 2 * GS + 3 * MS + 2 * WFC)/10 =====================================================================
            #   ==================== Prices from GS ===========================
            if message["symbol"] == "GS":
                def best_price(side):
                    if message[side]:
                        return message[side][0][0]

                gs_bid_price = best_price("buy")
                gs_ask_price = best_price("sell")

                now = time.time()

                if now > gs_last_print_time + 1:
                    gs_last_print_time = now
                    # print(
                    #     {
                    #         "gs_bid_price": gs_bid_price,
                    #         "gs_ask_price": gs_ask_price,
                    #     }
                    # )
            # ==================== Prices from MS ===========================
            if message["symbol"] == "MS":
                def best_price(side):
                    if message[side]:
                        return message[side][0][0]

                ms_bid_price = best_price("buy")
                ms_ask_price = best_price("sell")

                now = time.time()

                if now > ms_last_print_time + 1:
                    ms_last_print_time = now
                    # print(
                    #     {
                    #         "ms_bid_price": ms_bid_price,
                    #         "ms_ask_price": ms_ask_price,
                    #     }
                    # )
            # ==================== Prices from WFC ===========================
            if message["symbol"] == "WFC":
                def best_price(side):
                    if message[side]:
                        return message[side][0][0]

                wfc_bid_price = best_price("buy")
                wfc_ask_price = best_price("sell")

                now = time.time()

                if now > wfc_last_print_time + 1:
                    wfc_last_print_time = now
                    # print(
                    #     {
                    #         "wfc_bid_price": wfc_bid_price,
                    #         "wfc_ask_price": wfc_ask_price,
                    #     }
                    # )

            # ==================== Trading XLF ===========================
            elif message["symbol"] == "XLF":

                def best_price(side):
                    if message[side]:
                        return message[side][0][0]

                xlf_bid_price = best_price("buy")
                xlf_ask_price = best_price("sell")

                now = time.time()

                if now > xlf_last_print_time + 1:
                    xlf_last_print_time = now
            #         print(
            #             {
            #                 "xlf_bid_price": xlf_bid_price,
            #                 "xlf_ask_price": xlf_ask_price,
            #             }
            #         )

                if (gs_bid_price == None or gs_ask_price == None or 
                    ms_bid_price == None or ms_ask_price == None or
                    wfc_bid_price == None or wfc_ask_price == None):
                    continue

                # buy if xlf buy price is < gs, ms, wfc, bond sell price
                xlf_fair_val = (3 * 1000 + 2 * gs_ask_price + 3 * ms_ask_price + 2 * wfc_ask_price)/10

                def buy_xlf(): # 2 at a time
                  exchange_add("XLF","BUY",xlf_bid_price+1,2)
                  print("bought XLF at price ", xlf_bid_price + 1)

                def sell_xlf_constituents():
                  exchange_add("GS","SELL",gs_bid_price+1,4)
                  print("sold GS at price ", gs_bid_price + 1)
                  exchange_add("MS","SELL",ms_ask_price,6)
                  print("sold MS at price ", ms_ask_price)
                  exchange_add("WFC","SELL",wfc_ask_price,4)
                  print("sold WFC at price ", wfc_ask_price)
                  exchange_add("BOND","SELL",bond_ask_price,6)
                  print("sold BOND at price ", bond_ask_price)


                if ((xlf_bid_price + 1) < xlf_fair_val) or (((xlf_bid_price + 1) == xlf_fair_val and positions["XLF"] <= -90)):
                        # buy xlf
                        buy_xlf()
                        # sell constituent stocks -- add a check to keep them equal
                        sell_xlf_constituents()
                
                # self if xlf sell price is > gs, ms, wfc, bond buy price
                def sell_xlf():
                  exchange_add("XLF","SELL",xlf_bid_price+1,2)
                  print("sold XLF at price ", xlf_bid_price + 1)

                def buy_xlf_constituents():
                  exchange_add("GS","BUY",gs_bid_price+1,4)
                  print("bought GS at price ", gs_bid_price + 1)
                  exchange_add("MS","BUY",ms_ask_price,6)
                  print("bought MS at price ", ms_ask_price)
                  exchange_add("WFC","BUY",wfc_ask_price,4)
                  print("bought WFC at price ", wfc_ask_price)
                  exchange_add("BOND","BUY",bond_ask_price,6)
                  print("bought BOND at price ", bond_ask_price)


                if ((xlf_ask_price + 1) > xlf_fair_val) or (((xlf_ask_price + 1) == xlf_fair_val and positions["XLF"] >= 90)):
                    # buy xlf
                    sell_xlf()
                    # sell constituent stocks -- add a check to keep them equal
                    buy_xlf_constituents()
                
                #have a function to make sure the number of stocks hedged is the same
                if(positions["XLF"] > 90):
                    # sell XLF
                    exchange_convert("XLF","SELL",150)
                elif(positions["XLF"] < -90):
                    #buy XLF
                    exchange_convert("XLF","BUY",150)

                
            
            # ===================== end Trading XLF =====================================================================

            # ==================== Prices from VALBZ ===========================
            if message["symbol"] == "VALBZ":
                def best_price(side):
                    if message[side]:
                        return message[side][0][0]

                valbz_bid_price = best_price("buy")
                valbz_ask_price = best_price("sell")

                now = time.time()

                if now > valbz_last_print_time + 1:
                    valbz_last_print_time = now
        #            print(
        #                {
        #                    "valbz_bid_price": valbz_bid_price,
        #                    "valbz_ask_price": valbz_ask_price,
        #                }
        #            )

            # ==================== Trading VALE/VALBZ ===========================
            elif message["symbol"] == "VALE":

                def best_price(side):
                    if message[side]:
                        return message[side][0][0]

                vale_bid_price = best_price("buy")
                vale_ask_price = best_price("sell")

                now = time.time()

                if now > vale_last_print_time + 1:
                    vale_last_print_time = now
                    # print(positions["VALE"])
                    # print(positions["VALBZ"])
        #            print(
        #                {
        #                    "vale_bid_price": vale_bid_price,
        #                    "vale_ask_price": vale_ask_price,
        #                }
        #            )

                if (valbz_bid_price == None or valbz_ask_price == None or vale_bid_price == None or vale_ask_price == None):
                    continue
                
                
                # have a function to convert if necessary (eg at limit but no break evens)
                # for now, safeguard with VALE and VALBZ should have opposite signs -- make more efficient later
                # convert VALE to VALBZ
                if((positions["VALE"] > 8 and positions["VALBZ"] <= 0) or (positions["VALBZ"] < -8 and positions["VALE"] >= 0)): # would never put you over the conversion limit
                    # convert
                    exchange_convert("VALE","SELL",10)
                    print("converted VALE to VALBZ ")
                # convert VALBZ to VALE
                elif((positions["VALBZ"] > 8 and positions["VALE"] <= 0) or (positions["VALE"] < -8 and positions["VALBZ"] >= 0)):
                    # convert 
                    exchange_convert("VALBZ","SELL",10)
                    print("converted VALBZ to VALE ")

                # buy if VALE buy price is < VALBZ sell price
                if ((vale_bid_price + 1) < valbz_ask_price) or ((vale_bid_price + 1) == valbz_ask_price and positions["VALE"] <= -5):
                        # buy vale
                        exchange_add("VALE","BUY",vale_bid_price+1,5)
                        print("bought VALE at price ", vale_bid_price + 1)
                        # sell valbz -- add a check to keep them equal
                        exchange_add("VALBZ","SELL",valbz_ask_price,5)
                        print("sold VALBZ at price ", valbz_ask_price)
                # sell if VALE sell price > VALBZ buy price
                elif ((vale_ask_price - 1) > valbz_bid_price) or ((vale_ask_price + 1) == valbz_bid_price and positions["VALE"] >= 5):
                        # sell vale
                        exchange_add("VALE","SELL",vale_ask_price-1,5)
                        print("sold VALE at price ", vale_ask_price - 1)
                        # buy valbz
                        exchange_add("VALBZ","BUY",valbz_bid_price,5)
                        print("bought VALBZ at price ", valbz_bid_price)
                #have a function to make sure the number of stocks hedged is the same 
                if(positions["VALE"] > -(positions["VALBZ"]) and vale_ask_price >= valbz_bid_price):
                    if(positions["VALE"<=0]):
                        # sell vale
                        exchange_add("VALE","SELL",vale_ask_price-1,1)
                        print("hedged VALE at price ", vale_ask_price-1)
                    if(positions["VALBZ"<=0]):
                        # buy valbz
                        exchange_add("VALBZ","",valbz_bid_price,1)
                        print("hedged VALBZ at price ", valbz_bid_price+1)
                elif(positions["VALE"] < -(positions["VALBZ"]) and vale_ask_price <= valbz_bid_price):
                    if(positions["VALBZ"<=0]):
                        # sell valbz
                        exchange_add("VALBZ","SELL",valbz_ask_price-1,1)
                        print("hedged VALBZ at price ", valbz_ask_price)
                    elif(positions["VALE">=0]):
                        # buy vale
                        exchange_add("VALE","BUY",vale_bid_price,1)
                        print("hedged VALE at price ", vale_bid_price)
                print(positions["VALE"])
                print(positions["VALBZ"])
            
                    
            # ===================== Trading BOND =======================        
            elif message["symbol"] == "BOND":
                def best_price(side):
                    if message[side]:
                        return message[side][0][0]

                bond_bid_price = best_price("buy")
                bond_ask_price = best_price("sell")

                now = time.time()

                if (bond_bid_price == None or bond_ask_price == None):
                    continue

                if now > bond_last_print_time + 1:
                    bond_last_print_time = now
        #            print(
        #                {
        #                    "bond_bid_price": bond_bid_price,
        #                    "bond_ask_price": bond_ask_price,
        #                }
        #            )
                    # penny: buy for any price < 1000, sell for price > 1000 
                    if ((bond_bid_price + 1) < 1000 and positions["BOND"] < 50):
                        num = 50 # adjust size later?
                        exchange_add("BOND","BUY",bond_bid_price+1,num)
        #                print("bought bond at price ", bond_bid_price + 1)
                    # buy bond at 1000 only if you're near position limit (eg near -100) and you can sell for > 1000
                    elif ((bond_bid_price) == 1000 and positions["BOND"] > 50):
                        exchange_add("BOND","BUY",bond_bid_price,25)
                        
                    if ((bond_ask_price - 1) > 1000 and positions["BOND"] > -50): 
                        num = 50
                        exchange_add("BOND","SELL",bond_bid_price-1,num)
        #                print("sold bond at price ", bond_ask_price - 1)
                    # sell bond at 1000 only if you're near position limit (eg near 100)
                    elif ((bond_ask_price) == 1000 and positions["BOND"] < -50):
                        exchange_add("BOND","SELL",bond_bid_price,25)

    # RESET THE GLOBAL VARIABLES
    id = 1

    vale_bid_price, vale_ask_price = None, None
    vale_last_print_time = time.time()
    positions["VALE"] = 0

    valbz_bid_price, valbz_ask_price = None, None
    valbz_last_print_time = time.time()
    positions["VALBZ"] = 0

    bond_bid_price, bond_ask_price = None, None
    bond_last_print_time = time.time()
    positions["BOND"] = 0

    gs_bid_price, gs_ask_price = None, None
    gs_last_print_time = time.time()
    positions["GS"] = 0

    ms_bid_price, ms_ask_price = None, None
    ms_last_print_time = time.time()
    positions["MS"] = 0

    wfc_bid_price, wfc_ask_price = None, None
    wfc_last_print_time = time.time()
    positions["WFC"] = 0

    xlf_bid_price, xlf_ask_price = None, None
    xlf_last_print_time = time.time()
    positions["XLF"] = 0


# ~~~~~============== PROVIDED CODE ==============~~~~~

# You probably don't need to edit anything below this line, but feel free to
# ask if you have any questinos about what it is doing or how it works. If you
# do need to change anything below this line, please feel free to


class Dir(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class ExchangeConnection:
    def __init__(self, args):
        self.message_timestamps = deque(maxlen=500)
        self.exchange_hostname = args.exchange_hostname
        self.port = args.port
        self.exchange_socket = self._connect(add_socket_timeout=args.add_socket_timeout)

        self._write_message({"type": "hello", "team": team_name.upper()})

    def read_message(self):
        """Read a single message from the exchange"""
        message = json.loads(self.exchange_socket.readline())
        if "dir" in message:
            message["dir"] = Dir(message["dir"])
        return message

    def send_add_message(
        self, order_id: int, symbol: str, dir: Dir, price: int, size: int
    ):
        """Add a new order"""
        self._write_message(
            {
                "type": "add",
                "order_id": order_id,
                "symbol": symbol,
                "dir": dir,
                "price": price,
                "size": size,
            }
        )

    def send_convert_message(self, order_id: int, symbol: str, dir: Dir, size: int):
        """Convert between related symbols"""
        self._write_message(
            {
                "type": "convert",
                "order_id": order_id,
                "symbol": symbol,
                "dir": dir,
                "size": size,
            }
        )

    def send_cancel_message(self, order_id: int):
        """Cancel an existing order"""
        self._write_message({"type": "cancel", "order_id": order_id})

    def _connect(self, add_socket_timeout):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if add_socket_timeout:
            # Automatically raise an exception if no data has been recieved for
            # multiple seconds. This should not be enabled on an "empty" test
            # exchange.
            s.settimeout(5)
        s.connect((self.exchange_hostname, self.port))
        return s.makefile("rw", 1)

    def _write_message(self, message):
        json.dump(message, self.exchange_socket)
        self.exchange_socket.write("\n")

        now = time.time()
        self.message_timestamps.append(now)
        if len(
            self.message_timestamps
        ) == self.message_timestamps.maxlen and self.message_timestamps[0] > (now - 1):
            print(
                "WARNING: You are sending messages too frequently. The exchange will start ignoring your messages. Make sure you are not sending a message in response to every exchange message."
            )


def parse_arguments():
    test_exchange_port_offsets = {"prod-like": 0, "slower": 1, "empty": 2}

    parser = argparse.ArgumentParser(description="Trade on an ETC exchange!")
    exchange_address_group = parser.add_mutually_exclusive_group(required=True)
    exchange_address_group.add_argument(
        "--production", action="store_true", help="Connect to the production exchange."
    )
    exchange_address_group.add_argument(
        "--test",
        type=str,
        choices=test_exchange_port_offsets.keys(),
        help="Connect to a test exchange.",
    )

    # Connect to a specific host. This is only intended to be used for debugging.
    exchange_address_group.add_argument(
        "--specific-address", type=str, metavar="HOST:PORT", help=argparse.SUPPRESS
    )

    args = parser.parse_args()
    args.add_socket_timeout = True

    if args.production:
        args.exchange_hostname = "production"
        args.port = 25000
    elif args.test:
        args.exchange_hostname = "test-exch-" + team_name
        args.port = 25000 + test_exchange_port_offsets[args.test]
        if args.test == "empty":
            args.add_socket_timeout = False
    elif args.specific_address:
        args.exchange_hostname, port = args.specific_address.split(":")
        args.port = int(port)

    return args


if __name__ == "__main__":
    # Check that [team_name] has been updated.
    assert (
        team_name != "REPLACEME"
    ), "Please put your team name in the variable [team_name]."

    main()
