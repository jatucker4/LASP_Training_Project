import pickle

fileObject = open("SaveFiles/breakoutSaveFile11:40AM on July 31", 'rb')
b = pickle.load(fileObject)
print(b)