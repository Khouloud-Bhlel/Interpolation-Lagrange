import numpy as np
from typing import List, Tuple

def format_decimal_to_2_places(num: float) -> float:
    """
    Format a decimal number to exactly 2 decimal places
    Returns a float rounded to 2 decimal places
    """
    return round(float(num), 2)

def format_coefficient_for_display(coeff: float) -> float:
    """
    Format coefficient values for display with 2 decimal places precision
    """
    # If it's very close to an integer, return the integer
    if abs(coeff - round(coeff)) < 1e-10:
        return float(round(coeff))
    # Otherwise, round to 2 decimal places
    return format_decimal_to_2_places(coeff)

class LagrangeInterpolator:
    """
    Lagrange Interpolation implementation with animation support
    """
    
    def __init__(self, points: List[Tuple[float, float]]):
        """
        Initialize with a list of (x, y) points
        """
        if len(points) < 2:
            raise ValueError("At least 2 points are required for interpolation")
        
        # Check for duplicate x-coordinates before sorting
        x_coords = [p[0] for p in points]
        if len(set(x_coords)) != len(x_coords):
            # Find the duplicates
            seen = set()
            duplicates = set()
            for x in x_coords:
                if x in seen:
                    duplicates.add(x)
                seen.add(x)
            raise ValueError(f"Duplicate x-coordinates found: {sorted(duplicates)}. Each x-coordinate must be unique for interpolation.")
        
        self.points = sorted(points, key=lambda p: p[0])  # Sort by x-coordinate
        self.x_values = [p[0] for p in self.points]
        self.y_values = [p[1] for p in self.points]
        self.n = len(self.points)
    
    def lagrange_basis(self, x: float, j: int) -> float:
        """
        Calculate the j-th Lagrange basis polynomial at point x
        """
        result = 1.0
        for i in range(self.n):
            if i != j:
                result *= (x - self.x_values[i]) / (self.x_values[j] - self.x_values[i])
        return result
    
    def interpolate(self, x: float) -> float:
        """
        Evaluate the Lagrange polynomial at point x
        """
        result = 0.0
        for j in range(self.n):
            result += self.y_values[j] * self.lagrange_basis(x, j)
        return result
    
    def interpolate_range(self, x_min: float = None, x_max: float = None, num_points: int = 100) -> Tuple[List[float], List[float]]:
        """
        Interpolate over a range of x values
        """
        if x_min is None:
            x_min = min(self.x_values) - 1
        if x_max is None:
            x_max = max(self.x_values) + 1
        
        x_range = np.linspace(x_min, x_max, num_points)
        y_range = [self.interpolate(x) for x in x_range]
        
        return x_range.tolist(), y_range
    
    def get_polynomial_coefficients(self) -> List[float]:
        """
        Get the coefficients of the interpolating polynomial
        Returns coefficients for polynomial a_n*x^n + a_(n-1)*x^(n-1) + ... + a_1*x + a_0
        """
        try:
            # Check for duplicate x-coordinates
            x_set = set(self.x_values)
            if len(x_set) != len(self.x_values):
                raise ValueError("Duplicate x-coordinates found. Each x-coordinate must be unique for interpolation.")
            
            # Create Vandermonde matrix
            V = np.vander(self.x_values, increasing=True)
            
            # Check if matrix is singular
            det = np.linalg.det(V)
            if abs(det) < 1e-12:
                raise ValueError("Singular matrix detected. The points may be too close together or collinear.")
            
            # Use least squares solver for better numerical stability
            coefficients, residuals, rank, s = np.linalg.lstsq(V, self.y_values, rcond=None)
            
            # Check if the solution is valid
            if rank < V.shape[1]:
                raise ValueError("The matrix is rank deficient. Cannot find unique polynomial coefficients.")
            
            return coefficients.tolist()
            
        except np.linalg.LinAlgError as e:
            raise ValueError(f"Linear algebra error during polynomial coefficient calculation: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error calculating polynomial coefficients: {str(e)}")
    
    def get_animation_data(self, num_steps: int = 50) -> List[dict]:
        """
        Generate data for animating the interpolation process
        """
        animation_steps = []
        x_min, x_max = min(self.x_values) - 1, max(self.x_values) + 1
        x_plot = np.linspace(x_min, x_max, 100)
        
        for step in range(1, min(num_steps, self.n) + 1):
            # Use only the first 'step' points
            partial_points = self.points[:step + 1]
            if len(partial_points) >= 2:
                partial_interpolator = LagrangeInterpolator(partial_points)
                x_range, y_range = partial_interpolator.interpolate_range(x_min, x_max, 100)
                
                animation_steps.append({
                    'step': step,
                    'points_used': partial_points,
                    'x_values': x_range,
                    'y_values': y_range,
                    'polynomial_degree': len(partial_points) - 1
                })
        
        return animation_steps
    
    def evaluate_at_points(self, x_values: List[float]) -> List[float]:
        """
        Evaluate the polynomial at specific x values
        """
        return [self.interpolate(x) for x in x_values]
    
    def get_lagrange_terms_details(self) -> dict:
        """
        Get detailed information about each Lagrange term including symbolic and numerical forms
        Returns a dictionary with evaluation_point, terms list, and polynomial_value
        """
        n = len(self.points)
        
        # Choose evaluation point - use midpoint or 0 if it's in range
        x_min, x_max = min(self.x_values), max(self.x_values)
        test_x = (x_min + x_max) / 2  # Midpoint for evaluation
        
        # Use x=0 if it's within a reasonable range
        if x_min <= 0 <= x_max:
            test_x = 0.0
        
        terms_details = []
        
        for j in range(n):
            # Get the point for this term
            x_j, y_j = self.points[j]
            
            # Build factors for symbolic representation
            factors = []
            denominator_calculation = []
            denominator_value = 1.0
            
            for i in range(n):
                if i != j:
                    x_i = self.x_values[i]
                    # Factor: (x - x_i)
                    factors.append(f"(x - {x_i})")
                    # Denominator calculation: (x_j - x_i)
                    denominator_calculation.append(f"({x_j} - {x_i})")
                    # Calculate denominator value
                    denominator_value *= (x_j - x_i)
            
            # Calculate numerator at evaluation point
            numerator_at_eval = 1.0
            for i in range(n):
                if i != j:
                    x_i = self.x_values[i]
                    numerator_at_eval *= (test_x - x_i)
            
            # Calculate the Lagrange basis function value at test_x
            lagrange_value = self.lagrange_basis(test_x, j)
            
            # Build symbolic representation
            symbolic = f"L_{j}(x) = " + " * ".join(factors) + f" / {denominator_value}"
            
            terms_details.append({
                'symbolic': symbolic,
                'factors': factors,
                'denominator_calculation': denominator_calculation,
                'denominator_value': denominator_value,
                'numerator_at_eval': numerator_at_eval,
                'final_value': lagrange_value
            })
        
        # Calculate polynomial value at evaluation point
        polynomial_value = self.interpolate(test_x)
        
        return {
            'evaluation_point': test_x,
            'terms': terms_details,
            'polynomial_value': polynomial_value
        }
