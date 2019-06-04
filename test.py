import asyncio
import gdax
import json
import time

async def run_orderbook():
    async with gdax.orderbook.OrderBook(['ETH-USD', 'BTC-USD']) as orderbook:
        while True:
            message = await orderbook.handle_message()
            print(message)
            print("Hello")
            #if message is None:
            #    continue
            #print('ETH-USD ask: %s bid: %s' %
            #      (orderbook.get_ask('ETH-USD'),
            #       orderbook.get_bid('ETH-USD')))
            #print('BTC-USD ask: %s bid: %s' %
            #      (orderbook.get_ask('BTC-USD'),
            #       orderbook.get_bid('BTC-USD')))
            

async def main():
    trader = gdax.trader.Trader(
        product_id='BTC-USD',
        api_key='9e293580cb9c373cde7276ecc0daa20d',
        api_secret='3SIr5U7TDaJ08Fi+mpqv2xx0tUBSWNZQhYFmhwsnqaX+YaybMs5mgEGcDia2m3S9XaldfrHFitiBvSjIjL32ZQ==',
        passphrase='Godlike1')
    res = await trader.get_account()
    f = open("get_account.json","w+")
    f.write(json.dumps(res, indent=4, sort_keys=True))
    #res = await trader.sell(type='limit', size='0.00001', price='99999.12')
    #print(res)

if __name__ == "__main__":
    start_time = time.time()
    loop = asyncio.get_event_loop()
    #loop.run_until_complete(main())
    loop.run_until_complete(run_orderbook())
    print("--- %s seconds ---" % (time.time() - start_time))