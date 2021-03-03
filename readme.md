
Time measurement with time.time() and time.process_time() on a simple function (foo())

1. main.py 
    Only show the time information  
    
    1) result/res_with_numpy.txt
    
        Show the time taken on foo() with different machines (Neon, Calumet and Laptop) 
        Here, foo() includes numpy array (mutliply two matrics)
         
    2) result/res_without_numpy.txt
    
        Show the time taken on foo() with different machines (Neon, Calumet and Laptop) 
        Here, foo() doesn't include any numpy array (just get the sum of numbers)
            
2. main_profile.py
    Show the profile and time information
    
    1) result/res_with_numpy_profile_neon.txt
        
        foo() includes numpy array 
    
    2) result/res_without_numpy_profile_neon.txt
        
        foo() doesn't include numpy array 
    
         
    


