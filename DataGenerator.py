import random
import ProcessFile
import os
import cv2
import numpy as np

from skimage.metrics import peak_signal_noise_ratio
from skimage.io import imread
def sobel_snr(bmp_file,bmp_file2):
    # Load image as grayscale
    """
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        raise ValueError("Error loading image. Check the file path!")

    # Compute signal power (mean squared pixel intensity)
    signal_power = np.mean(img ** 2)

    # Compute noise power (variance of pixel values)
    noise_power = np.var(img)

    # Compute SNR in decibels (dB)
    snr = 10 * np.log10(signal_power / noise_power)
    """

    img1 = imread(bmp_file)
    img2 = imread(bmp_file2)

    psnr_value = peak_signal_noise_ratio(img1, img2)

    return psnr_value



#this will need to be changed in the future
def ave8Error(arr1,arr2):
    # Calculate the absolute differences in frequencies
    total_error = 0
    for num1,num2 in zip(arr1,arr2):
        if num1 == 0:
            num1=.0000001
            num1=1
        if num2 ==0:
            num2=.0000001
            num2=1
        total_error+=abs((num1 - num2)/num2)
    #total_error = abs(count1[num1] - count2[num2]) for num1,num2 in zip(arr1,arr2)
    # Mean Absolute Error (MAE)
    mae = (total_error / len(arr1)) * 100
    return mae

def ave8File():
    arr_of_inputs=[]
    for i in range(1,30):
        arr_of_inputs.append(random.randrange(2, 40, i))
    with open("indata.txt",'w') as file:
        for i in arr_of_inputs:
            file.write(f"{i}\n")
    return arr_of_inputs


def add_avg_toFile(avg,input_file,output_file):
    
    constant_value = avg  # Change this to the value you want to add

    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        for line in infile:
            try:
                num = float(line.strip())  # Convert line to a number
                outfile.write(f"{num + constant_value}\n")  # Add constant and write
            except ValueError:
                outfile.write(line)  # Keep non-numeric lines unchanged

def sobelFileOUT(simulation_file_name , swap_text_file , compile_args,replacement_type):
     queue_of_files={}
     print(f"file: {simulation_file_name}")
     variable_name = simulation_file_name.split("FUNCNAME")[1]
     method_signature =simulation_file_name.split("FUNCNAME")[0]+"FUNCNAME" 

     varaiable_name_chars = list(variable_name)
     varaiable_name_chars = variable_name.replace("]","[").split("[")
     indexArr=[ "#"+f"{int(i)}"+"#" for i in varaiable_name_chars if i.isdigit()] #variable indexes
     index_string = ''.join(indexArr)

     variable_name = variable_name.split("[")[0]
     variable_name = variable_name.split("_testFile")[0]


     inputFile = f"{method_signature}{variable_name}_file{index_string}.itxt"


 
     variable_name = variable_name.split("_testFile.cpp")[0]
     #simulation_file_name = simulation_file_name.replace("[","#").replace("]","#")
     file_text_name=""
     if simulation_file_name.find("[") != -1:
         varaiable_fileName = simulation_file_name.replace("_testFile.cpp","").replace("[","#").replace("]","#")
         varaiable_fileName=varaiable_fileName.split("#")
         varaiable_fileName.insert(1,"_file")
         varaiable_fileName.insert(-1,".txt")
         for i in varaiable_fileName:
             if i.isdigit():
                 file_text_name+=f"#{i}#"
                 continue
             file_text_name+=i
     else:
         varaiable_fileName = simulation_file_name.replace("_testFile.cpp","_file.txt")
         file_text_name=varaiable_fileName


     print(f"cur file: {inputFile}")


     outputFile = "TemporaryOutput.bmp"
     #original_numbers=sobel_snr(outputFile)

     #original_numbers = ProcessFile.avg_and_std_deviation_of_file(outputFile)
     #original_numbers_avg = original_numbers[2]
     #original_numbers_std_dev = original_numbers[3]
     #try:
     #    original_numbers = original_numbers[-1]
     #except:
     #    return

    


    #compile  and run file
     bin_file_name = "temp"
    
     compile_args = f"{simulation_file_name} -std=c++20 -o{bin_file_name}.o -DC -w"
     os.system(f"./compile.sh {compile_args}")
    

     #test each potential swap file and detail their usefulness
     substitutions_to_consider = []
    
     if replacement_type == "V2V":
         for file in swap_text_file:
            if(file == inputFile.replace(".itxt",".txt")):
                continue
            #os.system(f"rm {outputFile}")
#            print("this is V2V")
#            print(f"file {file}")
#            print(f"input file {inputFile}")
            compared_nums_avg = ProcessFile.avg_and_std_deviation_of_file(file)[1]
            compared_nums_avg2 = ProcessFile.avg_and_std_deviation_of_file(file_text_name)[1]



            add_avg_toFile(compared_nums_avg-compared_nums_avg2,file,inputFile)
            #fileTooWrite = open(f"{inputFile}", "w") 
      
            #load data from otehr variable into this file
            #with open(f"{file}", "r") as scan: 
                #print(f" reading file: {inputFile} normal file: {file}")
            #    lines = scan.readlines()
            #    fileTooWrite.write(scan.read()) 

              
            # Closing the output file 
            #fileTooWrite.close()

            #run testprogram
            os.system(f"./{bin_file_name}.o")
            #new_numbers = ProcessFile.avg_and_std_deviation_of_file("outdata.txt")
            #new_numbers = sobel_snr("lenaout.bmp")
            new_numbers=0
            psnr = sobel_snr("lenaout.bmp",outputFile)




            #read file output
            
            
 #           print(new_numbers)
 #           print(f"{simulation_file_name}")
 #           print(f"{swap_text_file}")

            #compare with original
            #try:
            #if new_numbers == False:
             #   continue
            print(psnr)
            #new_numbers = new_numbers[-1]
            percentError = abs(psnr)
            #print(percentError)
            min_err = 20.0
            if percentError > min_err:
                print(percentError)
                print(f"{simulation_file_name} | {file} | {percentError}")
                print("Succesfully wrote to file")
                #queue_of_files.append((percentError,(simulation_file_name,file)))

                if simulation_file_name in queue_of_files:
                    queue_of_files[simulation_file_name].append((percentError,file))
                else:
                    queue_of_files[simulation_file_name]=[(percentError,file)]



            #except:
            #    print("Failed")
            #    print(file)
            #    continue
        
     else:#V2C
        print("this is V2C")
        #os.system(f"rm {outputFile}")
        
        fileTooWrite = open(f"{inputFile}", "w") 
        originalDataFile = f"{inputFile}".replace(".itxt",".txt")

        with open(f"{originalDataFile}", "r") as scan: 
            lines=scan.readlines()
            for line in lines:
                fileTooWrite.write(f"{replacement_type}\n") 

        fileTooWrite.close()

        os.system(f"./{bin_file_name}.o")

        new_numbers = ProcessFile.avg_and_std_deviation_of_file(outputFile)
        print(original_numbers_avg)
        print(original_numbers_std_dev)
        print(new_numbers[2])
        print(new_numbers[3])
        #compare with original
        try:
            new_numbers = new_numbers[-1]
            #numbers_precentage_change = ProcessFile.percentage_change(original_numbers,new_numbers)
            numbers_precentage_change = ave8Error(original_numbers,new_numbers)
            print(numbers_precentage_change)
            max_err = 20.0
            if numbers_precentage_change < max_err:
                with open(f"Testing{inputFile} with {simulation_file_name}", "w") as fileout:
                    for item in new_numbers:
                        fileout.write(f"{item}\n")  # Write each element on a new line
                print(numbers_precentage_change)
                print(f"Succesfully wrote to file Testing{inputFile} with {simulation_file_name}")
                print(f"Replace with const: {replacement_type}")
        except:
            pass




     return queue_of_files



def ave8FileOUT(simulation_file_name , swap_text_file , compile_args,replacement_type):
     queue_of_files={}
     print(f"file: {simulation_file_name}")
     variable_name = simulation_file_name.split("FUNCNAME")[1]
     method_signature =simulation_file_name.split("FUNCNAME")[0]+"FUNCNAME" 

     varaiable_name_chars = list(variable_name)
     varaiable_name_chars = variable_name.replace("]","[").split("[")
     indexArr=[ "#"+f"{int(i)}"+"#" for i in varaiable_name_chars if i.isdigit()] #variable indexes
     index_string = ''.join(indexArr)

     variable_name = variable_name.split("[")[0]
     variable_name = variable_name.split("_testFile")[0]


     inputFile = f"{method_signature}{variable_name}_file{index_string}.itxt"


 
     variable_name = variable_name.split("_testFile.cpp")[0]
     #simulation_file_name = simulation_file_name.replace("[","#").replace("]","#")
     file_text_name=""
     if simulation_file_name.find("[") != -1:
         varaiable_fileName = simulation_file_name.replace("_testFile.cpp","").replace("[","#").replace("]","#")
         varaiable_fileName=varaiable_fileName.split("#")
         varaiable_fileName.insert(1,"_file")
         varaiable_fileName.insert(-1,".txt")
         for i in varaiable_fileName:
             if i.isdigit():
                 file_text_name+=f"#{i}#"
                 continue
             file_text_name+=i
     else:
         varaiable_fileName = simulation_file_name.replace("_testFile.cpp","_file.txt")
         file_text_name=varaiable_fileName


     print(f"cur file: {inputFile}")


     outputFile = "TemporaryOutput"
     original_numbers = ProcessFile.avg_and_std_deviation_of_file(outputFile)
     original_numbers_avg = original_numbers[2]
     original_numbers_std_dev = original_numbers[3]
     try:
         original_numbers = original_numbers[-1]
     except:
         return

    


    #compile  and run file
     bin_file_name = "temp"
    
     compile_args = f"{simulation_file_name} -std=c++20 -o{bin_file_name}.o -DC -w"
     os.system(f"./compile.sh {compile_args}")
    

     #test each potential swap file and detail their usefulness
     substitutions_to_consider = []
    
     if replacement_type == "V2V":
         for file in swap_text_file:
            if(file == inputFile.replace(".itxt",".txt")):
                continue
            #os.system(f"rm {outputFile}")
#            print("this is V2V")
#            print(f"file {file}")
#            print(f"input file {inputFile}")
            compared_nums_avg = ProcessFile.avg_and_std_deviation_of_file(file)[1]
            compared_nums_avg2 = ProcessFile.avg_and_std_deviation_of_file(file_text_name)[1]



            add_avg_toFile(compared_nums_avg-compared_nums_avg2,file,inputFile)
            #fileTooWrite = open(f"{inputFile}", "w") 
      
            #load data from otehr variable into this file
            #with open(f"{file}", "r") as scan: 
                #print(f" reading file: {inputFile} normal file: {file}")
            #    lines = scan.readlines()
            #    fileTooWrite.write(scan.read()) 

              
            # Closing the output file 
            #fileTooWrite.close()

            #run testprogram
            os.system(f"./{bin_file_name}.o")
            new_numbers = ProcessFile.avg_and_std_deviation_of_file("outdata.txt")


            #read file output
            
            
 #           print(new_numbers)
 #           print(f"{simulation_file_name}")
 #           print(f"{swap_text_file}")

            #compare with original
            #try:
            if new_numbers == False:
                continue
            #print(new_numbers)
            new_numbers = new_numbers[-1]
            percentError = ProcessFile.mean_percentage_error(original_numbers,new_numbers)
            #print(percentError)
            max_err = 20.0
            if percentError < max_err:
                print(percentError)
                print(f"{simulation_file_name} | {file} | {percentError}")
                print("Succesfully wrote to file")
                #queue_of_files.append((percentError,(simulation_file_name,file)))

                if simulation_file_name in queue_of_files:
                    queue_of_files[simulation_file_name].append((percentError,file))
                else:
                    queue_of_files[simulation_file_name]=[(percentError,file)]



            #except:
            #    print("Failed")
            #    print(file)
            #    continue
        
     else:#V2C
        print("this is V2C")
        #os.system(f"rm {outputFile}")
        
        fileTooWrite = open(f"{inputFile}", "w") 
        originalDataFile = f"{inputFile}".replace(".itxt",".txt")

        with open(f"{originalDataFile}", "r") as scan: 
            lines=scan.readlines()
            for line in lines:
                fileTooWrite.write(f"{replacement_type}\n") 

        fileTooWrite.close()

        os.system(f"./{bin_file_name}.o")

        new_numbers = ProcessFile.avg_and_std_deviation_of_file(outputFile)
        print(original_numbers_avg)
        print(original_numbers_std_dev)
        print(new_numbers[2])
        print(new_numbers[3])
        #compare with original
        try:
            new_numbers = new_numbers[-1]
            #numbers_precentage_change = ProcessFile.percentage_change(original_numbers,new_numbers)
            numbers_precentage_change = ave8Error(original_numbers,new_numbers)
            print(numbers_precentage_change)
            max_err = 20.0
            if numbers_precentage_change < max_err:
                with open(f"Testing{inputFile} with {simulation_file_name}", "w") as fileout:
                    for item in new_numbers:
                        fileout.write(f"{item}\n")  # Write each element on a new line
                print(numbers_precentage_change)
                print(f"Succesfully wrote to file Testing{inputFile} with {simulation_file_name}")
                print(f"Replace with const: {replacement_type}")
        except:
            pass




     return queue_of_files
    #os.system(f"rm {bin_file_name}.o")



