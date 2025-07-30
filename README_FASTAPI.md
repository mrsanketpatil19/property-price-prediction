# House Price Prediction FastAPI Web Application

A modern web application for predicting house prices using machine learning. Built with FastAPI, Bootstrap, and scikit-learn.

## 🏠 Features

- **Interactive Web Interface**: Beautiful, responsive web form for inputting property details
- **Real-time Predictions**: Instant house price predictions based on user input
- **REST API**: Simple API endpoint for programmatic access
- **Modern UI**: Clean, professional design with Bootstrap 5
- **Comprehensive Form**: All major property features included
- **Error Handling**: Robust error handling and validation

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## 🚀 Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Train the Model

Before running the web application, you need to train the model:

```bash
python train_model.py
```

This will create three files:
- `model.pkl` - The trained Ridge Regression model
- `scaler.pkl` - The feature scaler
- `feature_columns.pkl` - The feature column names

### 3. Run the Application

```bash
python app.py
```

Or using uvicorn directly:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Access the Application

Open your web browser and navigate to:
- **Web Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🌐 Web Interface

The web application provides a user-friendly form where users can input:

### Basic Information
- Building Class (1-story, 2-story, etc.)
- Zoning Class (Residential, Commercial, etc.)
- Lot Size (square feet)
- House Life (years since construction)

### Property Details
- House Type (Single Family, Duplex, etc.)
- House Design (1 Story, 2 Story, etc.)
- Overall Material Quality (1-10 scale)
- House Condition (1-9 scale)

### Areas and Sizes
- First Floor Area
- Second Floor Area
- Grade Living Area
- Garage Area

### Rooms and Bathrooms
- Bedrooms Above Grade
- Full/Half Bathrooms Above Grade
- Underground Bathrooms
- Total Rooms Above Grade

### Additional Features
- Neighborhood
- Foundation Type
- Kitchen Quality
- Number of Fireplaces

## 🔌 API Endpoints

### 1. Web Form Prediction
- **URL**: `POST /predict`
- **Content-Type**: `application/x-www-form-urlencoded`
- **Description**: Full form submission with all property features

### 2. Simple API Prediction
- **URL**: `GET /api/predict`
- **Parameters**:
  - `building_class` (int): Building class code
  - `lot_size` (int): Lot size in square feet
  - `overall_material` (int): Overall material quality (1-10)
  - `house_condition` (int): House condition (1-9)
  - `house_life` (int): Years since construction
  - `first_floor_area` (int): First floor area in square feet
  - `grade_living_area` (int): Grade living area in square feet
  - `garage_area` (int, optional): Garage area in square feet
  - `neighborhood` (str, optional): Neighborhood name
  - `house_type` (str, optional): House type
  - `foundation_type` (str, optional): Foundation type

### Example API Call

```bash
curl "http://localhost:8000/api/predict?building_class=60&lot_size=8500&overall_material=7&house_condition=5&house_life=15&first_floor_area=1200&grade_living_area=1500&garage_area=400"
```

Response:
```json
{
  "predicted_price": "$245,678.90",
  "predicted_price_raw": 245678.9,
  "input_features": {
    "Building_Class": 60,
    "Lot_Size": 8500,
    "Overall_Material": 7,
    "House_Condition": 5,
    "House_life": 15,
    "First_Floor_Area": 1200,
    "Grade_Living_Area": 1500,
    "Garage_Area": 400,
    "Neighborhood": "NAmes",
    "House_Type": "1Fam",
    "Foundation_Type": "PConc"
  }
}
```

## 🏗️ Project Structure

```
Property_Price_Prediction/
├── app.py                          # Main FastAPI application
├── train_model.py                  # Model training script
├── requirements.txt                # Python dependencies
├── Property_Price_Train.csv       # Training dataset
├── Data_description.txt           # Dataset description
├── House_Price_Prediction.ipynb   # Original Jupyter notebook
├── templates/
│   └── index.html                 # Web interface template
├── static/
│   ├── css/                       # CSS files
│   └── js/                        # JavaScript files
├── model.pkl                      # Trained model (generated)
├── scaler.pkl                     # Feature scaler (generated)
└── feature_columns.pkl            # Feature columns (generated)
```

## 🎯 Model Performance

The application uses a **Ridge Regression** model with the following performance metrics:
- **R² Score**: ~87.80%
- **RMSE**: ~22,886
- **MAE**: ~16,125

## 🔧 Customization

### Adding New Features

1. Update the form in `templates/index.html`
2. Add the feature to the prediction endpoint in `app.py`
3. Retrain the model using `train_model.py`

### Modifying the Model

1. Edit `train_model.py` to use a different algorithm
2. Run the training script again
3. The new model will be automatically loaded by the FastAPI app

### Styling Changes

1. Modify the CSS in `templates/index.html`
2. Add custom CSS files in `static/css/`
3. Update the template to reference new stylesheets

## 🐛 Troubleshooting

### Common Issues

1. **Model not loaded error**
   - Solution: Run `python train_model.py` first

2. **Port already in use**
   - Solution: Change the port in `app.py` or kill the existing process

3. **Missing dependencies**
   - Solution: Run `pip install -r requirements.txt`

4. **Dataset not found**
   - Solution: Ensure `Property_Price_Train.csv` is in the project directory

### Debug Mode

Run the application in debug mode for detailed error messages:

```bash
uvicorn app:app --reload --log-level debug
```

## 📊 Data Preprocessing

The application applies the same preprocessing steps as the original notebook:

1. **Data Cleaning**: Remove ID column, handle missing values
2. **Feature Engineering**: Create House_life feature, remove date columns
3. **Outlier Removal**: Remove outliers using Z-score method
4. **Feature Transformation**: Log and cube root transformations
5. **Encoding**: One-hot encoding for categorical variables
6. **Scaling**: StandardScaler for numerical features

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test the application
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 📞 Support

For questions or issues, please open an issue on the GitHub repository.

---

**Happy House Price Predicting! 🏠💰** 