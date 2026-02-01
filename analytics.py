from storage import load_trades

def performance_report():
    trades = load_trades()

    if not trades:
        print("No trades recorded yet.")
        return

    wins = [t for t in trades if t["result"] == "WIN"]
    losses = [t for t in trades if t["result"] == "LOSS"]

    win_rate = (len(wins) / len(trades)) * 100
    avg_rr = sum(t["rr"] for t in trades) / len(trades)

    print("\n===== PERFORMANCE REPORT =====")
    print(f"Total Trades : {len(trades)}")
    print(f"Wins         : {len(wins)}")
    print(f"Losses       : {len(losses)}")
    print(f"Win Rate     : {win_rate:.2f}%")
    print(f"Avg R:R      : {avg_rr:.2f}")
    print("==============================\n")

if __name__ == "__main__":
    performance_report()
