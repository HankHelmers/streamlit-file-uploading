# Class: Contains all relevent information saved for each gene saved / url inspected
# Inputs:
# * name - gene name, retrieved from website
# * description - gene that we are investigating, example CPS4
# * organism - inputted in main function, common name
# * dataset - inputted in main function, dataset used for reference
# * sequence - CDS sequence, retrieved from the website
class SequencePacket:
    def __init__(self, url, name, description, organism, dataset, sequence):
        self.url = url
        self.name = name
        self.description = description
        self.organism = organism
        self.dataset = dataset
        self.sequence = sequence
