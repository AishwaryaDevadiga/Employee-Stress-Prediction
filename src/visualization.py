"""
Visualization Module
Creates plots for analysis and model evaluation.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import os


# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


def plot_accuracy_comparison(accuracies, output_path='outputs/plots'):
    """
    Create a bar chart comparing model accuracies.
    
    Parameters:
    -----------
    accuracies : dict
        Dictionary with model names and their accuracies
    output_path : str
        Path to save the plot
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    
    models = list(accuracies.keys())
    scores = list(accuracies.values())
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(models, scores, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
    
    # Add value labels on top of bars
    for bar, score in zip(bars, scores):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{score:.4f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.xlabel('Model', fontsize=12, fontweight='bold')
    plt.ylabel('Accuracy', fontsize=12, fontweight='bold')
    plt.title('Model Accuracy Comparison', fontsize=14, fontweight='bold')
    plt.ylim([0, 1])
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    filepath = os.path.join(output_path, 'accuracy_comparison.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"✓ Accuracy comparison plot saved to {filepath}")
    plt.close()


def plot_confusion_matrices(results, output_path='outputs/plots'):
    """
    Create confusion matrices for all models.
    
    Parameters:
    -----------
    results : dict
        Results dictionary with model data
    output_path : str
        Path to save the plots
    """
    os.makedirs(output_path, exist_ok=True)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    axes = axes.ravel()
    
    for idx, (model_name, data) in enumerate(results.items()):
        cm = data['confusion_matrix']
        
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   ax=axes[idx], cbar=True, annot_kws={'size': 12})
        axes[idx].set_title(f'{model_name}\nConfusion Matrix', 
                          fontsize=12, fontweight='bold')
        axes[idx].set_xlabel('Predicted', fontsize=10)
        axes[idx].set_ylabel('Actual', fontsize=10)
    
    plt.tight_layout()
    filepath = os.path.join(output_path, 'confusion_matrices.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"✓ Confusion matrices plot saved to {filepath}")
    plt.close()


def plot_feature_importance(feature_importance_df, output_path='outputs/plots', 
                           top_n=15):
    """
    Create a bar chart of feature importance.
    
    Parameters:
    -----------
    feature_importance_df : pd.DataFrame
        DataFrame with 'Feature' and 'Importance' columns
    output_path : str
        Path to save the plot
    top_n : int
        Number of top features to display
    """
    os.makedirs(output_path, exist_ok=True)
    
    top_features = feature_importance_df.head(top_n)
    
    plt.figure(figsize=(12, 8))
    bars = plt.barh(range(len(top_features)), top_features['Importance'].values, 
                    color='#2ca02c')
    
    # Add value labels
    for idx, (bar, value) in enumerate(zip(bars, top_features['Importance'].values)):
        plt.text(value, bar.get_y() + bar.get_height()/2, 
                f'{value:.4f}', ha='left', va='center', fontsize=9)
    
    plt.yticks(range(len(top_features)), top_features['Feature'].values)
    plt.xlabel('Importance', fontsize=12, fontweight='bold')
    plt.title(f'Top {top_n} Feature Importance (Random Forest)', 
             fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    filepath = os.path.join(output_path, 'feature_importance.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"✓ Feature importance plot saved to {filepath}")
    plt.close()


def plot_stress_distribution(df, output_path='outputs/plots', 
                             score_column='Stress_Score',
                             level_column='Stress_Level'):
    """
    Create visualizations of stress score and level distributions.
    
    Parameters:
    -----------
    df : pd.DataFrame
        The dataset with stress features
    output_path : str
        Path to save the plots
    score_column : str
        Name of the stress score column
    level_column : str
        Name of the stress level column
    """
    os.makedirs(output_path, exist_ok=True)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Stress Score Distribution
    axes[0].hist(df[score_column], bins=30, color='#1f77b4', edgecolor='black', alpha=0.7)
    axes[0].set_xlabel(score_column, fontsize=11, fontweight='bold')
    axes[0].set_ylabel('Frequency', fontsize=11, fontweight='bold')
    axes[0].set_title(f'{score_column} Distribution', fontsize=12, fontweight='bold')
    axes[0].grid(axis='y', alpha=0.3)
    
    # Stress Level Distribution
    stress_level_counts = df[level_column].value_counts().sort_index()
    level_names = ['Low', 'Medium', 'High']
    colors = ['#2ca02c', '#ff7f0e', '#d62728']
    
    bars = axes[1].bar([level_names[i] for i in stress_level_counts.index], 
                       stress_level_counts.values, color=colors, edgecolor='black', alpha=0.7)
    
    # Add count labels
    for bar in bars:
        height = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    axes[1].set_xlabel('Stress Level', fontsize=11, fontweight='bold')
    axes[1].set_ylabel('Count', fontsize=11, fontweight='bold')
    axes[1].set_title('Stress Level Distribution', fontsize=12, fontweight='bold')
    axes[1].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    filepath = os.path.join(output_path, 'stress_distribution.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"✓ Stress distribution plot saved to {filepath}")
    plt.close()


def save_classification_reports(results, output_path='outputs/results'):
    """
    Save classification reports as text files.
    
    Parameters:
    -----------
    results : dict
        Results dictionary with model data
    output_path : str
        Path to save the reports
    """
    os.makedirs(output_path, exist_ok=True)
    
    for model_name, data in results.items():
        filepath = os.path.join(output_path, f'{model_name}_classification_report.txt')
        with open(filepath, 'w') as f:
            f.write(f"Classification Report for {model_name}\n")
            f.write("=" * 70 + "\n\n")
            f.write(data['classification_report'])
        
        print(f"✓ Classification report for {model_name} saved to {filepath}")
