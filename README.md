cyanogenmod-finder
==================

Find download links of CyanogenMod package through http://oss.reflected.net/jenkins

###Requirements: 
run
```
pip install -r requirements.txt'
```
  
###Command: 
```bash
python find_cm.py [model] [output_file]
```

###Example: 

After running 
```bash
python find_cm.py i9100 cm_9100_links.txt
```
A file named cm_9100_links.txt containning download links of cm will apper in the current directory.

###Note:
To view the progress in real time:
```bash
tail -f [output_file]
```

###TO-DO:
* Prettify commandline output
* Add more commandline options   

<br />  
###LICENSE:
The MIT License (MIT)

Copyright (c) 2014 Calvin Chen

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
