import zipfile
import os
from shutil import copyfile, rmtree

dirName = 'results'
if not os.path.exists(dirName):
    os.mkdir(dirName)
    print("Directory " , dirName ,  " Created ")
else:    
    print("Directory " , dirName ,  " already exists")


for file in os.listdir("./"): # home of annotation
    if file.endswith(".zip"):
        unzip_file = file.replace('.zip', '')
        print('Processing zip file: ', file)
#         print(unzip_file)
        zip_ref = zipfile.ZipFile(file, 'r')
        zip_ref.extractall(unzip_file)
        zip_ref.close()
        
        wkdir = "./" + unzip_file + '/curation/' 
#         print (wkdir)
        for sub_file in os.listdir(wkdir): # individual annotion outcome, and use this as new of file 
            for zip_file in os.listdir(wkdir + '/' + sub_file):
                if zip_file.endswith(".zip"):
                    zip_ref = zipfile.ZipFile(wkdir + '/' + sub_file + '/' + zip_file, 'r')
                    zip_ref.extractall(wkdir + '/' + sub_file)
                    zip_ref.close()
                    copyfile(wkdir + '/' + sub_file + '/CURATION_USER.xmi', dirName + '/' + sub_file +  '.xml')
        rmtree(unzip_file)      