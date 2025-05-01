# ApproxComputing
Approximates functions by profiling the code, storing its stack trace, and performing V2V(Variable to Variable) and V2C(Varaible to Constant) substitutions. [Read about it here](https://dl.acm.org/doi/10.1145/3453688.3461498)

The goal of this is to introduce error into a program in the effort to decrease its size. The main application of this is porting the generated code through high level sysnthesis. It allows the creation of a circuit that creates a similar output with signifcantly less resource usgae. 


| Original Image  | Original Image + Sobel Filter  | Image with 20db PSNR(Approximated) |
|--------|--------|--------|
| ![alt text](https://github.com/nurpy/ApproxComputing/blob/main/lena.bmp) | ![alt text](https://github.com/nurpy/ApproxComputing/blob/main/lena.bmp) |![alt text](https://github.com/nurpy/ApproxComputing/blob/main/lena.bmp) |
| ![alt text](https://github.com/nurpy/ApproxComputing/blob/main/luna.bmp) | ![alt text](https://github.com/nurpy/ApproxComputing/blob/main/TemporaryOutput.bmp) |![alt text](https://github.com/nurpy/ApproxComputing/blob/main/outluna.bmp)|

| Original Image + Sobel Filter  | Image with 20db PSNR(Approximated) |
|--------|--------|
| 100% Size | 53% Size|
