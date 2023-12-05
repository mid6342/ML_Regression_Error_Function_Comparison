# Python Project: Error Function Analysis in Machine Learning Regression

## Overview
This project explores three commonly used error functions in machine learning regression: Mean Absolute Error (MAE), Mean Squared Error (MSE), and the Huber Loss function. The focus is on evaluating these functions across different types of datasets to determine the most effective error function in various scenarios.

## Abstract
The project examines the application of MAE, MSE, and Huber Loss functions in machine learning regression. It involves creating datasets with different functions (linear, sine, polynomial of degree two and three) with applied noise, then mapping these using the error functions to identify the best fit. The analysis indicates similar performance across the error functions, with distinctions in cases of minimal error.

## Introduction
The project is part of a Python class assignment aimed at finding ideal functions by matching a training function with others, using the smallest sum of squared errors. This method is a key aspect of machine learning regression, used in scenarios like predicting stock prices or real estate values.

### Error Functions
- **Mean Squared Error (MSE):** Involves squaring the difference between two data points, with large errors significantly impacting the result.
- **Mean Absolute Error (MAE):** Calculates the absolute value of the difference between data points, less sensitive to large errors.
- **Huber Loss:** Combines MSE and MAE, using MSE for small errors and MAE for larger errors.

## Dataset Construction
The dataset includes 50 ideal functions and four training functions, manipulated slightly to challenge the error functions' differentiation capabilities. Functions include linear, sine, and polynomial (second and third degree), created using Excel's random number function for noise application.

## Results
Analysis of each function type (linear, sine, polynomial of degree two and three) with the error functions revealed:
- Consistent mapping of the ideal function by all error functions for linear and polynomial (second degree) functions.
- Variations in performance, particularly for the sine function and polynomial of degree three, where the error functions faced limitations in accurately mapping the ideal function.

## Conclusion
All error functions showed similar performance, with specific challenges in scenarios like the sine function and polynomial of degree three. The Huber Loss and Mean Squared Error emerged as slightly more effective overall, particularly in handling datasets with outliers.

## References
- Forsyth, D. (2019). Applied Machine Learning.
- Verdhan, V. (2020). Supervised Learning with Python.
