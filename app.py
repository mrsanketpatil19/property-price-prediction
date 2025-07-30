from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
import pickle
import os
from typing import Optional
import uvicorn
import plotly.graph_objects as go
import plotly.express as px
import json
from io import BytesIO
import base64

app = FastAPI(title="House Price Prediction API", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Global variables for model and scaler
model = None
scaler = None
feature_columns = None

def load_model():
    """Load the trained model and scaler"""
    global model, scaler, feature_columns
    
    # Load the model
    if os.path.exists("model.pkl"):
        with open("model.pkl", "rb") as f:
            model = pickle.load(f)
    
    # Load the scaler
    if os.path.exists("scaler.pkl"):
        with open("scaler.pkl", "rb") as f:
            scaler = pickle.load(f)
    
    # Load feature columns
    if os.path.exists("feature_columns.pkl"):
        with open("feature_columns.pkl", "rb") as f:
            feature_columns = pickle.load(f)

@app.on_event("startup")
async def startup_event():
    """Initialize the model on startup"""
    load_model()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with overview and navigation"""
    return templates.TemplateResponse("home.html", {"request": request})



@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    """About page with project details"""
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/analytics", response_class=HTMLResponse)
async def analytics(request: Request):
    """Analytics page with interactive plots"""
    # Create sample data for plots
    sample_data = {
        'price_range': ['$100k-$200k', '$200k-$300k', '$300k-$400k', '$400k-$500k', '$500k+'],
        'count': [450, 380, 290, 180, 159],
        'avg_price': [150000, 250000, 350000, 450000, 600000]
    }
    
    # Create interactive plots
    price_distribution = create_price_distribution_plot()
    feature_importance = create_feature_importance_plot()
    model_comparison = create_model_comparison_plot()
    
    return templates.TemplateResponse("analytics.html", {
        "request": request,
        "price_distribution": price_distribution,
        "feature_importance": feature_importance,
        "model_comparison": model_comparison,
        "sample_data": sample_data
    })

@app.get("/predict", response_class=HTMLResponse)
async def predict_page(request: Request):
    """Prediction page with form"""
    return templates.TemplateResponse("predict.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict_price(
    request: Request,
    building_class: int = Form(...),
    zoning_class: str = Form(...),
    lot_extent: float = Form(...),
    lot_size: int = Form(...),
    lane_type: str = Form(...),
    property_shape: str = Form(...),
    land_outline: str = Form(...),
    lot_configuration: str = Form(...),
    property_slope: str = Form(...),
    neighborhood: str = Form(...),
    condition1: str = Form(...),
    house_type: str = Form(...),
    house_design: str = Form(...),
    overall_material: int = Form(...),
    house_condition: int = Form(...),
    house_life: int = Form(...),
    roof_design: str = Form(...),
    exterior1st: str = Form(...),
    exterior2nd: str = Form(...),
    brick_veneer_type: str = Form(...),
    brick_veneer_area: float = Form(...),
    exterior_material: str = Form(...),
    exterior_condition: str = Form(...),
    foundation_type: str = Form(...),
    basement_height: str = Form(...),
    basement_condition: str = Form(...),
    exposure_level: str = Form(...),
    bsmt_fin_type1: str = Form(...),
    bsmt_fin_sf1: int = Form(...),
    bsmt_fin_type2: str = Form(...),
    bsmt_fin_sf2: int = Form(...),
    bsmt_unf_sf: int = Form(...),
    total_basement_area: int = Form(...),
    heating_quality: str = Form(...),
    air_conditioning: str = Form(...),
    electrical_system: str = Form(...),
    first_floor_area: int = Form(...),
    second_floor_area: int = Form(...),
    grade_living_area: int = Form(...),
    underground_full_bathroom: int = Form(...),
    underground_half_bathroom: int = Form(...),
    full_bathroom_above_grade: int = Form(...),
    half_bathroom_above_grade: int = Form(...),
    bedroom_above_grade: int = Form(...),
    kitchen_quality: str = Form(...),
    rooms_above_grade: int = Form(...),
    functional_rate: str = Form(...),
    fireplaces: int = Form(...),
    fireplace_quality: str = Form(...),
    garage: str = Form(...),
    garage_finish_year: str = Form(...),
    garage_size: int = Form(...),
    garage_area: int = Form(...),
    garage_quality: str = Form(...),
    garage_condition: str = Form(...),
    paved_drive: str = Form(...),
    w_deck_area: int = Form(...),
    open_lobby_area: int = Form(...),
    enclosed_lobby_area: int = Form(...),
    screen_lobby_area: int = Form(...),
    fence_quality: str = Form(...),
    sale_type: str = Form(...),
    sale_condition: str = Form(...)
):
    """Predict house price based on input features"""
    
    if model is None or scaler is None or feature_columns is None:
        return templates.TemplateResponse(
            "predict.html", 
            {"request": request, "error": "Model not loaded. Please train the model first."}
        )
    
    try:
        # Create input data dictionary
        input_data = {
            'Building_Class': building_class,
            'Zoning_Class': zoning_class,
            'Lot_Extent': lot_extent,
            'Lot_Size': lot_size,
            'Lane_Type': lane_type,
            'Property_Shape': property_shape,
            'Land_Outline': land_outline,
            'Lot_Configuration': lot_configuration,
            'Property_Slope': property_slope,
            'Neighborhood': neighborhood,
            'Condition1': condition1,
            'House_Type': house_type,
            'House_Design': house_design,
            'Overall_Material': overall_material,
            'House_Condition': house_condition,
            'House_life': house_life,
            'Roof_Design': roof_design,
            'Exterior1st': exterior1st,
            'Exterior2nd': exterior2nd,
            'Brick_Veneer_Type': brick_veneer_type,
            'Brick_Veneer_Area': brick_veneer_area,
            'Exterior_Material': exterior_material,
            'Exterior_Condition': exterior_condition,
            'Foundation_Type': foundation_type,
            'Basement_Height': basement_height,
            'Basement_Condition': basement_condition,
            'Exposure_Level': exposure_level,
            'BsmtFinType1': bsmt_fin_type1,
            'BsmtFinSF1': bsmt_fin_sf1,
            'BsmtFinType2': bsmt_fin_type2,
            'BsmtFinSF2': bsmt_fin_sf2,
            'BsmtUnfSF': bsmt_unf_sf,
            'Total_Basement_Area': total_basement_area,
            'Heating_Quality': heating_quality,
            'Air_Conditioning': air_conditioning,
            'Electrical_System': electrical_system,
            'First_Floor_Area': first_floor_area,
            'Second_Floor_Area': second_floor_area,
            'Grade_Living_Area': grade_living_area,
            'Underground_Full_Bathroom': underground_full_bathroom,
            'Underground_Half_Bathroom': underground_half_bathroom,
            'Full_Bathroom_Above_Grade': full_bathroom_above_grade,
            'Half_Bathroom_Above_Grade': half_bathroom_above_grade,
            'Bedroom_Above_Grade': bedroom_above_grade,
            'Kitchen_Quality': kitchen_quality,
            'Rooms_Above_Grade': rooms_above_grade,
            'Functional_Rate': functional_rate,
            'Fireplaces': fireplaces,
            'Fireplace_Quality': fireplace_quality,
            'Garage': garage,
            'Garage_Finish_Year': garage_finish_year,
            'Garage_Size': garage_size,
            'Garage_Area': garage_area,
            'Garage_Quality': garage_quality,
            'Garage_Condition': garage_condition,
            'Pavedd_Drive': paved_drive,
            'W_Deck_Area': w_deck_area,
            'Open_Lobby_Area': open_lobby_area,
            'Enclosed_Lobby_Area': enclosed_lobby_area,
            'Screen_Lobby_Area': screen_lobby_area,
            'Fence_Quality': fence_quality,
            'Sale_Type': sale_type,
            'Sale_Condition': sale_condition
        }
        
        # Convert to DataFrame
        df = pd.DataFrame([input_data])
        
        # Apply the same preprocessing as in the notebook
        # Transform numerical features
        df['Lot_Extent'] = np.log(df['Lot_Extent'])
        df['Lot_Size'] = np.log(df['Lot_Size'])
        df['Brick_Veneer_Area'] = df['Brick_Veneer_Area'] ** (1/3)
        df['BsmtFinSF2'] = df['BsmtFinSF2'] ** (1/3)
        df['Screen_Lobby_Area'] = df['Screen_Lobby_Area'] ** (1/3)
        
        # Clip negative areas to 0
        df['Garage_Area'] = df['Garage_Area'].clip(lower=0)
        df['W_Deck_Area'] = df['W_Deck_Area'].clip(lower=0)
        df['Open_Lobby_Area'] = df['Open_Lobby_Area'].clip(lower=0)
        df['Enclosed_Lobby_Area'] = df['Enclosed_Lobby_Area'].clip(lower=0)
        
        # Convert discrete numerical to categorical
        discrete_cols = ['Garage_Size', 'Fireplaces', 'Rooms_Above_Grade', 'Bedroom_Above_Grade',
                        'Half_Bathroom_Above_Grade', 'Full_Bathroom_Above_Grade', 
                        'Underground_Half_Bathroom', 'Underground_Full_Bathroom', 
                        'House_Condition', 'Overall_Material', 'Building_Class']
        
        for col in discrete_cols:
            if col in df.columns:
                df[col] = df[col].astype('object')
        
        # Create dummy variables
        df_encoded = pd.get_dummies(df, drop_first=False)
        
        # Align columns with training data - optimized to avoid fragmentation
        missing_cols = [col for col in feature_columns if col not in df_encoded.columns]
        if missing_cols:
            # Create a DataFrame with missing columns and concatenate
            missing_df = pd.DataFrame(0, index=df_encoded.index, columns=missing_cols)
            df_encoded = pd.concat([df_encoded, missing_df], axis=1)
        
        df_encoded = df_encoded[feature_columns]
        
        # Scale the features
        df_scaled = scaler.transform(df_encoded)
        
        # Make prediction
        prediction = model.predict(df_scaled)[0]
        
        return templates.TemplateResponse(
            "predict.html", 
            {
                "request": request, 
                "prediction": f"${prediction:,.2f}",
                "input_data": input_data
            }
        )
        
    except Exception as e:
        return templates.TemplateResponse(
            "predict.html", 
            {"request": request, "error": f"Error making prediction: {str(e)}"}
        )

@app.get("/api/predict")
async def predict_api(
    building_class: int,
    lot_size: int,
    overall_material: int,
    house_condition: int,
    house_life: int,
    first_floor_area: int,
    grade_living_area: int,
    garage_area: int = 0,
    neighborhood: str = "NAmes",
    house_type: str = "1Fam",
    foundation_type: str = "PConc"
):
    """Simple API endpoint for basic predictions"""
    
    if model is None:
        return {"error": "Model not loaded"}
    
    try:
        # Create minimal input for API
        input_data = {
            'Building_Class': building_class,
            'Lot_Size': lot_size,
            'Overall_Material': overall_material,
            'House_Condition': house_condition,
            'House_life': house_life,
            'First_Floor_Area': first_floor_area,
            'Grade_Living_Area': grade_living_area,
            'Garage_Area': garage_area,
            'Neighborhood': neighborhood,
            'House_Type': house_type,
            'Foundation_Type': foundation_type
        }
        
        # Add default values for required features
        default_values = {
            'Zoning_Class': 'RL', 'Lot_Extent': 60.0, 'Lane_Type': 'Grvl',
            'Property_Shape': 'Reg', 'Land_Outline': 'Lvl', 'Lot_Configuration': 'Inside',
            'Property_Slope': 'Gtl', 'Condition1': 'Norm', 'House_Design': '1Story',
            'Roof_Design': 'Gable', 'Exterior1st': 'VinylSd', 'Exterior2nd': 'VinylSd',
            'Brick_Veneer_Type': 'None', 'Brick_Veneer_Area': 0.0, 'Exterior_Material': 'VinylSd',
            'Exterior_Condition': 'TA', 'Basement_Height': 'TA', 'Basement_Condition': 'TA',
            'Exposure_Level': 'No', 'BsmtFinType1': 'GLQ', 'BsmtFinSF1': 0,
            'BsmtFinType2': 'Unf', 'BsmtFinSF2': 0, 'BsmtUnfSF': 0, 'Total_Basement_Area': 0,
            'Heating_Quality': 'TA', 'Air_Conditioning': 'N', 'Electrical_System': 'SBrkr',
            'Second_Floor_Area': 0, 'Underground_Full_Bathroom': 0, 'Underground_Half_Bathroom': 0,
            'Full_Bathroom_Above_Grade': 1, 'Half_Bathroom_Above_Grade': 0, 'Bedroom_Above_Grade': 3,
            'Kitchen_Quality': 'TA', 'Rooms_Above_Grade': 6, 'Functional_Rate': 'Typ',
            'Fireplaces': 0, 'Fireplace_Quality': 'No_Fireplace', 'Garage': 'Attchd',
            'Garage_Finish_Year': 'Unf', 'Garage_Size': 2, 'Garage_Quality': 'TA',
            'Garage_Condition': 'TA', 'Pavedd_Drive': 'Y', 'W_Deck_Area': 0,
            'Open_Lobby_Area': 0, 'Enclosed_Lobby_Area': 0, 'Screen_Lobby_Area': 0,
            'Fence_Quality': 'No_Fence', 'Sale_Type': 'WD', 'Sale_Condition': 'Normal'
        }
        
        input_data.update(default_values)
        
        # Convert to DataFrame and process
        df = pd.DataFrame([input_data])
        
        # Apply transformations
        df['Lot_Extent'] = np.log(df['Lot_Extent'])
        df['Lot_Size'] = np.log(df['Lot_Size'])
        df['Brick_Veneer_Area'] = df['Brick_Veneer_Area'] ** (1/3)
        df['BsmtFinSF2'] = df['BsmtFinSF2'] ** (1/3)
        df['Screen_Lobby_Area'] = df['Screen_Lobby_Area'] ** (1/3)
        
        # Convert discrete numerical to categorical
        discrete_cols = ['Garage_Size', 'Fireplaces', 'Rooms_Above_Grade', 'Bedroom_Above_Grade',
                        'Half_Bathroom_Above_Grade', 'Full_Bathroom_Above_Grade', 
                        'Underground_Half_Bathroom', 'Underground_Full_Bathroom', 
                        'House_Condition', 'Overall_Material', 'Building_Class']
        
        for col in discrete_cols:
            if col in df.columns:
                df[col] = df[col].astype('object')
        
        # Create dummy variables
        df_encoded = pd.get_dummies(df, drop_first=False)
        
        # Align columns with training data - optimized to avoid fragmentation
        if feature_columns is not None:
            missing_cols = [col for col in feature_columns if col not in df_encoded.columns]
            if missing_cols:
                # Create a DataFrame with missing columns and concatenate
                missing_df = pd.DataFrame(0, index=df_encoded.index, columns=missing_cols)
                df_encoded = pd.concat([df_encoded, missing_df], axis=1)
            df_encoded = df_encoded[feature_columns]
        
        # Scale and predict
        if scaler is not None:
            df_scaled = scaler.transform(df_encoded)
            prediction = model.predict(df_scaled)[0]
        else:
            prediction = model.predict(df_encoded)[0]
        
        return {
            "predicted_price": f"${prediction:,.2f}",
            "predicted_price_raw": prediction,
            "input_features": input_data
        }
        
    except Exception as e:
        return {"error": str(e)}

def create_price_distribution_plot():
    """Create modern price distribution plot"""
    # Sample price data with more realistic distribution
    prices = np.random.normal(180000, 80000, 1000)
    prices = np.clip(prices, 50000, 500000)
    
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=prices,
        nbinsx=30,
        name="Price Distribution",
        marker=dict(
            color='rgba(102, 126, 234, 0.8)',
            line=dict(color='rgba(102, 126, 234, 1)', width=1)
        ),
        hovertemplate='<b>Price Range:</b> %{x}<br><b>Count:</b> %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text="Distribution of House Prices",
            font=dict(size=24, color='#2d3748', family='Inter'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title=dict(text="Price ($)", font=dict(size=16, color='#4a5568')),
            gridcolor='rgba(0,0,0,0.1)',
            zerolinecolor='rgba(0,0,0,0.2)',
            showgrid=True,
            gridwidth=1
        ),
        yaxis=dict(
            title=dict(text="Number of Properties", font=dict(size=16, color='#4a5568')),
            gridcolor='rgba(0,0,0,0.1)',
            zerolinecolor='rgba(0,0,0,0.2)',
            showgrid=True,
            gridwidth=1
        ),
        plot_bgcolor='rgba(255,255,255,0.9)',
        paper_bgcolor='rgba(255,255,255,0.9)',
        font=dict(family='Inter', size=14, color='#2d3748'),
        margin=dict(l=60, r=60, t=80, b=60),
        showlegend=False,
        hoverlabel=dict(
            bgcolor='rgba(255,255,255,0.95)',
            bordercolor='rgba(102, 126, 234, 0.5)',
            font=dict(size=12, color='#2d3748')
        )
    )
    
    return fig.to_html(full_html=False, include_plotlyjs=False)

def create_feature_importance_plot():
    """Create modern feature importance plot"""
    features = ['Lot Size', 'Overall Quality', 'Year Built', 'Total Area', 'Garage Area', 
                'Basement Area', 'Bathrooms', 'Bedrooms', 'Kitchen Quality', 'Foundation']
    importance = [0.25, 0.22, 0.18, 0.15, 0.08, 0.06, 0.03, 0.02, 0.01, 0.01]
    
    # Create gradient colors based on importance
    colors = [f'rgba({int(255 - imp * 1000)}, {int(100 + imp * 500)}, {int(50 + imp * 200)}, {0.7 + imp * 0.3})' 
              for imp in importance]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=importance,
        y=features,
        orientation='h',
        name="Feature Importance",
        marker=dict(
            color=colors,
            line=dict(color='rgba(255,255,255,0.8)', width=1)
        ),
        hovertemplate='<b>%{y}</b><br><b>Importance:</b> %{x:.3f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text="Most Important Features",
            font=dict(size=24, color='#2d3748', family='Inter'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title=dict(text="Importance Score", font=dict(size=16, color='#4a5568')),
            gridcolor='rgba(0,0,0,0.1)',
            zerolinecolor='rgba(0,0,0,0.2)',
            showgrid=True,
            gridwidth=1,
            range=[0, 0.3]
        ),
        yaxis=dict(
            title=dict(text="Features", font=dict(size=16, color='#4a5568')),
            gridcolor='rgba(0,0,0,0.1)',
            zerolinecolor='rgba(0,0,0,0.2)',
            showgrid=False
        ),
        plot_bgcolor='rgba(255,255,255,0.9)',
        paper_bgcolor='rgba(255,255,255,0.9)',
        font=dict(family='Inter', size=14, color='#2d3748'),
        margin=dict(l=60, r=60, t=80, b=60),
        showlegend=False,
        hoverlabel=dict(
            bgcolor='rgba(255,255,255,0.95)',
            bordercolor='rgba(102, 126, 234, 0.5)',
            font=dict(size=12, color='#2d3748')
        )
    )
    

    
    return fig.to_html(full_html=False, include_plotlyjs=False)

def create_model_comparison_plot():
    """Create modern model comparison plot"""
    models = ['Linear Regression', 'Ridge Regression', 'Lasso Regression', 'Elastic Net']
    r2_scores = [0.85, 0.878, 0.865, 0.836]
    rmse_scores = [28000, 22886, 24097, 26528]
    
    # Create gradient colors based on performance
    colors = ['#e53e3e', '#38a169', '#d69e2e', '#805ad5']  # Red, Green, Yellow, Purple
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='R² Score',
        x=models,
        y=r2_scores,
        marker=dict(
            color=colors,
            line=dict(color='rgba(255,255,255,0.8)', width=2)
        ),
        hovertemplate='<b>%{x}</b><br><b>R² Score:</b> %{y:.3f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text="Model Performance Comparison",
            font=dict(size=24, color='#2d3748', family='Inter'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title=dict(text="Models", font=dict(size=16, color='#4a5568')),
            gridcolor='rgba(0,0,0,0.1)',
            zerolinecolor='rgba(0,0,0,0.2)',
            showgrid=False,
            tickangle=-45
        ),
        yaxis=dict(
            title=dict(text="R² Score", font=dict(size=16, color='#4a5568')),
            gridcolor='rgba(0,0,0,0.1)',
            zerolinecolor='rgba(0,0,0,0.2)',
            showgrid=True,
            gridwidth=1,
            range=[0.8, 0.9]
        ),
        plot_bgcolor='rgba(255,255,255,0.9)',
        paper_bgcolor='rgba(255,255,255,0.9)',
        font=dict(family='Inter', size=14, color='#2d3748'),
        margin=dict(l=60, r=60, t=80, b=80),
        showlegend=False,
        hoverlabel=dict(
            bgcolor='rgba(255,255,255,0.95)',
            bordercolor='rgba(102, 126, 234, 0.5)',
            font=dict(size=12, color='#2d3748')
        )
    )
    

    
    return fig.to_html(full_html=False, include_plotlyjs=False)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 