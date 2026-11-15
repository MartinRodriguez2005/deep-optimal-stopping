

# Deep Optimal Stopping

A quantitative finance project exploring numerical methods for derivative pricing and optimal stopping problems, combining stochastic simulation, analytical pricing, Monte Carlo methods and deep learning.

## Project Structure

```text
deep-optimal-stopping/
├── app/
│   ├── Home.py
│   └── pages/
│       ├── 1_GBM_Simulation.py
│       └── 2_Analytical_Pricing.py
├── src/
│   ├── algorithms/
│   ├── evaluation/
│   ├── models/
│   ├── pricing/
│   └── simulation/
├── tests/
├── docs/
├── experiments/
├── notebooks/
├── pyproject.toml
└── requirements.txt
```

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd deep-optimal-stopping
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
pip install -e .
```

## Run the Application

Launch the Streamlit interface from the project root:

```bash
streamlit run app/Home.py
```

## Testing

Run the test suite with:

```bash
python -m pytest -v
```

## Technologies

- Python
- NumPy and SciPy
- Pandas
- Plotly
- PyTorch
- Streamlit
- Pytest

## Development Roadmap

- [x] Geometric Brownian Motion simulation
- [x] Black–Scholes analytical pricing
- [x] Forward pricing and valuation
- [ ] Monte Carlo option pricing
- [ ] Longstaff–Schwartz algorithm
- [ ] Deep Optimal Stopping
- [ ] Numerical benchmarking and model evaluation

