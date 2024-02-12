#import pandas as pd
import os
class MempoolTransaction:
    def _init_(self, txid, fee, weight, parents):
        self.txid = txid
        self.fee = int(fee)
        self.weight = int(weight)
        self.parents = set(parents.split(';')) if parents else set()
        self.children = set()


def parse_mempool_csv():
    path = os.path.expanduser("~/Download/mempool.csv-Sheet1.csv")
    with open(path) as f:
        return [MempoolTransaction(*line.strip().split(',')) for line in f.readlines()]


def construct_block(transactions, max_weight):
    sorted_transactions = sorted(transactions, key=lambda x: x.fee, reverse=True)
    block = []
    included_transactions = set()

    for transaction in sorted_transactions:
        if transaction.txid not in included_transactions and all(
                parent in included_transactions for parent in transaction.parents):
            if sum(tx.weight for tx in block) + transaction.weight <= max_weight:
                block.append(transaction)
                included_transactions.add(transaction.txid)
                for child in transaction.children:
                    included_transactions.add(child)

    return block


def main():
    transactions = parse_mempool_csv()
    block = construct_block(transactions, max_weight=4000000)

    for transaction in block:
        print(transaction.txid)



main()
