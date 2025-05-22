import sys
from model import *

if len(sys.argv) < 2:
    print("Usage: python script.py <organism_name>")
    sys.exit(1)

def find_lineage(organism_name):
    #initialize database connection
    init()
    #find Name entries matching organism_name
    name_entries = list(Name.select(Name.q.name ==  organism_name))

    if not name_entries:
        print("No taxonomic entry found for organism",organism_name,". Make sure to enter an organism's scientific name")
        return

    #processes each name entry if there are multiple and gets Taxonomy record for each
    for name_entry in name_entries:
        taxonomy = name_entry.taxonomy
        print("Found taxonomy for", organism_name,":",taxonomy.scientific_name," TaxID:",taxonomy.taxid)

        #list to store lineage
        lineage = []
        #start from current taxonomy
        current_taxon = taxonomy
        #loops until root is reached
        while current_taxon.parent is not None and current_taxon != current_taxon.parent:
            lineage.append(current_taxon.rank + ":" + current_taxon.scientific_name + " TaxID:" + str(current_taxon.taxid))
            #move current_taxon to parent taxon
            current_taxon = current_taxon.parent

        #add root taxon
        lineage.append(current_taxon.rank + ":" + current_taxon.scientific_name + " TaxID:" + str(current_taxon.taxid))

        #print lineage in reverse order
        print("\nTaxonomic Lineage:")
        for rank in reversed(lineage):
            print(rank)
        print()

organism_name = sys.argv[1]
find_lineage(organism_name)
