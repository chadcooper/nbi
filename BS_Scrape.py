import BeautifulSoup as bs
import urllib2, re

def FetchFipsCodes( ):
    """ Fetches a table of FIPS codes form a EPA webpage and tosses them
        into a dictionary """
    url = 'http://www.epa.gov/enviro/html/codes/state.html'
    f = open('C:/temp/python/data/outputs/fips.csv', 'w')
    
    # Fetch and parse the web page
    response = urllib2.urlopen(url)
    html = response.read()
    soup = bs.BeautifulSoup(html)
    
    # Find the table in the html code
    tbl = soup.findAll('table')
    # Setup a empty dictionary to use later
    d={}
    for table in tbl:
        # Find the table rows
        rows = table.findAll('tr')
        for tr in rows:
            # Find the table columns within each row
            cols = tr.findAll('td')
            # New list to store the columns contents in
            ls=[]
            for td in cols:   
                # Grab each cell value in the current row, toss it into the list
                # So you get ['AK','02','ALASKA']
                ls.append(td.find(text=True))
                # Write the row out to text file
                f.write(td.find(text=True) + ',')
            if len(ls) > 0:
                # Setup dictionary key and values
                key = ls[1]
                valAbbr = ls[0]
                valFull = ls[2]
                # Write the current line's cell values from list to dictionary
                d[key] = [valAbbr, valFull]
                # Write a newline to textfile
                f.write('\n')
    return d

if __name__ == '__main__':
    FetchFipsCodes()
            
