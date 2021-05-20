# The kaolinite shuttle links the Great Oxidation and Lomagundi events

Code for geochemical index calculation and data visualisation for the article "The kaolinite shuttle links the Great Oxidation and Lomagundi events" by Weiduo Hao, Kaarel Mänd, Yuhao Li, Daniel S. Alessi, Peeter Somelar, Mathieu Moussavou, Alexander E. Romashkin, Aivo Lepland, Kalle Kirsimäe, Noah J. Planavsky, and Kurt O. Konhauser, published in [Nature Communications](https://doi.org/10.1038/s41467-021-23304-8).

This is used to generate Figures 1 in the main manuscript and Figures S1, S4, S5, and S6 in the Supplementary Information file.

Further data analysis and visualisation (not in this repository) involved [Microsoft Excel](https://www.microsoft.com/en-us/microsoft-365/excel) and [Inkscape](https://inkscape.org/) software suites.

## Paleosols workflow

### Data stitching and index generation

The data is read in from the Microsoft Excel spreadsheet `input_data/input_paleosols.xlsx`, which contains paleosol data separated on different sheets per source reference, but using a semi-unified table structure.
The ipython notebook `paleosol_unify.ipynb` then applies [pandas](https://github.com/pandas-dev/pandas), [pyrolite](https://github.com/morganjwilliams/pyrolite/), and [mendeleev](https://github.com/lmmentel/mendeleev) to stitch the data into a single table with homogenised units, saved as the spreadsheet `unified_paleosols.xlsx`.
For chemical indices, instead of saving only the calculated number, the cells are filled with Excel formulae referencing the stitched data to enable vetting by non-python-users.
This is done with the [openpyxl](https://foss.heptapod.net/openpyxl/openpyxl) package.

### Data visualisation

Data visualisation happens in the `paleosol_visualise.ipybn` notebook, referencing the `unified_paleosols.xlsx` spreadsheet.
Importantly, prior to running the `paleosol_visualise.ipybn` notebook, the .xlsx file will need to be opened and saved once in Microsoft Excel or Libreoffice Calc, in order that the formulae be evaluated and the results accessible to pandas.
Visualisation employs the [matplotlib](https://github.com/matplotlib/matplotlib), [seaborn](https://github.com/mwaskom/seaborn/), and [python-ternary](https://github.com/marcharper/python-ternary) packages and the figures are saved as 350-dpi .png files in the `figures` folder.

## Shale XRD workflow

Shale mineralogical data is collected from spreadsheets `input_data/franceville_xrd.csv` and `input_data/onega_xrd.xlsx` with pandas, then visualised using matplotlib in the `lithosection_visualise.ipynb` notebook.
Both lithological columns and legend are present in the `franceville_litho.png`, `onega_litho.png`, and `litho_legend.png` files, respectively.

## Titration workflow

Visualisation of kaolinite titration data in the `titration_visualise.ipynb` notebook works off of the `titration_ca-cb.csv` and `titration_logK.csv` files in the `input_data` folder with the help of pandas and matplotlib.
