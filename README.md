# Supply Chain Risk Management Simulator

An interactive web application for teaching supply chain risk management through Monte Carlo simulations and network visualization.

## Features

- **Interactive Network Visualization**: Visualize supply chain networks as nodes (suppliers, manufacturers, distributors, retailers) and arcs (flows)
- **Monte Carlo Simulations**: Run thousands of simulations to assess supply chain resilience under different risk scenarios
- **Risk Analysis Dashboard**: View statistical distributions, availability metrics, and disruption patterns
- **Customizable Parameters**: Adjust simulation count and risk levels (Low/Medium/High)
- **Export Results**: Download simulation data for further analysis

## Local Testing

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app locally:
```bash
streamlit run supply_chain_risk_app.py
```

3. Open your browser to `http://localhost:8501`

## Deployment to Streamlit Community Cloud

### Step 1: Prepare Your Repository

1. Create a GitHub account if you don't have one (github.com)

2. Create a new repository:
   - Go to github.com and click "New repository"
   - Name it (e.g., "supply-chain-risk-simulator")
   - Make it Public
   - Initialize with README (optional)

3. Upload your files to GitHub:
   - `supply_chain_risk_app.py`
   - `requirements.txt`
   - `README.md` (this file)

   You can do this via:
   - GitHub web interface (Upload files button)
   - Git command line
   - GitHub Desktop application

### Step 2: Deploy on Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)

2. Sign in with your GitHub account

3. Click "New app"

4. Configure your app:
   - **Repository**: Select your GitHub repository
   - **Branch**: main (or master)
   - **Main file path**: supply_chain_risk_app.py

5. Click "Deploy"

6. Wait a few minutes for deployment to complete

7. Your app will be live at: `https://[your-app-name].streamlit.app`

### Step 3: Share with Students

Once deployed, you can:
- Share the URL directly with students
- Embed it in your course management system
- Add it to your course website

## Customization Ideas

### Easy Modifications:
- Change network structure (add/remove nodes and connections)
- Adjust risk parameters (disruption probabilities, delay distributions)
- Add more metrics (cost impact, customer satisfaction)
- Change visualization colors and layout

### Advanced Extensions:
- Add user-uploaded network data (CSV/Excel)
- Implement different disruption scenarios (natural disasters, strikes, etc.)
- Add optimization algorithms for risk mitigation
- Include time-series analysis of disruptions
- Add machine learning for risk prediction

## App Structure

```
supply_chain_risk_app.py
├── Network Definition
│   └── create_supply_network() - Defines nodes, edges, and attributes
├── Monte Carlo Simulation
│   └── run_monte_carlo_simulation() - Simulates disruptions and calculates metrics
└── Three Main Tabs
    ├── Network Visualization - Interactive graph using Plotly
    ├── Risk Analysis - Statistical distributions and metrics
    └── Simulation Results - Detailed data table and download
```

## Teaching Applications

This app can be used to demonstrate:
- **Supply chain network design**: Understanding node types and relationships
- **Risk quantification**: Using Monte Carlo methods for uncertainty analysis
- **Resilience metrics**: Network availability, flow disruption, recovery time
- **Scenario analysis**: Comparing low/medium/high risk environments
- **Statistical analysis**: Interpreting distributions and percentiles
- **Decision making**: Using simulation results to inform strategy

## Technical Details

### Dependencies:
- **Streamlit**: Web app framework
- **NetworkX**: Graph/network analysis
- **Plotly**: Interactive visualizations
- **NumPy/Pandas**: Data manipulation
- **SciPy**: Statistical distributions

### Simulation Logic:
1. Each simulation randomly determines which nodes experience disruptions
2. Disruption probability varies by risk level (Low: 5%, Medium: 15%, High: 30%)
3. Delays follow a log-normal distribution
4. Metrics calculated: total delay, network availability, flow availability
5. Results aggregated across all simulations for statistical analysis

## Troubleshooting

### Common Issues:

**App won't start locally:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.8+)

**Deployment fails on Streamlit Cloud:**
- Verify requirements.txt is in root directory
- Check that file names match exactly (case-sensitive)
- Ensure repository is public

**Slow performance:**
- Reduce number of simulations (use slider)
- Streamlit Community Cloud has resource limits

## Updates and Maintenance

To update your deployed app:
1. Make changes to your code locally
2. Test locally with `streamlit run supply_chain_risk_app.py`
3. Commit and push changes to GitHub
4. Streamlit Cloud automatically redeploys (usually within 1-2 minutes)

## License

This educational tool is provided as-is for instructional purposes.

## Support

For Streamlit-specific questions:
- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Community Forum](https://discuss.streamlit.io)

## Contact

[Add your contact information or course details here]
