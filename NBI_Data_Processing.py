import arcpy, csv, os, urllib, sys, traceback
import BS_Scrape as bs

def FetchCSV( inStates, directory ):
    """ Fetches NBI bridge data """
    url = 'http://www.fhwa.dot.gov/bridge/nbi/2010/'
    for state in inStates:
	KillObject(os.path.join(directory, state + '10.txt'))
 	urllib.urlretrieve(url + state + '10.txt', os.path.join(directory, state + '10.txt'))

def KillObject( object ):
    """ Kills an input object """
    if arcpy.Exists(object):
        arcpy.Delete_management(object)

def MakeFgdb( dir, db, fd, spatRef ):
    """ Create a file geodatabase and featuredataset """
    if os.path.isdir(dir) != 1:
        os.mkdir(dir)
    KillObject( os.path.join(dir, db) )
    arcpy.CreateFileGDB_management(dir, db)
    arcpy.CreateFeatureDataset_management(os.path.join(dir, db), fd, spatRef)
    
def CreateGdbTable( db, table, fields ):
    """	Creates an empty standalone GDB table and adds fields provided in a list - with a set schema """
    KillObject( db + '/' + table )
    arcpy.CreateTable_management(db, table)
    for field in fields:
	if field[1] == 'TEXT':
	    arcpy.AddField_management(db + '/' + table,field[0],field[1],'#','#',field[2],field[3],'NULLABLE','NON_REQUIRED','#')
	else:
	    arcpy.AddField_management(db + '/' + table,field[0],field[1],'#','#','#',field[3],'NULLABLE','NON_REQUIRED','#')

def AddFields( db, table, fieldList ):
    """ Add fields to a table or featureclass """
    for field in fields:
	if field[1] == 'TEXT':
	    arcpy.AddField_management(db + '/' + table,field[0],field[1],'#','#',field[2],field[3],'NULLABLE','NON_REQUIRED','#')
	else:
	    arcpy.AddField_management(db + '/' + table,field[0],field[1],'#','#','#',field[3],'NULLABLE','NON_REQUIRED','#')
	    
def CreateFc( db, name, fields ):
    """ Creates a featureclass in given location """
    KillObject( db + '/' + name )
    arcpy.CreateFeatureclass_management(db, name, 'POINT')
    AddFields( db, name, fields )
	    
def GetStateName( inStateCode, inStateDict ):
    """ Takes a state FIPS code and returns the state name """
    if inStateCode in inStateDict.keys():
	stateName = inStateDict[inStateCode][0]
    else:
	stateName = '99'
    return stateName

def ParseNbiFile( file, stateDict ):
    """ Parses NBI bridge file and return what we want in a list """
    # Open the text file, read it into memory
    data = open(file).read().splitlines()
    # Define a new, empty list object
    l = []
    # Iterate through the lines of the file, slice up the line by index
    #   position of each data column
    ln = 0
    for line in data:
	latDMS = line[129:137] 
	lonDMS = line[137:146]
	# Only process rows with valid lat/lon values
	if len(latDMS.strip()) > 0 and int(latDMS.strip()) > 0:
	    if len(lonDMS.strip()) > 0 and int(lonDMS.strip()) > 0:
		stateCode = GetStateName( line[0:2], stateDict )
		latDeg = latDMS[0:2] 
		#print latDeg
		latMin = latDMS[2:4]  
		#print latMin
		latSec = latDMS[4:6]+'.'+latDMS[6:8]  
		#print latSec
		latDD = str(int(latDeg)+(float(latMin)/60)+(float(latSec)/3600)) 
		lonDeg = lonDMS[0:3]
		#print lonDeg
		lonMin = lonDMS[3:5] 
		#print lonMin
		lonSec = lonDMS[5:7]+'.'+lonDMS[7:9]  
		#print lonSec
		lonDD = str('-'+str(int(lonDeg)+(float(lonMin)/60)+float(lonSec)/3600)) 
		yearBuilt = line[156:160]  
		strucNum = line[4:18]
		#print '\n' + str(strucNum)
		facility = line[62:80]
		# Add our line to list l
		# Do string formatting to lat/long to only display 5 decimal points
		l.extend([[strucNum,stateCode,facility,('%.5f' % float(latDD)),('%.5f' % float(lonDD)),yearBuilt]])
    return l

def PushNbiToTable( tbl, inList, fields ):
    """ Take a list of NBI data and push it to a FGDB standalone table """
    rows = arcpy.InsertCursor(tbl)
    ln = 0
    for line in inList:
	t = 0
	# Create a new row
	row = rows.newRow()
	# Iterate through the fields
	for field in fields:
	    val = line[t].strip()
	    # Set the value for each field
	    if field[1] == 'DOUBLE':
		row.setValue(field[0], '%.5f' % float(val))
	    else:
		row.setValue(field[0], val)
	    t = t + 1
	# insert the row into the table
	rows.insertRow(row)
	ln = ln + 1
	del row
	del t
	del line
    del rows

def PushNbiToFeatureclass( inFc, inList, fields ):
    """ Take a list of NBI data and push it directly to a FGDB point FC """
    cur = arcpy.InsertCursor(inFc)
    for line in inList:
	t = 0
	feat = cur.newRow()
	feat.shape = arcpy.Point(line[4], line[3])
	for field in fields:
	    val = line[t].strip()
	    # Set the value for each field
	    if field[1] == 'DOUBLE':
		feat.setValue(field[0], '%.5f' % float(val))
	    else:
		feat.setValue(field[0], val)
	    t = t + 1
	# Insert the row into the table
	cur.insertRow(feat)
    del cur  

if __name__ == '__main__':
    try:
        directory_in = 'C:/temp/python/data/inputs'
        directory_out = 'C:/temp/python/data/outputs'
	# our spatial reference, this can be copied from a prj file
	sr = 'GEOGCS["GCS_North_American_1927",DATUM["D_North_American_1927",SPHEROID["Clarke_1866",6378206.4,294.9786982]],\
	      PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'
	# our list of fields and their properties:
	#   [field_name,field_type,field_length (zero for non-text fields),field_alias]
	fields = [['STRUCTURE_NUMBER','TEXT','18','Structure Number'],
		  ['STATE','TEXT','2','State'],
		  ['FACILITY_CARRIED_BY_STRUCTURE','TEXT','20','Facility Carried By Structure'],
		  ['LAT','DOUBLE','0','Latitude'],
		  ['LON','DOUBLE','0','Longitude'],
		  ['YEAR_BUILT','TEXT','4','Year Bridge Was Construted']]
	files = ['ar','ok']
	# Fetch data files
	FetchCSV( files, directory_in )
	# Create our new file geodatabase to work with
	MakeFgdb( directory_out, 'NBI.gdb', 'Bridges', sr )
	# Create our standalone geodatabase table and its schema
	CreateGdbTable( os.path.join(directory_out, 'NBI.gdb'), 'NbiTest', fields )
	
	CreateFc( os.path.join(directory_out, 'NBI.gdb/Bridges'), 'NbiBridges', fields )	    
	# Get dict of state names and codes
	stateDict = bs.FetchFipsCodes( )
	## Push csv to table
	for f in files:
	    k = ParseNbiFile( os.path.join(directory_in, f + '10.txt'), stateDict )
	    PushNbiToTable( os.path.join(directory_out, 'NBI.gdb/NbiTest'), k , fields)
	    PushNbiToFeatureclass( os.path.join(directory_out, 'NBI.gdb/Bridges/NbiBridges'), k, fields)
	print 'Done'
    except Exception, err:
	tb = sys.exc_info()[2]
	tbinfo = traceback.format_tb(tb)[0]
	pymsg = "\nPYTHON ERRORS:\nTraceback Info:\n" + tbinfo + "\nError Info:\n	   " + \
				str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
	print pymsg
	msgs = "GP ERRORS:\n" + arcpy.GetMessages(2) + "\n"
	print msgs
	sys.stderr.write('ERROR: %s\n' % str(err))
	
