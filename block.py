
import os
class MempoolTransaction:
    def __init__(self, txid, fee, weight, parents):
        self.txid = txid
        self.fee = int(fee)
        self.weight = int(weight)
        self.parents = set(parents.split(',')) if parents else set()
        self.children = set()


def parse_mempool_csv():
    transactions = []
    path = os.path.expanduser("~/Downloads/mempool.csv - Sheet1.csv")
    with open(path) as f:
        for line in f:
            txid, fee, weight, parents = line.strip().split(',')
            transactions.append(MempoolTransaction(txid, fee, weight, parents))
    return transactions


def add_transaction_to_block(transaction, block, max_weight):
    if sum(tx.weight for tx in block) + transaction.weight <= max_weight:
        block.append(transaction)
        return True
    else:
        return False


def construct_block_with_weight_limit(transactions, max_weight):
    sorted_transactions = sorted(transactions, key=lambda x: x.fee, reverse=True)

    block = []

    included_transactions = set()

    for transaction in sorted_transactions:
        print("transaction id: ", transaction.txid)
        # if transaction.txid not in included_transactions and all(parent in included_transactions for parent in transaction.parents):

        if add_transaction_to_block(transaction, block, max_weight):
                included_transactions.add(transaction.txid)
                for child in transaction.children:
                    included_transactions.add(child)

        print("transaction id: ", transaction.txid)
    return block


def main():
    transactions = parse_mempool_csv()
    max_weight = 4000000
    block = construct_block_with_weight_limit(transactions, max_weight)
    for transaction in block:
        print("transaction id: ", transaction.txid)


if __name__ == "__main__":
    main()
