"""
Model Evaluation Module
Comprehensive evaluation metrics and reporting for ML models.
"""

import pandas as pd
import numpy as np
from sklearn.metrics import (
    confusion_matrix, classification_report, roc_curve, auc,
    precision_recall_curve, f1_score, accuracy_score
)
import matplotlib.pyplot as plt
import seaborn as sns


class ModelEvaluator:
    """Comprehensive model evaluation and reporting."""
    
    def __init__(self):
        """Initialize evaluator."""
        self.results = {}
        self.confusion_matrices = {}
        self.classification_reports = {}
    
    def evaluate_model(self, model, X_test, y_test, model_name):
        """
        Evaluate a single model.
        
        Parameters:
        -----------
        model : estimator
            Trained model
        X_test : array-like
            Test features
        y_test : array-like
            Test labels
        model_name : str
            Name of model
        
        Returns:
        --------
        dict
            Evaluation metrics
        """
        # Predictions
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)
        
        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        cf_matrix = confusion_matrix(y_test, y_pred)
        class_report = classification_report(y_test, y_pred, output_dict=True)
        
        results = {
            'Model': model_name,
            'Accuracy': accuracy,
            'Precision': class_report['weighted avg']['precision'],
            'Recall': class_report['weighted avg']['recall'],
            'F1-Score': class_report['weighted avg']['f1-score'],
            'Support': class_report['weighted avg']['support']
        }
        
        self.results[model_name] = results
        self.confusion_matrices[model_name] = cf_matrix
        self.classification_reports[model_name] = class_report
        
        return results
    
    def get_confusion_matrix(self, model_name):
        """
        Get confusion matrix for a model.
        
        Parameters:
        -----------
        model_name : str
            Name of model
        
        Returns:
        --------
        np.ndarray
            Confusion matrix
        """
        return self.confusion_matrices.get(model_name)
    
    def get_classification_report(self, model_name):
        """
        Get classification report for a model.
        
        Parameters:
        -----------
        model_name : str
            Name of model
        
        Returns:
        --------
        str
            Formatted classification report
        """
        report = self.classification_reports.get(model_name)
        if report:
            return classification_report(y_true=None, y_pred=None, output_dict=False)
        return None
    
    def get_results_dataframe(self):
        """
        Get all results as DataFrame.
        
        Returns:
        --------
        pd.DataFrame
            Results for all models
        """
        return pd.DataFrame(self.results).T
    
    def plot_confusion_matrices(self, figsize=(15, 10)):
        """
        Plot confusion matrices for all models.
        
        Parameters:
        -----------
        figsize : tuple
            Figure size
        """
        n_models = len(self.confusion_matrices)
        fig, axes = plt.subplots(2, 2, figsize=figsize)
        axes = axes.flatten()
        
        stress_levels = ['Low', 'Medium', 'High']
        
        for idx, (model_name, cf_matrix) in enumerate(self.confusion_matrices.items()):
            sns.heatmap(
                cf_matrix, annot=True, fmt='d', cmap='Blues',
                xticklabels=stress_levels,
                yticklabels=stress_levels,
                ax=axes[idx],
                cbar=False
            )
            axes[idx].set_title(f'{model_name}')
            axes[idx].set_ylabel('True Label')
            axes[idx].set_xlabel('Predicted Label')
        
        # Hide unused subplots
        for idx in range(n_models, 4):
            axes[idx].set_visible(False)
        
        plt.tight_layout()
        return fig
    
    def plot_accuracy_comparison(self):
        """
        Plot accuracy comparison for all models.
        
        Returns:
        --------
        matplotlib.figure.Figure
            Comparison plot
        """
        results_df = self.get_results_dataframe()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        colors = ['#10b981' if acc > 0.95 else '#f59e0b' if acc > 0.85 else '#ef4444'
                  for acc in results_df['Accuracy']]
        
        bars = ax.bar(results_df.index, results_df['Accuracy'], color=colors, edgecolor='black')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1%}', ha='center', va='bottom', fontweight='bold')
        
        ax.set_ylabel('Accuracy', fontsize=12)
        ax.set_title('Model Accuracy Comparison', fontsize=14, fontweight='bold')
        ax.set_ylim([0, 1])
        ax.axhline(y=0.95, color='g', linestyle='--', alpha=0.5, label='95% Target')
        ax.legend()
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        return fig
    
    def print_summary(self):
        """Print evaluation summary."""
        results_df = self.get_results_dataframe()
        
        print("\n" + "="*80)
        print("MODEL EVALUATION SUMMARY")
        print("="*80)
        print(results_df.to_string())
        print("="*80)
        
        best_model = results_df['Accuracy'].idxmax()
        print(f"\n✓ Best Model: {best_model} ({results_df.loc[best_model, 'Accuracy']:.1%})")
    
    def save_report(self, filepath='model_evaluation_report.txt'):
        """
        Save detailed evaluation report to file.
        
        Parameters:
        -----------
        filepath : str
            Output file path
        """
        results_df = self.get_results_dataframe()
        
        with open(filepath, 'w') as f:
            f.write("="*80 + "\n")
            f.write("MODEL EVALUATION REPORT\n")
            f.write("="*80 + "\n\n")
            
            f.write("PERFORMANCE SUMMARY\n")
            f.write("-"*80 + "\n")
            f.write(results_df.to_string())
            f.write("\n\n")
            
            f.write("DETAILED METRICS\n")
            f.write("-"*80 + "\n")
            
            for model_name in self.classification_reports.keys():
                f.write(f"\n{model_name}:\n")
                f.write("-"*80 + "\n")
                
                report = self.classification_reports[model_name]
                f.write("Precision: {:.4f}\n".format(report['weighted avg']['precision']))
                f.write("Recall:    {:.4f}\n".format(report['weighted avg']['recall']))
                f.write("F1-Score:  {:.4f}\n".format(report['weighted avg']['f1-score']))
                
                cf = self.confusion_matrices[model_name]
                f.write("\nConfusion Matrix:\n")
                f.write(f"  True Negatives:  {cf[0,0]}\n")
                f.write(f"  False Positives: {cf[0,1]}\n")
                f.write(f"  False Negatives: {cf[1,0]}\n")
                f.write(f"  True Positives:  {cf[1,1]}\n")
        
        print(f"✓ Report saved to {filepath}")


class CrossValidationEvaluator:
    """Cross-validation evaluation."""
    
    def __init__(self):
        """Initialize CV evaluator."""
        self.cv_results = {}
    
    def evaluate_cv(self, model, X, y, cv=5, model_name='Model'):
        """
        Perform cross-validation evaluation.
        
        Parameters:
        -----------
        model : estimator
            Model to evaluate
        X : array-like
            Features
        y : array-like
            Labels
        cv : int
            Number of folds
        model_name : str
            Name of model
        
        Returns:
        --------
        dict
            CV results
        """
        from sklearn.model_selection import cross_validate
        
        scoring = ['accuracy', 'precision_weighted', 'recall_weighted', 'f1_weighted']
        cv_results = cross_validate(model, X, y, cv=cv, scoring=scoring)
        
        results = {
            'Model': model_name,
            'Accuracy': f"{cv_results['test_accuracy'].mean():.4f} (+/- {cv_results['test_accuracy'].std():.4f})",
            'Precision': f"{cv_results['test_precision_weighted'].mean():.4f} (+/- {cv_results['test_precision_weighted'].std():.4f})",
            'Recall': f"{cv_results['test_recall_weighted'].mean():.4f} (+/- {cv_results['test_recall_weighted'].std():.4f})",
            'F1-Score': f"{cv_results['test_f1_weighted'].mean():.4f} (+/- {cv_results['test_f1_weighted'].std():.4f})"
        }
        
        self.cv_results[model_name] = results
        
        return results
    
    def print_cv_results(self):
        """Print cross-validation results."""
        print("\n" + "="*80)
        print("5-FOLD CROSS-VALIDATION RESULTS")
        print("="*80)
        
        for model_name, results in self.cv_results.items():
            print(f"\n{model_name}:")
            for metric, value in results.items():
                if metric != 'Model':
                    print(f"  {metric:12}: {value}")
        
        print("="*80)
