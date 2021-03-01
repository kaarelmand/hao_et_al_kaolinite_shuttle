# The kaolinite shuttle: Linking the Great Oxidation and Lomagundi events

Code for parameter generation and data visualisation for the article "The kaolinite shuttle: Linking the Great Oxidation and Lomagundi events" by Weiduo Hao, Kaarel Mänd, Yuhao Li, Daniel S. Alessi, Peeter Somelar, Mathieu Moussavou, Alexander E. Romashkin, Aivo Lepland, Kalle Kirsimäe, Noah J. Planavsky, and Kurt O. Konhauser.

This is used to generate Figures 1 in the main manuscript and Figures S1, S4, S5, and S6 in the Supplementary Information file.

Further data analysis and visualisation (not in this repository) involved [Microsoft Excel](https://www.microsoft.com/en-us/microsoft-365/excel) and [Inkscape](https://inkscape.org/) software suites.

## Paleosols workflow

### Data stitching and parameter generation

The data is inputted in the Microsoft Excel spreadsheet `input_paleosols.xlsx`, which includes paleosol data seperated per source reference on different sheets, but using a unified table structure.
The ipython notebook `paleosol_unify.ipynb` then applies [`pandas`](https://github.com/pandas-dev/pandas), [`pyrolite`](https://github.com/morganjwilliams/pyrolite/), and [`mendeleev`](https://github.com/lmmentel/mendeleev) to stitch the data into a unified table with homogenised units, outputted as the spreadsheet `unified_paleosols.xlsx`.
For calculated chemical parameters, instead of only saving the calculated number, the cells are instead filled with Excel formulae referencing the inputted data.
This is done in order that the calculations could be vetted by colleagues not familiar with python.
This is done using the [`openpyxl`](https://foss.heptapod.net/openpyxl/openpyxl) package.

### Data visualisation

Data visualisation is done in the `paleosol_visualise.ipybn` notebook, referencing the `unified_paleosols.xlsx` spreadsheet.
Importantly, prior to running the `paleosol_visualise.ipybn` notebook, the .xlsx file will need to be opened and saved once in Microsoft Excel or Libreoffice Calc, in order that the formulae be evaluated and the results accessible to `pandas`.
Visualisation employs the [`matplotlib`](https://github.com/matplotlib/matplotlib), [`seaborn`](https://github.com/mwaskom/seaborn/), and [`python-ternary`](https://github.com/marcharper/python-ternary) packages and the figures are outputted in .svg and .png formats.

## Shale workflow

TO BE ADDED
