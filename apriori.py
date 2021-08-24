import sys

from itertools import chain, combinations
from collections import defaultdict
from optparse import OptionParser


def subsets(arr):
    # Retorna um conjunto não vazio de Array
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])


def returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet):
    # Calcula o suporte para itens no itemSet e retorna um subconjunto do itemSet
    # Cada um de cujos elementos satisfaz o suporte mínimo
    _itemSet = set()
    localSet = defaultdict(int)

    for item in itemSet:
        for transaction in transactionList:
            if item.issubset(transaction):
                freqSet[item] += 1
                localSet[item] += 1

    for item, count in localSet.items():
        support = float(count) / len(transactionList)

        if support >= minSupport:
            _itemSet.add(item)

    return _itemSet


def joinSet(itemSet, length):
    # Une um conjunto com ele mesmo e retorna os conjuntos de itens de n elementos
    return set(
        [i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length]
    )


def getItemSetTransactionList(data_iterator):
    transactionList = list()
    itemSet = set()
    for record in data_iterator:
        transaction = frozenset(record)
        transactionList.append(transaction)
        for item in transaction:
            itemSet.add(frozenset([item]))
    return itemSet, transactionList


def runApriori(data_iter, minSupport, minConfidence):
    # Executa o algoritmo apriori
    # data_iter é um iterador de registro
    itemSet, transactionList = getItemSetTransactionList(data_iter)

    freqSet = defaultdict(int)
    largeSet = dict()
    # Dicionário global que armazena (chave = n-itemSets, valor = suporte)
    # Satisfazem o minSuporte

    assocRules = dict()
    # Dicionário que armazena regras de associação

    oneCSet = returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet)

    currentLSet = oneCSet
    k = 2
    while currentLSet != set([]):
        largeSet[k - 1] = currentLSet
        currentLSet = joinSet(currentLSet, k)
        currentCSet = returnItemsWithMinSupport(
            currentLSet, transactionList, minSupport, freqSet
        )
        currentLSet = currentCSet
        k = k + 1

    def getSupport(item):
        # Retorna o suporte de um item
        return float(freqSet[item]) / len(transactionList)

    toRetItems = []
    for key, value in largeSet.items():
        toRetItems.extend([(tuple(item), getSupport(item)) for item in value])

    toRetRules = []
    for key, value in list(largeSet.items())[1:]:
        for item in value:
            _subsets = map(frozenset, [x for x in subsets(item)])
            for element in _subsets:
                remain = item.difference(element)
                if len(remain) > 0:
                    confidence = getSupport(item) / getSupport(element)
                    if confidence >= minConfidence:
                        toRetRules.append(((tuple(element), tuple(remain)), confidence))
    return toRetItems, toRetRules


def printResults(items, rules):
    # Imprime os conjuntos de itens gerados classificados por suporte e as regras de confiança classificadas por confiança
    for item, support in sorted(items, key=lambda x: x[1]):
        print("item: %s , %.3f" % (str(item), support))
    print("\n------------------------ RULES:")
    for rule, confidence in sorted(rules, key=lambda x: x[1]):
        pre, post = rule
        print("Rule: %s ==> %s , %.3f" % (str(pre), str(post), confidence))


def to_str_results(items, rules):
    # Imprime os conjuntos de itens gerados classificados por suporte e as regras de confiança classificadas por confiança
    i, r = [], []
    for item, support in sorted(items, key=lambda x: x[1]):
        x = "item: %s , %.3f" % (str(item), support)
        i.append(x)

    for rule, confidence in sorted(rules, key=lambda x: x[1]):
        pre, post = rule
        x = "Rule: %s ==> %s , %.3f" % (str(pre), str(post), confidence)
        r.append(x)

    return i, r


def dataFromFile(fname):
    # Função que lê o arquivo e produz um gerador
    with open(fname, "rU") as file_iter:
        for line in file_iter:
            line = line.strip().rstrip(",")
            record = frozenset(line.split(","))
            yield record


if __name__ == "__main__":

    optparser = OptionParser()
    optparser.add_option(
        "-f", "--arquivo", dest="input", help="Nome do arquivo CSV", default=None
    )
    optparser.add_option(
        "-s",
        "--minSuporte",
        dest="minS",
        help="Valor do suporte mínimo",
        default=0.15,
        type="float",
    )
    optparser.add_option(
        "-c",
        "--minConfianca",
        dest="minC",
        help="Valor da confiança mínima",
        default=0.6,
        type="float",
    )

    (options, args) = optparser.parse_args()

    inFile = None
    if options.input is None:
        inFile = sys.stdin
    elif options.input is not None:
        inFile = dataFromFile(options.input)
    else:
        print("Falha ao localizar arquivo\n")
        sys.exit("Saindo...")

    minSupport = options.minS
    minConfidence = options.minC

    items, rules = runApriori(inFile, minSupport, minConfidence)

    printResults(items, rules)
