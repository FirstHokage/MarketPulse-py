import json
import urllib.request
import argparse

def get_market_price(symbol):
    """Fetches live prices from Finance's public chart API."""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    try:
        # Well, no need to explain xD
    
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            result = data.get('chart', {}).get('result')
            if result:
                return result[0]['meta']['regularMarketPrice']
    except Exception:
        pass
    return None

def display_price(name, price):
    
    if price < 0.01:
        print(f"🔹 {name.upper()}: ${price:,.6f}")
    else:
        print(f"🔹 {name.upper()}: ${price:,.2f}")

def main():
    parser = argparse.ArgumentParser(description="Universal Market Tracker (Metals, Crypto, Stocks)")
    parser.add_argument(
        "asset", 
        nargs="?", 
        default="all", 
        help="Type 'all' or specify an asset like 'gold', 'copper', 'btc', or 'shib'"
    )
    
    args = parser.parse_args()
    query = args.asset.lower().strip()
    
    
    aliases = {
        "gold": "GC=F",
        "silver": "SI=F",
        "copper": "HG=F",
        "platinum": "PL=F",
        "btc": "BTC-USD",
        "bitcoin": "BTC-USD",
        "eth": "ETH-USD",
        "ethereum": "ETH-USD",
        "usdt": "USDT-USD",
        "tether": "USDT-USD",
        "bnb": "BNB-USD",
        "sol": "SOL-USD",
        "solana": "SOL-USD",
        "xrp": "XRP-USD",
        "doge": "DOGE-USD",
        "dogecoin": "DOGE-USD",
        "chainlink": "LINK-USD",
        "monero": "XMR-USD",
        "xdash": "DASH-USD",
        "dash": "DASH-USD"
    }
    
    print("Fetching live market data...\n" + "-"*40)

    if query == "all":
        
        dashboard = ["btc", "eth", "usdt", "bnb", "sol", "xrp", "doge", 
            "chainlink", "monero", "xdash", "gold", "silver", 
            "platinum", "copper"]
        for item in dashboard:
            price = get_market_price(aliases[item])
            if price:
                display_price(item.capitalize(), price)
            else:
                print(f"❌ Failed to fetch {item.capitalize()}")
                
        print("-" * 40)
        print("💡 Tip: Try running 'python YourTracker.py gold' or 'python YourTracker.py xmr'")
        
    else:
        symbol_to_try = aliases.get(query)
        price = None
        
        if symbol_to_try:
            # Matches a known alias (e.g., "copper" -> "HG=F")
            price = get_market_price(symbol_to_try)
        else:
            
            price = get_market_price(f"{query.upper()}-USD")
            if not price:
                
                price = get_market_price(query.upper())
                
        if price:
            display_price(query, price)
        else:
            print(f"❌ Could not find price for '{query}'. Try a standard name like 'copper' or a ticker like 'xrp'.")

if __name__ == "__main__":
    main()







# FirstHokage ©