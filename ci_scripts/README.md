# CI scripts

**upload_file.py** - can upload one file to pythonanywhere.com, relative to user's home directory

    $ pip3 install requests --user
    $ export PYTHON_API_KEY=<APIKey>
    $ export PYTHON_USERNAME=<username>
    $ python3 upload_file.py <SourceFilePath> <DestinationFilePath> 
    
**file_list.txt** - list of files to upload

    <source file> <dst file>
    <source file> <dst file>
