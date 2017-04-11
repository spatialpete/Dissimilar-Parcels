#http://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/vector.html#iterating-over-vector-layer
#http://gis.stackexchange.com/questions/32521/is-there-a-way-to-use-select-by-attribute-in-qgis-using-a-python-command
import numpy

# iface.activeLayer() is the selected layer in the map view
layParcel = iface.activeLayer()

# creating streetList variable
streetList = []

# populating streetList from parcel data field STNAME (field 20)
features = layParcel.getFeatures()
for feat in features:
    attrs = feat.attributes()
    #preventing duplicates, only adds road names not already in the list
    if attrs[20] not in streetList:
        streetList.append(attrs[20])

print streetList

#now a for loop to iterate through streets
for street in streetList:
# The important part: get the feature iterator with an expression
    it = layParcel.getFeatures( QgsFeatureRequest().setFilterExpression ( u'"STNAME" = \'%s\'' %(street) ) )
# Set the selection - select street by roadname
    layParcel.setSelectedFeatures( [ f.id() for f in it ] )
    featuresSel = layParcel.selectedFeatures()
    #clearing parcelStats & parcelMean for each iteration
    parcelStats = []
    parcelMean = 0
    #for each selected parcel
    for parcels in featuresSel:
        parcelAttributes = parcels.attributes()
        #print the building value for testing
        #print parcelAttributes[14]
        #appending all stats to a list for processing, and converting to Integers
        parcelStats.append(int(parcelAttributes[13]))
        parcelMean += int(parcelAttributes[13])
        print parcelMean
    #Calculating std deviation and mean using numpy on the list
    parcelStdDev = numpy.std(parcelStats)
    #parcelMean = numpy.mean(parcelStats)
    #didn't work very well, going to calculate mean manually
    if len(parcelStats) > 0:
        pMean = parcelMean / len(parcelStats)
        print street +" " + str(pMean)
    #iterate over the selection again to select parcels
    #which deviate from the mean
    for parcels in featuresSel:
        parcelAttributes = parcels.attributes()
        # if the building value is less than or equal to 3 std deviations from the mean
        #print parcelAttributes[13], pMean
        if int(parcelAttributes[13]) < (pMean - parcelStdDev):
            print parcelAttributes[0]  + " " +str(pMean)+ " " + parcelAttributes[13]
        else:
            print "parcel " + parcelAttributes[1] + " is not 1 std deviation less than the mean"
    
    