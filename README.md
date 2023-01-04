# mkt-source-formatter
 
 Here's what you need to use this.

 - Raw `nabe/b` folder in this structure
 ```
 /Nabe
   /b
     <assets>
 ```
 No other folder otherwise this might not work.

 - Decompressed `nabe/b` folder in this structure

 ```
 /Nabe
   /b
     /<assets>
       <file>.wav
 ```

 Once you've selected those directories in the program, select an output directory. It is a good idea for this to be an empty folder, although it can be a previous output folder if you want to build off of it.

 Once you click start, it will read the catalog file, when it detects a file that exists in the raw nabe folder, it will copy that to `output/PCK`. Then it will try to copy the corresponding decompressed folder to `output/WAV`. If it fails, it'll just move on.
