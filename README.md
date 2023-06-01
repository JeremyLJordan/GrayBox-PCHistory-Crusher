<p align="center" width="100%">
    <img width="75%" src="https://i.imgur.com/eeQYb4K.png"> 
</p>




GrayBox PCHistory Crusher was created to process pchistory.txt files provided by GrayKey. The script can be manually configured with a multitude of arguments, or run simply with just the defaults. The script utilizes hashcat, which imported and installed automatically, to brute-force the hashed passcodes.





## Authors

- [@n3on_one](https://twitter.com/n3on_one) - Twitter



## Installation

Use pip to install requrirements 

```bash
pip -r install requirements.txt
```
    
## Usage/Examples
The only requirement for running with the default configuration is that the pchistory.txt file must be located in the directory where the gpc.py file is located. Then just run the script in PowerShell or the command prompt.
```python
py .\gpc.py
```

if you would rather provide arguments, it will look something like this. 


```python
py .\gpc.py -p 'C:\pchistory.txt' -arch gpu -agro 4 -o 'C:\temp\output.txt'
```
Note: All arguments are optional.

## Screenshots

![App Screenshot](https://i.imgur.com/PQpFQLL.png)


## Help
![help image](https://i.imgur.com/8NK3Yiw.png)

It is strongly recommended that you install NVIDIA CUDA to make Hashcat run smoothly. If you encounter any issues, verify it is installed before reporting an issue. It can be found here:

https://developer.nvidia.com/cuda-toolkit
## Acknowledgements
The idea for this project originated from [David Haddad's](https://www.linkedin.com/in/davidjhaddad) GK Password Parser project, which is designed for windows environments. You can download it here https://breakpointforensics.com/tools/

