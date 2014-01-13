import sys, traceback, Dictionaries, arcgisscripting, GpModules, csv, time
import locale
locale.setlocale(locale.LC_ALL,'')

start = time.clock()

gp = arcgisscripting.create()

flds = [['STATE','TEXT','20','State Name'],
['STRUC_NO','TEXT','17','Structure Number'],
['REC_TYPE','TEXT','3','Record Type'],
['RT_SIG_PFX','TEXT','40','Route Signing Prefix'],
['LVL_SERV','TEXT','50','Designated Level of Service'],
['RT_NO','TEXT','7','Route Number'],
['DIR_SUFFIX','TEXT','30','Directional Suffix'],
['HWY_AG_DST','TEXT','4','Highway Agency District'],
['COUNTY','TEXT','30','County Name'],
['PLACE_CODE','TEXT','40','Place Code'],
['FEAT_INTSC','TEXT','26','Features Intersected'],
['CRT_FAC_IN','TEXT','3','Critical Facility Indicator'],
['FAC_CAR_ST','TEXT','20','Facility Carried By Structure'],
['LOCATION','TEXT','27','Location'],
['MIN_VT_CLR','TEXT','0','Inventory Route, Minimum Vertical Clearance'],
['KM_POINT','TEXT','0','Kilometerpoint'],
['HWY_NETWK','TEXT','0','Base Highway Network'],
['LRS_ROUTE','TEXT','12','LRS Inventory Route'],
['SUBRT_NO','TEXT','0','Subroute Number'],
['LAT_DMS','TEXT','0','Latitute Degrees Minutes Seconds'],
['LAT_DEG','TEXT','0','Latitude Degrees'],
['LAT_MIN','TEXT','0','Latitude Minutes'],
['LAT_SEC','TEXT','0','Latitude Seconds'],
['LAT_DD','DOUBLE','0','Latitude Decimal Degrees'],
['LON_DMS','TEXT','0','Longitude Degrees Minutes Seconds'],
['LON_DEG','TEXT','0','Longitude Degrees'],
['LON_MIN','TEXT','0','Longitude Minutes'],
['LON_SEC','TEXT','0','Longitude Seconds'],
['LON_DD','DOUBLE','0','Longitude Decimal Degrees'],
['BYPASS_LEN','FLOAT','0','Bypass/Detour Length'],
['TOLL','TEXT','50','Toll'],
['MAINT_RESP','TEXT','50','Maintenance Responsibility'],
['OWNER','TEXT','50','Owner'],
['FUNCT_CLA','TEXT','80','Functional Class Of Inventory Route'],
['YEAR_BUILT','TEXT','0','Year Built'],
['LANES_ON','TEXT','0','Lanes On Structure'],
['LANES_UNDR','TEXT','0','Lanes Under Structure'],
['AVG_TRAFIC','LONG','0','Average Daily Traffic'],
['YR_AVG_TRF','TEXT','0','Year Of Average Daily Traffic'],
['DSGN_LOAD','TEXT','0','Design Load'],
['APRCH_WIDH','FLOAT','0','Approach Roadway Width'],
['BRDG_MEDN','TEXT','50','Bridge Median'],
['SKEW','TEXT','0','Skew'],
['STRX_FLARD','TEXT','0','Structure Flared'],
['BRDG_RAILS','TEXT','3','Bridge Railings'],
['TRANSTNS','TEXT','3','Transitions'],
['APRCH_RAIL','TEXT','3','Approach Guardrail'],
['APRCH_R_ED','TEXT','3','Approach Guardrail Ends'],
['HIST_SIGNF','TEXT','0','Historical significance'],
['NAV_CTRL','TEXT','3','Navigation Control'],
['NAV_VT_CLR','TEXT','0','Navigation Vertical Clearance'],
['HAV_HZ_CLR','TEXT','0','Navigation Horizontal Clearance'],
['STRX_OPEN','TEXT','3','Structure Open/Posted/Closed'],
['SRV_TYP_ON','TEXT','0','Type of Service On Bridge'],
['SRV_TYP_UN','TEXT','0','Type of Service Under Bridge'],
['DSGN_TYPE','TEXT','0','Kind of Material/Design'],
['MAT_TYPE','TEXT','0','Type of Design/Construction'],
['MAT_KIND','TEXT','0','Kind of Material/Design'],
['CNST_TYPE','TEXT','0','Type of Design/Construction'],
['NO_MN_SPAN','TEXT','0','Number Of Spans In Main Unit'],
['NO_AP_SPAN','TEXT','0','Number Of Approach Spans'],
['TOT_HZ_CLR','TEXT','0','Inventory Rte Total Horz Clearance'],
['MX_SPN_LEN','TEXT','0','Length Of Maximum Span'],
['STRX_LEN','TEXT','0','Structure Length'],
['L_CURB_LEN','TEXT','0','Left Curb/Sidewalk Width'],
['R_CURB_LEN','TEXT','0','Right Curb/Sidewalk Width'],
['RDWY_WIDTH','TEXT','0','Bridge Roadway Width Curb-To-Curb'],
['DECK_WIDTH','TEXT','0','Deck Width, Out-To-Out'],
['MN_V_CLR_O','TEXT','0','Min Vert Clear Over Bridge Roadway'],
['O_REF_FEAT','TEXT','3','Reference Feature'],
['MN_V_CLR_U','TEXT','0','Minimum Vertical Underclearance'],
['U_REF_FEAT','TEXT','3','Reference Feature'],
['MN_LAT_UC','TEXT','0','Minimum Lateral Underclearance'],
['MN_LAT_UCL','TEXT','0','Min Lateral Underclear On Left'],
['DECK','TEXT','3','Deck'],
['SUPERSTRX','TEXT','3','Superstructure'],
['SUBSTRX','TEXT','3','Substructure'],
['CHAN_PROT','TEXT','3','Channel/Channel Protection'],
['CULVERTS','TEXT','3','Culverts'],
['OP_RT_METH','TEXT','0','Method Used To Determine Operating Rating'],
['OPER_METH','TEXT','0','Operating Rating'],
['IV_RT_METH','TEXT','0','Method Used To Determine Inventory Rating'],
['INVEN_METH','TEXT','0','Inventory Rating'],
['STRX_EVAL','TEXT','3','Structural Evaluation'],
['DECK_GEOM','TEXT','3','Deck Geometry'],
['UC_VT_HZ','TEXT','3','Underclear, Vertical & Horizontal'],
['BRDG_POST','TEXT','0','Bridge Posting'],
['WW_ADEQCY','TEXT','3','Waterway Adequacy'],
['AP_RW_ALGN','TEXT','3','Approach Roadway Alignment'],
['PRP_WK_TYP','TEXT','0','Type of Work Proposed'],
['WK_DONE_BY','TEXT','3','Work Done By'],
['IMPVMT_LEN','TEXT','0','Length Of Structure Improvement'],
['INSPECT_DT','TEXT','0','Inspection Date'],
['INSPT_FREQ','TEXT','0','Designated Inspection Frequency'],
['FRX_DET','TEXT','5','Fracture Critical Details'],
['UDWAT_INSP','TEXT','5','Underwater Inspection'],
['OT_INSP','TEXT','5','Other Special Inspection'],
['FRX_DET_DT','TEXT','6','Fracture Critical Details Date'],
['UD_INSP_DT','TEXT','6','Underwater Inspection Date'],
['OT_INSP_DT','TEXT','6','Other Special Inspection Date'],
['BRG_IMP_CT','TEXT','0','Bridge Improvement Cost'],
['RW_IMP_CT','TEXT','0','Roadway Improvement Cost'],
['TOT_COST','TEXT','0','Total Project Cost'],
['YR_IMP_EST','TEXT','0','Year Of Improvement Cost Estimate'],
['NGHB_ST_CD','TEXT','5','Neighboring State Code'],
['PCT_RESP','TEXT','0','Percent Responsibility'],
['BD_BRG_NO','TEXT','17','Border Bridge Structure Number'],
['STRAHNET','TEXT','0','STRAHNET Highway Designation'],
['STRX_DESIG','TEXT','3','Parallel Structure Designation'],
['TRAFIC_DIR','TEXT','0','Direction Of Traffic'],
['TMP_STR_DS','TEXT','3','Temporary Structure Designation'],
['HY_SOI_RT','TEXT','0','Highway System Of Inventory Route'],
['FD_LND_HY','TEXT','0','Federal Lands Highways'],
['YR_RECONST','TEXT','0','Year Reconstructed'],
['DK_ST_TYPE','TEXT','3','Deck Structure Type'],
['WR_SF_TYPE','TEXT','3','Type of Wearing Surface'],
['MEMB_TYPE','TEXT','3','Type of Membrane'],
['DK_PROTCT','TEXT','3','Deck Protection'],
['AVG_TRCK_C','TEXT','0','Average Daily Truck Traffic'],
['NAT_NETWRK','TEXT','0','Designated National Network'],
['PIER_PROT','TEXT','0','Pier/Abutment Protection'],
['NBIS_LEN','TEXT','3','NBIS Bridge Length'],
['SCR_BRDGS','TEXT','3','Scour Critical Bridges'],
['FUT_ADT','TEXT','0','Future Average Daily Traffic Count'],
['YR_FUT_ADT','TEXT','0','Year of Future Average Dailiy Traffic Count'],
['MN_NAV_CLR','TEXT','0',
 'Minimum Navigation Vertical Clearance Vertical Lift Bridge'],
['FED_AGNCY','TEXT','0','Federal Agency Indicator'],
['WASH_USE','TEXT','0','Washington Headquarters Use'],
['STATUS','TEXT','0','Status'],
['ASTERISK','TEXT','3','Asterisk Field in SR'],
['SUFF_RATNG','TEXT','0',
 'Sufficiency Rating (select from last 4 positions only)']]

def get_state( st_code ):
    try:
        stDict = Dictionaries.nbiStCodes
        if st_code in stDict.keys():
            state = stDict[st_code]
        else:
            state = 'UNKNOWN'
        return state
    except:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = 'PYTHON ERRORS:\nTraceback Info:\n' + tbinfo + \
                '\nError Info:\n    ' +  str(sys.exc_type)+ ': ' + \
                str(sys.exc_value) + '\n'
        print pymsg
        
def get_county( cty_code, st_code ):
    try:
        coDict = Dictionaries.countyFips
        stDict = Dictionaries.nbiStCodes
        p = str(st_code[:2])+str(cty_code)
        if st_code in stDict.keys():
            if p in coDict.keys():
                county = coDict[p]
            else:
                county = 'UNKNOWN'
        else:
            county = 'UNKNOWN'
        #print p
        return county
    except:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = ('PYTHON ERRORS:\nTraceback Info:\n' + tbinfo + 
                '\nError Info:\n    ' +  str(sys.exc_type)+ ': ' + 
                str(sys.exc_value) + '\n')
        print pymsg

def get_route_prefix( rt_prefix_code ):
    """
    Translates the route signing prefix numeric code to a valid
    description via a dictionary
    """
    rd = {1:'Interstate highway',
          2:'U.S. numbered highway',
          3:'State highway',
          4:'County highway',
          5:'City street',
          6:'Federal lands road',
          7:'State lands road',
          8:'Other'}
    if int(rt_prefix_code) in rd.keys():
        rt_type = rd[int(rt_prefix_code)]
    else:
        rt_type = 'Unknown'
    return rt_type

def get_level_service( svc_code ):
    """
    Translates the designated level of service code to a valid
    description via a dictionary
    """
    sd = {0:'Other',
          1:'Mainline',
          2:'Alternate',
          3:'Bypass',
          4:'Spur',
          6:'Business',
          7:'Ramp/Wye/Connector/etc.',
          8:'Service and/or unclassified frontage road'}
    if int(svc_code) in sd.keys():
        svc_level = sd[int(svc_code)]
    else:
        svc_level = 'Unknown'
    return svc_level

def get_direction( directional_code ):
    """
    Translates the directional suffix code to a valid description via a 
    dictionary
    """
    dir_d = {0:'Not applicable',
             1:'North',
             2:'East',
             3:'South',
             4:'West'}
    if int(directional_code) in dir_d.keys():
        direction = dir_d[int(directional_code)]
    else:
        direction = 'Unknown'
    return direction

##def get_place( place_code ):
##    """
##    Translates the concatenation of the state FIPS code and FIPS place code
##    to a valid FIPS place name
##    """
##    if place_code in fips_place_dict.fips_places.keys():
##        place_name = fips_place_dict.fips_places[place_code]
##    elif place_code[2:] == '00000':
##        place_name = 'Not applicable'
##    else:
##        place_name = 'Unknown - ' + place_code[2:]
##    return place_name

def get_toll( toll_code ):
    """
    
    """
    toll_dict = {1:'Toll bridge',
                 2:'On toll road',
                 3:'On free road',
                 4:'On Interstate toll segment',
                 5:'Toll bridge separate from highway segment'}
    if int(toll_code) in toll_dict.keys():
        toll_name = toll_dict[int(toll_code)]
    else:
        toll_name = 'Unknown'
    return  toll_name

def get_funct_cls( funct_code ):
    """
    
    """
    if len(funct_code) < 1:
        funct_code = '00'
    funct_dict = {'01':'Rural - Principal Arterial - Interstate',
                  '02':'Rural - Principal Arterial - Other',
                  '06':'Rural - Minor Arterial',
                  '07':'Rural - Major Collector',
                  '08':'Rural - Minor Collector',
                  '09':'Rural - Local',
                  '11':'Urban - Principal Arterial - Interstate',
                  '12':'Urban - Principal Arterial - Other Freeway or Expressway',
                  '14':'Urban - Other Principal Arterial',
                  '16':'Urban - Minor Arterial',
                  '17':'Urban - Collector',
                  '19':'Urban - Local'}
    if funct_code in funct_dict.keys():
        funct_name = funct_dict[funct_code]
    else:
        funct_name = 'Unknown'
    return funct_name

def get_maint_resp( maint_code ):
    """
    
    """
    if len(maint_code) < 1:
        maint_code = 00
    maint_dict = {01:'State Highway Agency',
                  02:'County Highway Agency',
                  03:'Town or Township Highway Agency',
                  04:'City or Municipal Highway Agency',
                  11:'State Park/Forest/Reservation Agency',
                  12:'Local Park/Forest/Reservation Agency',
                  21:'Other State Agencies',
                  25:'Other Local Agencies',
                  26:'Private (other than railroad)',
                  27:'Railroad',
                  31:'State Toll Authority',
                  32:'Local Toll Authority',
                  60:'Other Federal Agencies (not listed below)',
                  61:'Indian Tribal Government',
                  62:'Bureau of Indian Affairs',
                  63:'Bureau of Fish and Wildlife',
                  64:'U.S. Forest Service',
                  66:'National Park Service',
                  67:'Tennessee Valley Authority',
                  68:'Bureau of Land Management',
                  69:'Bureau of Reclamation',
                  70:'Corps of Engineers (Civil)',
                  71:'Corps of Engineers (Military)',
                  72:'Air Force',
                  73:'Navy/Marines',
                  74:'Army',
                  75:'NASA',
                  76:'Metropolitan Washington Airports Service',
                  80:'Unknown'}
    if int(maint_code) in maint_dict.keys():
        maint_name = maint_dict[int(maint_code)]
    else:
        maint_name = 'Unknown'
    return maint_name

def get_bridge_median( median_code ):
    """
    
    """
    if len(median_code) < 1:
        median_code = 00
    med_dict = {0:'No median',
                1:'Open median',
                2:'Closed median (no barrier)',
                3:'Closed median with non-mountable barriers'}
    if int(median_code) in med_dict.keys():
        median_name = med_dict[int(median_code)]
    else:
        median_name = 'Unknown'
    return median_name
        
def create_gdb_table( db, table, fields ):
    """
    Creates an empty standalone GDB table and adds field provided in a list 
    with a set schema. Field width is set for text fields.
    db:  Full path to database
    table:  Name of table we want to create
    fields:  List containing fields and size/type information
    """
    GpModules.KillObject(db + '/' + table)
    gp.CreateTable(db,table)
    for field in fields:
        if field[1] == 'TEXT':
            gp.AddField_management(db + '/' + table,field[0],field[1],"#","#",
               field[2],field[3],"NULLABLE","NON_REQUIRED","#")
        else:
            gp.AddField_management(db + '/' + table,field[0],field[1],"#","#",
               "#",field[3],"NULLABLE","NON_REQUIRED","#")

def main():
    rfile = open('//fayfiler/seecoapps/GIS/Projects/Bridges/NBI/AR07.txt') \
            .read().splitlines()  # raw input file
    wfile = open('//fayfiler/seecoapps/GIS/Projects/Bridges/NBI/AR07rw.txt', 
            'w')  # rewritten output file
    count = len(open('//fayfiler/seecoapps/GIS/Projects/Bridges/NBI/AR07.txt',
            'rU').readlines())
    print 'No. of lines -->',count

    try:
        for line in rfile:
            v0 = get_state( line[0:3].replace(',',' ') )   # state
            v1 = line[3:18].replace(',',' ').strip()       # structure number
            v2 = line[18:19].replace(',',' ').strip()      # record type
            v3 = get_route_prefix( line[19:20].
                                   replace(',',' ').strip() )  # rte prefix     
            v4 = get_level_service( line[20:21].
                                    replace(',',' ').strip() ) # level of svc
            v5 = line[21:26].replace(',',' ').strip()      # route number
            v6 = get_direction( line[26:27].
                                replace(',',' ').strip() ) # direct suffix
            v7 = line[27:29].replace(',',' ').strip()      # hwy agency dist
            v8 = get_county( line[29:32].replace(',',' '), 
                             line[0:3].replace(',',' ') )  # county              
            v9 = line[32:37].replace(',',' ').strip()      # place code  
            v10 = line[37:61].replace(',',' ').strip()     # feat intersected
            v11 = line[61:62].replace(',',' ').strip()     # crit fac indic
            v12 = line[62:80].replace(',',' ').strip()     # fac carried
            v13 = line[80:105].replace(',',' ').strip()    # location            
            v14 = line[105:109].replace(',',' ').strip()   # min vert clrance
            v15 = line[109:116].replace(',',' ').strip()   # kilometerpoint
            v16 = line[116:117].replace(',',' ').strip()   # base hwy netwk
            v17 = line[117:127].replace(',',' ').strip()   # LRS invtry rte
            v18 = line[127:129].replace(',',' ').strip()   # subrte number
            v19 = line[129:137].replace(',',' ').strip()   # lat dms
            v20 = v19[0:2]                                 # lat deg
            v21 = v19[2:4]                                 # lat min
            v22 = v19[4:6]+'.'+v19[6:8]                    # lat sec
            v23 = str(int(v20)+(float(v21)/60)+(float(v22)/3600))  # lat dd
            v24 = line[137:146].replace(',',' ').strip()   # lon dms
            v25 = v24[0:3]                                 # lon deg
            v26 = v24[3:5]                                 # lon min
            v27 = v24[5:7]+'.'+v24[7:9]                    # lon sec
            v28 = str('-'+str(int(v25)+(float(v26)/60)+ \
                      float(v27)/3600))                    # lon dd
            # detour len conv from km to mi
            if len(line[146:149].replace(',',' ').strip()) > 0:
                v29 = '%.1f' % (float(line[146:149].
                      replace(',',' ').
                      strip())*0.62137)
            else:
                v29 = ''
            v30 = get_toll( line[149:150].
                            replace(',',' ').strip() )     # toll
            v31 = get_maint_resp( line[150:152].
                                  replace(',',' ').strip() )  # maint responsb  
            v32 = get_maint_resp( line[152:154].
                                  replace(',',' ').strip() )  # owner          
            v33 = get_funct_cls( line[154:156].
                                 replace(',',' ').strip() )   # funct class    
            v34 = line[156:160].replace(',',' ').strip()   # year built
            v35 = line[160:162].replace(',',' ').strip()   # lanes on
            v36 = line[162:164].replace(',',' ').strip()   # lanes under       <<<
            # avg traffic
            if len(line[164:170].replace(',',' ').strip()) > 0:
                v37 = '%d' % (int(line[164:170].
                      replace(',',' ').strip()))
            else:
                v37 = ''
            v38 = line[170:174].replace(',',' ').strip()   # yr of avg traffic
            v39 = line[174:175].replace(',',' ').strip()   # design load
            # approach width
            if len(line[175:179].replace(',',' ').strip()) > 0:
                v40 = '%.1f' % (float(str(int(line[175:179].
                      replace(',',' ').strip()[0:3]))+'.'+
                      line[175:179].strip()[3:4])*0.62137)
            else:
                v40 = ''
            v41 = get_bridge_median( line[179:180].
                                     replace(',',' ').strip() ) # bridge median
            v42 = line[180:182].replace(',',' ').strip()   # skew
            v43 = line[182:183].replace(',',' ').strip()   # strux flared
            v44 = line[183:184].replace(',',' ').strip()   # bridge railings
            v45 = line[184:185].replace(',',' ').strip()   # transitions
            v46 = line[185:186].replace(',',' ').strip()   # approach gd-rail
            v47 = line[186:187].replace(',',' ').strip()   # app gr-rail ends
            v48 = line[187:188].replace(',',' ').strip()
            v49 = line[188:189].replace(',',' ').strip()
            v50 = line[189:193].replace(',',' ').strip()
            v51 = line[193:198].replace(',',' ').strip()
            v52 = line[198:199].replace(',',' ').strip()
            v53 = line[199:200].replace(',',' ').strip()
            v54 = line[200:201].replace(',',' ').strip()
            v55 = line[201:202].replace(',',' ').strip()
            v56 = line[202:204].replace(',',' ').strip()
            v57 = line[204:205].replace(',',' ').strip()
            v58 = line[205:207].replace(',',' ').strip()
            v59 = line[207:210].replace(',',' ').strip()
            v60 = line[210:214].replace(',',' ').strip()
            v61 = line[214:217].replace(',',' ').strip()
            v62 = line[217:222].replace(',',' ').strip()
            v63 = line[222:228].replace(',',' ').strip()
            v64 = line[228:231].replace(',',' ').strip()
            v65 = line[231:234].replace(',',' ').strip()
            v66 = line[234:238].replace(',',' ').strip()
            v67 = line[238:242].replace(',',' ').strip()
            v68 = line[242:246].replace(',',' ').strip()
            v69 = line[246:247].replace(',',' ').strip()
            v70 = line[247:251].replace(',',' ').strip()
            v71 = line[251:252].replace(',',' ').strip()
            v72 = line[252:255].replace(',',' ').strip()
            v73 = line[255:258].replace(',',' ').strip()
            v74 = line[258:259].replace(',',' ').strip()
            v75 = line[259:260].replace(',',' ').strip()
            v76 = line[260:261].replace(',',' ').strip()
            v77 = line[261:262].replace(',',' ').strip()
            v78 = line[262:263].replace(',',' ').strip()
            v79 = line[263:264].replace(',',' ').strip()
            v80 = line[264:267].replace(',',' ').strip()
            v81 = line[267:268].replace(',',' ').strip()
            v82 = line[268:271].replace(',',' ').strip()
            v83 = line[271:272].replace(',',' ').strip()
            v84 = line[272:273].replace(',',' ').strip()
            v85 = line[273:274].replace(',',' ').strip()
            v86 = line[274:275].replace(',',' ').strip()
            v87 = line[275:276].replace(',',' ').strip()
            v88 = line[276:277].replace(',',' ').strip()
            v89 = line[277:279].replace(',',' ').strip()
            v90 = line[279:280].replace(',',' ').strip()
            v91 = line[280:286].replace(',',' ').strip()
            v92 = line[286:290].replace(',',' ').strip()
            v93 = line[290:292].replace(',',' ').strip()
            v94 = line[292:295].replace(',',' ').strip()
            v95 = line[295:298].replace(',',' ').strip()
            v96 = line[298:301].replace(',',' ').strip()
            v97 = line[301:305].replace(',',' ').strip()
            v98 = line[305:309].replace(',',' ').strip()
            v99 = line[309:313].replace(',',' ').strip()
            v100 = line[313:319].replace(',',' ').strip()
            v101 = line[319:325].replace(',',' ').strip()
            v102 = line[325:331].replace(',',' ').strip()
            v103 = line[331:335].replace(',',' ').strip()
            v104 = line[335:338].replace(',',' ').strip()
            v105 = line[338:340].replace(',',' ').strip()
            v106 = line[340:355].replace(',',' ').strip()
            v107 = line[355:356].replace(',',' ').strip()
            v108 = line[356:357].replace(',',' ').strip()
            v109 = line[357:358].replace(',',' ').strip()
            v110 = line[358:359].replace(',',' ').strip()
            v111 = line[359:360].replace(',',' ').strip()
            v112 = line[360:361].replace(',',' ').strip()
            v113 = line[361:365].replace(',',' ').strip()
            v114 = line[365:366].replace(',',' ').strip()
            v115 = line[366:367].replace(',',' ').strip()
            v116 = line[367:368].replace(',',' ').strip()
            v117 = line[368:369].replace(',',' ').strip()
            v118 = line[369:371].replace(',',' ').strip()
            v119 = line[371:372].replace(',',' ').strip()
            v120 = line[372:373].replace(',',' ').strip()
            v121 = line[373:374].replace(',',' ').strip()
            v122 = line[374:375].replace(',',' ').strip()
            v123 = line[375:381].replace(',',' ').strip()
            v124 = line[381:385].replace(',',' ').strip()
            v125 = line[385:389].replace(',',' ').strip()
            v126 = line[390:391].replace(',',' ').strip()
            v127 = line[391:426].replace(',',' ').strip()
            v128 = line[426:427].replace(',',' ').strip()
            v129 = line[427:428].replace(',',' ').strip()
            v130 = line[428:432].replace(',',' ').strip()

            #l = ['v' + str(elem) for elem in range(123)]
            #newline = 'crap\n'
            newline = v0+','+v1+','+v2+','+v3+','+v4+','+v5+','+v6+','+ \
            v7+','+v8+','+v9+','+v10+','+v11+','+v12+','+v13+','+v14+','+ \
            v15+','+v16+','+v17+','+v18+','+v19+','+v20+','+v21+','+v22+','+ \
            v23+','+v24+','+v25+','+v26+','+v27+','+v28+','+v29+','+v30+','+ \
            v31+','+v32+','+v33+','+v34+','+v35+','+v36+','+v37+','+v38+','+ \
            v39+','+v40+','+v41+','+v42+','+v43+','+v44+','+v45+','+v46+','+ \
            v47+','+v48+','+v49+','+v50+','+v51+','+v52+','+v53+','+v54+','+ \
            v55+','+v56+','+v57+','+v58+','+v59+','+v60+','+v61+','+v62+','+ \
            v63+','+v64+','+v65+','+v66+','+v67+','+v68+','+v69+','+v70+','+ \
            v71+','+v72+','+v73+','+v74+','+v75+','+v76+','+v77+','+v78+','+ \
            v79+','+v80+','+v81+','+v82+','+v83+','+v84+','+v85+','+v86+','+ \
            v87+','+v88+','+v89+','+v90+','+v91+','+v92+','+v93+','+v94+','+ \
            v95+','+v96+','+v97+','+v98+','+v99+','+v100+','+v101+','+ \
            v102+','+v103+','+v104+','+v105+','+v106+','+v107+','+v108+','+ \
            v109+','+v110+','+v111+','+v112+','+v113+','+v114+','+v115+','+ \
            v116+','+v117+','+v118+','+v119+','+v120+','+v121+','+v122+','+ \
            v123+','+v124+','+v125+','+v126+','+v127+','+v128+','+v129+','+ \
            v130+'\n'
            
            wfile.write(newline)
        wfile.close()

        create_gdb_table( 'C:/Testing/Testing.gdb', 'ArBridges', flds )
        
        rows = gp.InsertCursor('C:/Testing/Testing.gdb/ArBridges')
        gdbFlds = [j[0] for j in flds]
        reader = csv.reader(open('F:/GIS/Projects/Bridges/NBI/AR07rw.txt',
                            'rU'))
        ln=0
        for line in reader:
            #print str(line)
            t = 0
            print 'Working on line:',str(ln)
            row = rows.NewRow()
            for gdbFld in gdbFlds:
                #print 't:',str(t)
                try:
                    if len(line[t].strip()) < 1:
                        val = None
                    else:
                        val = line[t].strip()
                    row.SetValue(gdbFld, val)
                except Exception,v:
                    traceback.print_exc()
                    print gp.GetMessages(2)
                t = t + 1
            rows.InsertRow(row)
            ln = ln + 1
            del t
            del row
        del rows
        #reader.close()
                
        end = time.clock()
        msg = '\n\n' + str(time.strftime('%I:%M:%S %p', time.localtime())) + \
              ':  Done! Process completed in ' + GpModules.Timer(start, end)
        print msg   

    except:
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = 'PYTHON ERRORS:\nTraceback Info:\n' + tbinfo + \
                '\nError Info:\n    ' +  str(sys.exc_type)+ ': ' + \
                str(sys.exc_value) + '\n'
        print pymsg
                
        msgs = 'GP ERRORS:\n' + gp.GetMessages(2) + '\n'
        print msgs
        
if __name__ == '__main__':
    main()