import csv

file = "./supplied-products.csv"

def generateBase():
    return "@base <http://localhost:8000/lecoqlibre/datafoodconsortium>.\n"

def generatePrefix(prefix, uri):
    return "@prefix " + prefix + ": <" + uri + ">.\n"

def generatePrefixDfcB():
    return generatePrefix("dfc-b", "https://www.datafoodconsortium.org#")

def generatePrefixDfcPt():
    return generatePrefix("dfc-pt", "https://www.datafoodconsortium.org/product-types#")

def generatePrefixDfcF():
    return generatePrefix("dfc-f", "https://www.datafoodconsortium.org/facets#")

def generatePrefixDfcM():
    return generatePrefix("dfc-m", "https://www.datafoodconsortium.org/measures#")

def generatePrefixSolid():
    return generatePrefix("solid", "http://www.w3.org/ns/solid/terms#")

def generatePrefixIndex():
    return generatePrefix("index", "TBD")

def generatePrefixes():
    return generateBase() \
        + generatePrefixDfcB() \
        + generatePrefixDfcPt() \
        + generatePrefixDfcF() \
        + generatePrefixDfcM()

def generateSuppliedProduct(row):
    return generatePrefixes() \
        + "\n" \
        + "<>\n" \
        + "\ta dfc-b:SuppliedProduct;\n" \
        + "\tdfc-b:hasType dfc-pt:" + row[3] + ";\n" \
        + "\tdfc-b:description \"" + row[0] + "\";\n" \
        + "\tdfc-b:hasCertification dfc-f:Organic-AB;\n" \
        + "\tdfc-b:hasQuantity [\n" \
        + "\t\ta dfc-b:QuantitativeValue;\n" \
        + "\t\tdfc-b:hasUnit dfc-m:Kilogram;\n" \
        + "\t\tdfc-b:value 1\n" \
        + "\t];\n" \
        + "\tdfc-b:image </images/" + row[1] + ".jpg>.\n"

def generateCatalogItem(row):
    return generatePrefixes() \
        + "\n" \
        + "<>\n" \
        + "\ta dfc-b:CatalogItem;\n" \
        + "\tdfc-b:name \"" + row[0] + "\"\n" \
        + "\tdfc-b:references </defined-products/supplied-products/" + row[1] + ".ttl>;\n" \
        + "\tdfc-b:stockLimitation 24;\n" \
        + "\tdfc-b:offeredThrough <#offer1>;\n" \
        + "\tdfc-b:listedIn </catalogs/default/catalog.ttl>.\n" \
        + "\n" \
        + "<#offer1>\n" \
        + "\ta dfc-b:Offer;\n" \
        + "\tdfc-b:offeredTo </agents/customer-categories.tll#default>;\n" \
        + "\tdfc-b:offers <>;\n" \
        + "\tdfc-b:hasPrice <#price1>;\n" \
        + "\tdfc-b:stockLimitation 12;\n" \
        + "\tdfc-b:listedIn </sale-sessions/sale-session1.ttl>.\n" \
        + "\n" \
        + "<#price1>\n" \
        + "\ta dfc-b:Price;\n" \
        + "\tdfc-b:value " + row[2] + ";\n" \
        + "\tdfc-b:VATrate 5.5;\n" \
        + "\tdfc-b:hasUnit dfc-m:Euro.\n"

def generateCatalog():
    return generateBase() \
        + generatePrefixDfcB() \
        + "\n" \
        + "<>\n" \
        + "\ta dfc-b:Catalog;\n" \
        + "\tdfc-b:lists\n"

def generateCatalogList(row):
    return "\t\t</catalogs/default/catalog-items/" + row[1] + ".ttl>,\n"

def getSuppliedProductFilename(row):
    return "./dataset/defined-products/supplied-products/" + row[1] + ".ttl"

def getCatalogItemFilename(row):
    return "./dataset/catalogs/default/catalog-items/" + row[1] + ".ttl"

def getCatalogFilename():
    return "./dataset/catalogs/default/catalog.ttl"

def getProductTypeIndexFilename():
    return "./dataset/catalogs/default/index0.ttl"

def populateProductTypeIndex(productTypeIndex, row):
    if row[3] not in productTypeIndex:
        productTypeIndex[row[3]] = []    
    productTypeIndex[row[3]].append(row[1])

def generateProductTypeIndex():
    return generateBase() \
        + generatePrefixSolid() \
        + generatePrefixDfcPt() \
        + generatePrefixIndex() \
        + "\n<>\n" \
        + "\ta index:Index;\n" \
        + "\ta solid:ListedDocument.\n\n"

def generateProductTypeIndexRegistration(productType, catalogItems):
    result = "<#" + productType + "> a index:Registration;\n" \
        + "\tindex:mentions dfc-pt:" + productType + ";\n" \
        + "\tsolid:instance \n"
    for catalogItem in catalogItems:
        result += "\t\t</catalogs/default/catalog-items/" + catalogItem + ".ttl>;\n"
    return result[:-2] + ".\n\n"

catalog = open(getCatalogFilename(), "w")
catalog.write(generateCatalog())
catalogList = ""

productTypeIndex = {}

with open(file, newline='') as csvFile:
    reader = csv.reader(csvFile, delimiter=';', quotechar='"')

    for row in reader:
        populateProductTypeIndex(productTypeIndex, row)

        f = open(getSuppliedProductFilename(row), "w")
        f.write(generateSuppliedProduct(row))
        f.close()

        f = open(getCatalogItemFilename(row), "w")
        f.write(generateCatalogItem(row))
        f.close()

        catalogList += generateCatalogList(row)
        
catalog.write(catalogList[:-2] + ".\n")
catalog.close()

f = open(getProductTypeIndexFilename(), "w")
f.write(generateProductTypeIndex())
registrations = ""
for productType, catalogItems in productTypeIndex.items():
    registrations += generateProductTypeIndexRegistration(productType, catalogItems)
f.write(registrations)
f.close()