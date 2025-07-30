import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pickle
import warnings
warnings.filterwarnings('ignore')

def train_and_save_model():
    """Train the Ridge Regression model and save it for the FastAPI app"""
    
    print("Loading dataset...")
    # Load the dataset
    df = pd.read_csv("Property_Price_Train.csv")
    
    print("Starting data preprocessing...")
    
    # Remove ID column
    df.drop("Id", axis=1, inplace=True)
    
    # Create House_life feature
    df["House_life"] = 2023 - df["Construction_Year"]
    
    # Remove date columns
    df.drop(["Construction_Year", "Remodel_Year", "Garage_Built_Year", "Month_Sold", "Year_Sold"], axis=1, inplace=True)
    
    # Handle missing values with meaningful categories
    missing_value_mappings = {
        'Lane_Type': 'No_Allay_Access',
        'Basement_Height': 'No_Basement',
        'Basement_Condition': 'No_Basement',
        'Exposure_Level': 'No_Basement',
        'BsmtFinType1': 'No_Basement',
        'BsmtFinType2': 'No_Basement',
        'Fireplace_Quality': 'No_Fireplace',
        'Garage': 'No_Garage',
        'Garage_Finish_Year': 'No_Garage',
        'Garage_Quality': 'No_Garage',
        'Garage_Condition': 'No_Garage',
        'Pool_Quality': 'No_Pool',
        'Fence_Quality': 'No_Fence'
    }
    
    for col, default_value in missing_value_mappings.items():
        df[col] = df[col].fillna(default_value)
    
    # Drop column with too many missing values
    df.drop("Miscellaneous_Feature", axis=1, inplace=True)
    
    # Impute remaining missing values
    def impute_null(data):
        for col in data.columns:
            if data[col].dtypes == 'int64' or data[col].dtypes == 'float64':
                data[col].fillna(data[col].mean(), inplace=True)
            else:
                data[col].fillna(data[col].value_counts().index[0], inplace=True)
    
    impute_null(df)
    
    # Convert discrete numerical to categorical
    discrete_cols = ['Garage_Size', 'Fireplaces', 'Rooms_Above_Grade', 'Bedroom_Above_Grade',
                     'Half_Bathroom_Above_Grade', 'Full_Bathroom_Above_Grade', 
                     'Underground_Half_Bathroom', 'Underground_Full_Bathroom', 
                     'House_Condition', 'Overall_Material', 'Building_Class']
    
    for col in discrete_cols:
        df[col] = df[col].astype('object')
    
    # Remove quasi-constant features
    quasi_constant_features = ['Road_Type', 'Utility_Type', 'Condition2', 'Roof_Quality', 
                              'Heating_Type', 'LowQualFinSF', 'Kitchen_Above_Grade', 
                              'Three_Season_Lobby_Area', 'Pool_Area', 'Pool_Quality', 'Miscellaneous_Value']
    
    for feature in quasi_constant_features:
        if feature in df.columns:
            df.drop(feature, axis=1, inplace=True)
    
    # Rename target variable
    df.rename(columns={'Sale_Price': 'tar_var'}, inplace=True)
    
    # Remove outliers from target variable
    z = np.abs(stats.zscore(df['tar_var']))
    threshold = 2.5
    outlier_indices = np.where(z > threshold)[0]
    df.drop(df.index[outlier_indices], inplace=True)
    
    print("Applying feature transformations...")
    
    # Separate numerical and categorical features
    df_num = df.select_dtypes(include=['int64', 'float64'])
    df_fac = df.select_dtypes(include=['object'])
    
    # Apply transformations to numerical features
    df_num["Lot_Extent"] = np.log(df_num["Lot_Extent"])
    df_num["Lot_Size"] = np.log(df_num["Lot_Size"])
    df_num["Brick_Veneer_Area"] = df_num["Brick_Veneer_Area"] ** (1/3)
    df_num["BsmtFinSF2"] = df_num["BsmtFinSF2"] ** (1/3)
    df_num["Screen_Lobby_Area"] = df_num["Screen_Lobby_Area"] ** (1/3)
    
    # Clip negative areas
    df_num['Garage_Area'] = df_num['Garage_Area'].clip(lower=0)
    df_num['W_Deck_Area'] = df_num['W_Deck_Area'].clip(lower=0)
    df_num['Open_Lobby_Area'] = df_num['Open_Lobby_Area'].clip(lower=0)
    df_num['Enclosed_Lobby_Area'] = df_num['Enclosed_Lobby_Area'].clip(lower=0)
    
    # Combine numerical and categorical data
    df_combined = pd.concat([df_num, df_fac], axis=1)
    
    # Separate target variable
    tar_var = df_combined['tar_var']
    df_combined.drop("tar_var", axis=1, inplace=True)
    
    # Create dummy variables
    df_encoded = pd.get_dummies(df_combined, drop_first=False)
    
    print("Training Ridge Regression model...")
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(df_encoded, tar_var, test_size=0.3, random_state=10)
    
    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Ridge Regression model
    model = Ridge()
    model.fit(X_train_scaled, y_train)
    
    # Evaluate the model
    train_score = model.score(X_train_scaled, y_train)
    test_score = model.score(X_test_scaled, y_test)
    
    print(f"Training R² Score: {train_score:.4f}")
    print(f"Testing R² Score: {test_score:.4f}")
    
    # Save the model, scaler, and feature columns
    print("Saving model and scaler...")
    
    with open("model.pkl", "wb") as f:
        pickle.dump(model, f)
    
    with open("scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)
    
    with open("feature_columns.pkl", "wb") as f:
        pickle.dump(df_encoded.columns.tolist(), f)
    
    print("Model training completed successfully!")
    print("Files saved: model.pkl, scaler.pkl, feature_columns.pkl")
    
    return model, scaler, df_encoded.columns.tolist()

if __name__ == "__main__":
    from scipy import stats
    train_and_save_model() 