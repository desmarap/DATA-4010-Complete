# Inside the outside: Investigating urban canopy using point cloud

## How to Use

1. **Download the Data**
   - Download the `RGBPC.las` and `MSPC.las` point cloud files.
   - Download the Tree Inventory dataset provided by the University of Manitoba.

2. **Install Required Python Packages**
   ```bash
   pip install laspy numpy pandas scipy
   ```

3. **Install Required R Packages (in RStudio)**
   ```r
   install.packages("lidR")
   install.packages("dplyr")
   ```

4. **Install Software**
   - [CloudCompare](https://www.danielgm.net/cc/)
   - [QGIS](https://qgis.org/)

5. **Run the Scripts**
   - `Data4010-K-means.Rmd`: Performs K-means clustering on the RGB dataset (Done by Patrick Desmarais).
   - `MergedFile.py`: Merges `RGBPC.las` and `MSPC.las` into one dataset (Done by Garik Avagyan).
   - `Data4010-RF.Rmd`: Performs segmentation and classification on the merged dataset (Done by Garik Avagyan, Ha Uyen Tran, Patrick Desmarais).

6. **Visualize the Results**
   - The output files created by `Data4010-RF.Rmd` can be opened and visualized using CloudCompare and QGIS.
