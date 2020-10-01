# power_solver (**Incomplete**)

* Simple linear solver ✅
* Newton-Rhapson 	❌
* Fast Decoupled 	❌
* Gauss-Seidel 	❌

***

# Installation

* Only tested on Python 3.8.1 and Windows 10. Adjustments such as changing **\\** to **/** if running on Bash etc must considered.

1. Create a virtual environment with [venv](https://docs.python.org/3/tutorial/venv.html) as follows:
```bash
virtualenv venv
```
2. Activate the environment:
```bash
venv\Scripts\activate.bat
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Run the solver:
```bash
python solver.py <name of file to parse>

Example: python solver.py examples/example_1.txt
```
* If no file name is given as an argument, the script will pick the first file in the `examples` folder