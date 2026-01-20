import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import networkx as nx
from scipy import stats

# Page configuration
st.set_page_config(page_title="Supply Chain Risk Simulator", layout="wide")

st.title("🔗 Supply Chain Risk Management Simulator")
st.markdown("### Monte Carlo Simulation for Network Resilience Analysis")

# Sidebar for simulation parameters
st.sidebar.header("Simulation Parameters")
num_simulations = st.sidebar.slider("Number of Monte Carlo Simulations", 100, 10000, 1000, 100)
risk_level = st.sidebar.selectbox("Overall Risk Level", ["Low", "Medium", "High"])

# Define risk parameters based on selection
risk_params = {
    "Low": {"disruption_prob": 0.05, "delay_mean": 2, "delay_std": 1},
    "Medium": {"disruption_prob": 0.15, "delay_mean": 5, "delay_std": 2},
    "High": {"disruption_prob": 0.30, "delay_mean": 10, "delay_std": 4}
}

params = risk_params[risk_level]

# Create tabs for different views
tab1, tab2, tab3 = st.tabs(["📊 Network Visualization", "📈 Risk Analysis", "📉 Simulation Results"])

# Define supply chain network structure
def create_supply_network():
    """Create a sample supply chain network"""
    G = nx.DiGraph()
    
    # Add nodes with attributes
    nodes = {
        "Supplier A": {"type": "supplier", "location": "Asia", "capacity": 1000},
        "Supplier B": {"type": "supplier", "location": "Europe", "capacity": 800},
        "Manufacturer 1": {"type": "manufacturer", "location": "North America", "capacity": 1500},
        "Manufacturer 2": {"type": "manufacturer", "location": "Asia", "capacity": 1200},
        "Distributor 1": {"type": "distributor", "location": "North America", "capacity": 2000},
        "Distributor 2": {"type": "distributor", "location": "Europe", "capacity": 1800},
        "Retailer A": {"type": "retailer", "location": "North America", "capacity": 500},
        "Retailer B": {"type": "retailer", "location": "Europe", "capacity": 600},
        "Retailer C": {"type": "retailer", "location": "Asia", "capacity": 400}
    }
    
    for node, attrs in nodes.items():
        G.add_node(node, **attrs)
    
    # Add edges (supply relationships)
    edges = [
        ("Supplier A", "Manufacturer 1", 500),
        ("Supplier A", "Manufacturer 2", 500),
        ("Supplier B", "Manufacturer 1", 400),
        ("Supplier B", "Manufacturer 2", 400),
        ("Manufacturer 1", "Distributor 1", 800),
        ("Manufacturer 1", "Distributor 2", 700),
        ("Manufacturer 2", "Distributor 1", 700),
        ("Manufacturer 2", "Distributor 2", 500),
        ("Distributor 1", "Retailer A", 500),
        ("Distributor 1", "Retailer C", 400),
        ("Distributor 2", "Retailer B", 600),
        ("Distributor 2", "Retailer C", 200)
    ]
    
    for source, target, flow in edges:
        G.add_edge(source, target, flow=flow)
    
    return G

# Monte Carlo simulation function
def run_monte_carlo_simulation(G, num_sims, disruption_prob, delay_mean, delay_std):
    """Run Monte Carlo simulations for supply chain disruptions"""
    results = []
    
    for sim in range(num_sims):
        total_delay = 0
        disrupted_nodes = []
        
        # Simulate disruptions at each node
        for node in G.nodes():
            if np.random.random() < disruption_prob:
                disrupted_nodes.append(node)
                # Sample delay from log-normal distribution
                delay = np.random.lognormal(mean=np.log(delay_mean), sigma=delay_std/delay_mean)
                total_delay += delay
        
        # Calculate impact metrics
        num_disrupted = len(disrupted_nodes)
        network_availability = 1 - (num_disrupted / len(G.nodes()))
        
        # Calculate flow disruption
        total_flow = sum(G[u][v]['flow'] for u, v in G.edges())
        disrupted_flow = 0
        for node in disrupted_nodes:
            # Sum outgoing flows from disrupted nodes
            disrupted_flow += sum(G[node][v]['flow'] for v in G.successors(node))
        
        flow_availability = 1 - (disrupted_flow / total_flow) if total_flow > 0 else 0
        
        results.append({
            'simulation': sim + 1,
            'total_delay': total_delay,
            'num_disrupted': num_disrupted,
            'network_availability': network_availability,
            'flow_availability': flow_availability,
            'disrupted_nodes': disrupted_nodes
        })
    
    return pd.DataFrame(results)

# Create network
G = create_supply_network()

# Tab 1: Network Visualization
with tab1:
    st.subheader("Supply Chain Network Structure")
    
    # Create network layout
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    
    # Prepare edge trace
    edge_x = []
    edge_y = []
    edge_text = []
    
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_text.append(f"Flow: {G[edge[0]][edge[1]]['flow']}")
    
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='#888'),
        hoverinfo='none',
        mode='lines')
    
    # Prepare node trace
    node_x = []
    node_y = []
    node_text = []
    node_color = []
    
    color_map = {
        "supplier": "#FF6B6B",
        "manufacturer": "#4ECDC4",
        "distributor": "#45B7D1",
        "retailer": "#96CEB4"
    }
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_info = G.nodes[node]
        node_text.append(f"{node}<br>Type: {node_info['type']}<br>Location: {node_info['location']}<br>Capacity: {node_info['capacity']}")
        node_color.append(color_map[node_info['type']])
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=[node for node in G.nodes()],
        textposition="top center",
        hovertext=node_text,
        marker=dict(
            color=node_color,
            size=30,
            line_width=2,
            line_color='white'))
    
    # Create figure
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=0),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        height=600
                    ))
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Legend
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown("🔴 **Suppliers**")
    col2.markdown("🔵 **Manufacturers**")
    col3.markdown("🟢 **Distributors**")
    col4.markdown("🟡 **Retailers**")

# Run simulation
with st.spinner("Running Monte Carlo simulations..."):
    simulation_results = run_monte_carlo_simulation(
        G, num_simulations, 
        params['disruption_prob'],
        params['delay_mean'],
        params['delay_std']
    )

# Tab 2: Risk Analysis
with tab2:
    st.subheader("Risk Metrics and Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Average Disrupted Nodes",
            f"{simulation_results['num_disrupted'].mean():.2f}",
            f"Max: {simulation_results['num_disrupted'].max()}"
        )
    
    with col2:
        st.metric(
            "Mean Network Availability",
            f"{simulation_results['network_availability'].mean():.1%}",
            f"Min: {simulation_results['network_availability'].min():.1%}"
        )
    
    with col3:
        st.metric(
            "Mean Flow Availability",
            f"{simulation_results['flow_availability'].mean():.1%}",
            f"Min: {simulation_results['flow_availability'].min():.1%}"
        )
    
    st.markdown("---")
    
    # Distribution plots
    col1, col2 = st.columns(2)
    
    with col1:
        # Total delay distribution
        fig_delay = go.Figure()
        fig_delay.add_trace(go.Histogram(
            x=simulation_results['total_delay'],
            nbinsx=50,
            name='Total Delay',
            marker_color='#FF6B6B'
        ))
        fig_delay.update_layout(
            title="Distribution of Total Delays",
            xaxis_title="Total Delay (days)",
            yaxis_title="Frequency",
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig_delay, use_container_width=True)
    
    with col2:
        # Network availability distribution
        fig_avail = go.Figure()
        fig_avail.add_trace(go.Histogram(
            x=simulation_results['network_availability'],
            nbinsx=50,
            name='Network Availability',
            marker_color='#4ECDC4'
        ))
        fig_avail.update_layout(
            title="Distribution of Network Availability",
            xaxis_title="Network Availability (%)",
            yaxis_title="Frequency",
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig_avail, use_container_width=True)
    
    # Risk metrics table
    st.subheader("Statistical Summary")
    
    stats_df = pd.DataFrame({
        'Metric': ['Total Delay (days)', 'Disrupted Nodes', 'Network Availability (%)', 'Flow Availability (%)'],
        'Mean': [
            simulation_results['total_delay'].mean(),
            simulation_results['num_disrupted'].mean(),
            simulation_results['network_availability'].mean() * 100,
            simulation_results['flow_availability'].mean() * 100
        ],
        'Std Dev': [
            simulation_results['total_delay'].std(),
            simulation_results['num_disrupted'].std(),
            simulation_results['network_availability'].std() * 100,
            simulation_results['flow_availability'].std() * 100
        ],
        '5th Percentile': [
            simulation_results['total_delay'].quantile(0.05),
            simulation_results['num_disrupted'].quantile(0.05),
            simulation_results['network_availability'].quantile(0.05) * 100,
            simulation_results['flow_availability'].quantile(0.05) * 100
        ],
        '95th Percentile': [
            simulation_results['total_delay'].quantile(0.95),
            simulation_results['num_disrupted'].quantile(0.95),
            simulation_results['network_availability'].quantile(0.95) * 100,
            simulation_results['flow_availability'].quantile(0.95) * 100
        ]
    })
    
    st.dataframe(stats_df.style.format({
        'Mean': '{:.2f}',
        'Std Dev': '{:.2f}',
        '5th Percentile': '{:.2f}',
        '95th Percentile': '{:.2f}'
    }), use_container_width=True)

# Tab 3: Simulation Results
with tab3:
    st.subheader("Detailed Simulation Results")
    
    # Show first 100 simulations
    st.dataframe(
        simulation_results[['simulation', 'total_delay', 'num_disrupted', 
                           'network_availability', 'flow_availability']].head(100),
        use_container_width=True
    )
    
    # Download button
    csv = simulation_results.to_csv(index=False)
    st.download_button(
        label="📥 Download Full Results (CSV)",
        data=csv,
        file_name=f"supply_chain_simulation_{num_simulations}_runs.csv",
        mime="text/csv"
    )
    
    st.markdown("---")
    st.info("💡 **Tip**: Use the sidebar to adjust simulation parameters and risk levels to see how they affect supply chain resilience.")
