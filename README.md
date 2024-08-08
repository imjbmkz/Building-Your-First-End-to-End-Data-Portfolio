# Building Your First End-to-End Data Portfolio
Hello! This is Josh Dev. In this series, we created an end-to-end data project that can be a good start for a data portfolio regardless if you are a beginner or an experienced data professional. This end-to-end project covers the major phases of a data project: from creation of data pipelines, visualizing and reporting data, and acquiring deeper insights.   

## Overview of the Project
![Alt text](/assets/images/diagram.png "Project Architecture Diagram")
This project covers the end-to-end business intelligence cycle. 
- The data engineering side covered development of a two-step data pipeline:
  - First step covers the extraction of data from online sources using Python and uploads the extracted files to an SFTP server
  - In the second step, the uploaded files in SFTP will be downloaded and loaded to the data warehouse
- An API has been developed in order to use the data extracted from the web to support compliance requirement for AML screening
- In the data analysis side of the project, an exploratory analysis has been conducted to the car sales dataset and visualized the results using Power BI
- In the data science part of the project, a simple linear regression model has been built to analyze the mtcars dataset and to derive relevant insights

## Episodes
1. Introduction and project overview ([recording](https://youtu.be/S9mVrof-bR8))
2. Version control and virtual environment essentials for data professionals ([recording](https://youtu.be/F5M4WZifOu0))
3. Extracting data to FTP using Python ([recording](https://youtu.be/j7fNG-V4aGE) | [project](/projects/3.%20Extracting%20data%20from%20web%20to%20FTP%20using%20Python/))
4. Loading CSV files from FTP to PostgreSQL using SSIS ([recording](https://youtu.be/m2DD-RvT-nA) | [project](/projects/4.%20Loading%20CSV%20files%20from%20FTP%20to%20PostgreSQL%20using%20SSIS/))
5. Developing screening API using FastAPI ([recording](https://www.youtube.com/live/QwxPWkWoU94?si=URTLbsLNBFEJjKXj) | | [project](/projects/5.%20Developing%20screening%20API%20using%20FastAPI/))
6. Data modeling and visualization using Power BI ([recording](https://youtu.be/0Y_DttINnBg?si=oJCWhNvYGVa-eK7I))
7. Supervised machine learning and regression analysis primer ([recording](https://youtu.be/IKqhdCGY40E?si=siu1uZ1dc0u5E-hs))
8. Creating a machine learning pipeline on house price dataset using sklearn
