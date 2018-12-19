import pickle
from importer import Mail


def main():
    data = pickle.load(open("../DataDumps/mailDump.p", "rb"))

    print(len(data))



if __name__=='__main__':
    main()