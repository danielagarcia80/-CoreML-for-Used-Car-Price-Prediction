# Special Topic: CoreML for Used Car Price Prediction

## Overview
This project explores the integration of **CoreML** into an iOS application to predict the price of a used car based on its attributes. By training a machine learning model using a dataset of used cars, we aim to develop an app in **SwiftUI** where users can input car details and receive an estimated price prediction.

## Project Goals
- Train a machine learning model using **CoreML tools** and a used car dataset.
- Convert and integrate the trained model into an **iOS app** using **SwiftUI**.
- Allow users to input car features (e.g., make, model, year, mileage, condition) and get a price estimate.

## Technologies Used
- **Python & CoreML Tools**: For training and converting the model.
- **Xcode & SwiftUI**: For developing the iOS app.
- **CoreML Framework**: For integrating the trained model into the app.

## Steps Involved
### 1. Data Collection & Preparation
- Obtain a **used car dataset** containing features such as:
  - Make, Model, Year
  - Mileage
  - Condition
  - Transmission Type
  - Fuel Type
  - Seller Type (Dealer/Private)
  - Price (Target variable)
- Clean and preprocess the dataset to remove missing or inconsistent values.

### 2. Model Training
- Use **scikit-learn** or **TensorFlow/Keras** to train a regression model.
- Convert the trained model to **CoreML format** using `coremltools`.
  
### 3. Integrating CoreML into SwiftUI
- Add the `.mlmodel` file to Xcode.
- Use **CoreML and Vision frameworks** to load the model in Swift.
- Create a SwiftUI form where users input car attributes.
- Use the model to predict and display the estimated price.

### 4. Testing & Optimization
- Test predictions with real-world data.
- Optimize the app for performance and efficiency.

## Expected Outcome
By the end of this project, we will have a fully functional **iOS application** that utilizes **machine learning** to predict used car prices, showcasing the power of CoreML in mobile applications.

## Future Enhancements
- Implement real-time model updates using online datasets.
- Add **image recognition** for predicting prices based on car photos.
- Deploy the app to the **App Store** with user-friendly UI enhancements.

---
### References
- **Apple CoreML Documentation**: [https://developer.apple.com/documentation/coreml](https://developer.apple.com/documentation/coreml)
- **CoreMLTools Library**: [https://pypi.org/project/coremltools/](https://pypi.org/project/coremltools/)
- **SwiftUI Guides**: [https://developer.apple.com/xcode/swiftui/](https://developer.apple.com/xcode/swiftui/)
- **Dataset Download**: https://www.kaggle.com/datasets/austinreese/craigslist-carstrucks-data?resource=download
- **CoreML Simple App Youtube Guide** https://www.youtube.com/watch?v=u1cSb4A7-YM&list=PLw-9a9yL-pt14ZOhrEUPzbMXrsX9EUjt7
