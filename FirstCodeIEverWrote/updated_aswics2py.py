    
def ASWICS2python():  
    '''This program reads in several files containing data from the GENESIS mission, and stores 
    them into a struct array. It takes 1 min, 13 seconds QQ.
    '''
    
    import numpy as np
    from numpy import array, save
        
        
    path = '/Users/andrewammons/Desktop/ACE_SWICS_1/'
    filename_ele = 'ACE_SWICS_2hr_1.1lv2_200'
    filename_eleNS = 'ACE_SWICS_1d_1.1lv2_98_11.txt'
    filename_q = 'ACE_qdist_2hr_1.1lv2_200'
    
    #Following is the struct array equivalent in function to the IDL structure.
    aswics = np.zeros((64), dtype = [('Names', 'S10'), ('Data', 'd')])
    aswics['Names'] = ['dnum', 'year', 'doy', 'he2o', 'c2o', 'n2o', 'ne2o', 'mg2o', 'si2o',
        's2o', 'fe2o', 'c56', 'o76', 'avq_c', 'avq_o', 'avq_fe', 'nhe',
        'vhe', 'vc5', 'vo6', 'vfe10', 'c4', 'c5', 'c6', 'o5', 'o6', 'o7',
        'o8', 'ne8', 'ne9', 'mg6', 'mg7', 'mg8', 'mg9', 'mg10', 'mg11',
        'mg12', 'si6', 'si7', 'si8', 'si9', 'si10', 'si11', 'si12', 'fe6',
        'fe7', 'fe8', 'fe9', 'fe10', 'fe11', 'fe12', 'fe13', 'fe14', 'fe15',
        'fe16', 'fe17', 'fe18', 'fe19', 'fe20', 'vthhe', 'vthc5', 'vtho6',
        'vthfe10', 'swtype'] 
    
    #the prerequisite to a matching solution (faster than my previous solution) **quick note**
    #(I'm writing this from the future) the method in which I used actually slows this whole
    #program down to about the length that your IDL program took, I really wanna mess 
    #around and see if I can get it back up to speed though.:
    file_ens = open(path + filename_eleNS)
    line_ens = file_ens.readline()
    while line_ens:
        line_ens += file_ens.readline()
        if 'BEGIN DATA' in line_ens:
            break
    line_ens = file_ens.readlines()
    file_ens.close()
    #Following is an alternative to my previous solution for iy = 1 to 4. I had been repelled by
    #it in the past, though it was because I used it wrong. It creates a whole number line, in this 
    #case specified as: "Creates 5 integers including 0, but called to start at '1', returning
    #a list of 1 to 4"
    iy = range(1,5)
    
    #the solution to the array tile size assignment calls for a variable value now.
    n = 1
    
    #I understand that you would prefer that there are no excess tile elements, but once again, I've 
    #read that this is the most efficient way, time-wise, to tile an array. I'll keep looking though.
    tile_index = 0
    for i in iy:
        year = 2000 + i
    
        #Once again, the following method is at least 3.5 times faster than anything else
        #I had been able to test.
        file_e = open(path + filename_ele + str(i) + '.txt')
        line_e = file_e.readline()
        while line_e:
            line_e += file_e.readline()
            if 'BEGIN DATA' in line_e:
                break
        line_e = file_e.readlines()
        e_len = len(line_e)
        file_e.close()
        
        file_q = open(path + filename_q + str(i) + '.txt')
        line_q = file_q.readline()
        while line_q:
            line_q += file_q.readline()
            if 'BEGIN DATA' in line_q:
                break
        line_q = file_q.readlines()
        q_len = len(line_q)
        file_q.close()
        
        
        index = 0
        
        #in the following, due to the assignment of data file length beforhand, we have
        #conveniently assigned the index limit as the greatest length value between our two main
        #files.
        
        while index != max(e_len,q_len):
            
            #This is the solution to generating an accurate size for the aswics_tile
            #the 'n' (number of tiles) will count up from n, to as many as needed.
            aswics_tile = np.tile(aswics,(n,1))
            
            #Add the corresponding year to all relavant struct arrays.
            aswics['Data'][1] = year
            
            if index >= e_len:
                ace_arr = np.zeros(70)
            else:
                ace_arr = array(line_e[index].split())
            aswics['Data'][np.array([2,16,17,18,19,20,59,60,61,62,11,12,13,14,15,3,4,6,7,8,10,13])] = ace_arr[np.array([6,8,10,15,20,25,11,16,21,26,33,36,39,42,45,58,61,64,67,70,55,54])]
    
            if index >= q_len:
                ace_arr = np.zeros(70)
            else:
                ace_arr = array(line_q[index].split())
            aswics['Data'][21:59] = ace_arr[8:46]
            
            #This loop reads each line in line_ens, a line starting with line_e[index][:8]
            #(current year, until doy) will be read to our struct array, I think this will solve
            #the issue which you described to me about matching, that is, if I understood it right.
            #As proud I am of this loop, it severely handicaps this program in the area of speed.
            #but if the shoe fits, wear it? I anticipate spending some time tweaking this program.
            for line in line_ens:
                if line.startswith(line_e[index][:8]):
                    ace_arr = array(line.split())
                    break
                    
            aswics['Data'][np.array([5,6])] = ace_arr[np.array([44,56])]
            
            #same old tile.
            aswics_tile[tile_index] = aswics
            n += 1
            
            index += 1
            tile_index += 1
    save('save_file_goes_here.npy',aswics_tile)
    return 'It has been done.'
            