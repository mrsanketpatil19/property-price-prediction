from setuptools import setup, find_packages

setup(
    name="house-price-prediction",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.95.2",
        "uvicorn==0.22.0",
        "pandas==1.5.3",
        "numpy==1.24.3",
        "scikit-learn==1.2.2",
        "python-multipart==0.0.6",
        "jinja2==3.1.2",
        "python-jose[cryptography]==3.3.0",
        "passlib[bcrypt]==1.7.4",
        "plotly==5.15.0",
    ],
    python_requires=">=3.9,<3.10",
) 