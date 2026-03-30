from setuptools import setup, find_packages

setup(
    name="hotel-intelligence-platform",
    version="0.1.0",
    author="Mehmet Işık",
    description="End-to-end AI/ML platform for hospitality analytics",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mmehmetisik/hotel-intelligence-platform",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.11",
    install_requires=[
        "pandas>=2.0",
        "numpy>=1.24",
        "scikit-learn>=1.3",
        "xgboost>=2.0",
        "lightgbm>=4.0",
        "streamlit>=1.30",
        "mlflow>=2.10",
        "plotly>=5.18",
        "groq>=0.4",
    ],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
