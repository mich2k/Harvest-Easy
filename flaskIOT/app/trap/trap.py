"""
    status_attuale=1 #-->quando non ci sono istanze nella tabella
    
    bin_attuale=BinRecord.query.all()
    
    if(len(bin_attuale)>0): 
        status_attuale=bin_attuale[0].status
    
    riempimento_attuale=msgJson['riempimento']

    if(status_attuale==1 and float(riempimento_attuale)>=0.9): status_attuale=2
    if(status_attuale==3 and float(riempimento_attuale)>=0.9): status_attuale=4
    if(status_attuale==2 and float(riempimento_attuale)<0.9): status_attuale=1
    if(status_attuale==4 and float(riempimento_attuale)<0.9): status_attuale=3"""