from odoo import models, fields, api
import json


class InterpolationPoint(models.Model):
    _name = 'lagrange.interpolation.point'
    _description = 'Interpolation Point'
    _order = 'x_coordinate'

    name = fields.Char(string='Name', compute='_compute_name', store=True)
    x_coordinate = fields.Float(string='X Coordinate', required=True)
    y_coordinate = fields.Float(string='Y Coordinate', required=True)
    interpolation_set_id = fields.Many2one('lagrange.interpolation.set', string='Interpolation Set')

    @api.depends('x_coordinate', 'y_coordinate')
    def _compute_name(self):
        for record in self:
            record.name = f"Point ({record.x_coordinate}, {record.y_coordinate})"


class InterpolationSet(models.Model):
    _name = 'lagrange.interpolation.set'
    _description = 'Interpolation Set'
    _order = 'create_date desc'

    name = fields.Char(string='Name', required=True, default='New Interpolation Set')
    description = fields.Text(string='Description')
    point_ids = fields.One2many('lagrange.interpolation.point', 'interpolation_set_id', string='Points')
    points_count = fields.Integer(string='Points Count', compute='_compute_points_count')
    polynomial_degree = fields.Integer(string='Polynomial Degree', compute='_compute_polynomial_degree')
    result_ids = fields.One2many('lagrange.interpolation.result', 'interpolation_set_id', string='Results')
    results_count = fields.Integer(string='Results Count', compute='_compute_results_count')
    
    @api.depends('point_ids')
    def _compute_points_count(self):
        for record in self:
            record.points_count = len(record.point_ids)
    
    @api.depends('point_ids')
    def _compute_polynomial_degree(self):
        for record in self:
            record.polynomial_degree = max(0, len(record.point_ids) - 1)
    
    @api.depends('result_ids')
    def _compute_results_count(self):
        for record in self:
            record.results_count = len(record.result_ids)


class InterpolationResult(models.Model):
    _name = 'lagrange.interpolation.result'
    _description = 'Interpolation Result'
    _order = 'create_date desc'

    name = fields.Char(string='Name', compute='_compute_name', store=True)
    interpolation_set_id = fields.Many2one('lagrange.interpolation.set', string='Interpolation Set', required=True)
    polynomial_coefficients = fields.Text(string='Polynomial Coefficients (JSON)')
    evaluation_points = fields.Text(string='Evaluation Points (JSON)')
    evaluation_results = fields.Text(string='Evaluation Results (JSON)')
    polynomial_formula = fields.Text(string='Polynomial Formula', compute='_compute_polynomial_formula')
    
    @api.depends('interpolation_set_id', 'create_date')
    def _compute_name(self):
        for record in self:
            set_name = record.interpolation_set_id.name if record.interpolation_set_id else 'Unknown'
            record.name = f"Result for {set_name} - {record.create_date.strftime('%Y-%m-%d %H:%M')}"
    
    @api.depends('polynomial_coefficients')
    def _compute_polynomial_formula(self):
        for record in self:
            if record.polynomial_coefficients:
                try:
                    coefficients = json.loads(record.polynomial_coefficients)
                    formula = self._build_polynomial_formula(coefficients)
                    record.polynomial_formula = formula
                except:
                    record.polynomial_formula = "Invalid coefficients format"
            else:
                record.polynomial_formula = ""
    
    def _build_polynomial_formula(self, coefficients):
        """Build human-readable polynomial formula from coefficients"""
        if not coefficients:
            return "No coefficients"
        
        terms = []
        degree = len(coefficients) - 1
        
        for i, coeff in enumerate(coefficients):
            if abs(coeff) < 1e-10:  # Skip very small coefficients
                continue
                
            power = degree - i
            term = ""
            
            # Handle coefficient sign and value
            if len(terms) == 0:  # First term
                if coeff < 0:
                    term = "-"
            else:  # Subsequent terms
                if coeff < 0:
                    term = " - "
                else:
                    term = " + "
            
            # Handle coefficient value
            abs_coeff = abs(coeff)
            if power == 0:
                # Constant term - always show the coefficient
                if self._is_simple_fraction(abs_coeff):
                    term += self._format_as_fraction(abs_coeff)
                else:
                    term += self._format_decimal(abs_coeff)
            elif abs_coeff == 1:
                # Coefficient is 1, don't show it explicitly
                # term already has the sign
                pass
            else:
                # Show the coefficient
                if self._is_simple_fraction(abs_coeff):
                    term += self._format_as_fraction(abs_coeff)
                else:
                    term += self._format_decimal(abs_coeff)
            
            # Handle variable and power
            if power > 1:
                term += f"x²" if power == 2 else f"x^{power}"
            elif power == 1:
                term += "x"
            # For power 0, no x term needed (already handled above)
            
            terms.append(term)
        
        return "P(x) = " + "".join(terms) if terms else "P(x) = 0"
    
    def _is_simple_fraction(self, num):
        """Check if a number can be represented as a simple fraction"""
        tolerance = 1e-10
        
        # Check for exact common fractions first
        common_fractions = {
            0.5: (1, 2), 0.25: (1, 4), 0.75: (3, 4), 0.125: (1, 8), 0.875: (7, 8),
            0.333333: (1, 3), 0.666667: (2, 3), 0.2: (1, 5), 0.4: (2, 5), 0.6: (3, 5), 0.8: (4, 5),
            0.166667: (1, 6), 0.833333: (5, 6)
        }
        
        for decimal, _ in common_fractions.items():
            if abs(num - decimal) < tolerance:
                return True
        
        # Check for general fractions with small denominators
        for denom in range(2, 9):  # Reduced range for cleaner fractions
            for numer in range(1, denom):
                if abs(num - numer / denom) < tolerance:
                    return True
        return False
    
    def _format_as_fraction(self, num):
        """Format number as fraction"""
        tolerance = 1e-10
        
        # Check for exact common fractions first
        common_fractions = {
            0.5: (1, 2), 0.25: (1, 4), 0.75: (3, 4), 0.125: (1, 8), 0.875: (7, 8),
            0.333333: (1, 3), 0.666667: (2, 3), 0.2: (1, 5), 0.4: (2, 5), 0.6: (3, 5), 0.8: (4, 5),
            0.166667: (1, 6), 0.833333: (5, 6)
        }
        
        for decimal, (numer, denom) in common_fractions.items():
            if abs(num - decimal) < tolerance:
                return f"({numer}/{denom})"
        
        # Check for general fractions with small denominators
        for denom in range(2, 9):
            for numer in range(1, denom):
                if abs(num - numer / denom) < tolerance:
                    return f"({numer}/{denom})"
        
        return self._format_decimal(num)
    
    def _format_decimal(self, num):
        """Format decimal with reasonable precision"""
        if abs(num - round(num)) < 1e-10:
            return str(int(round(num)))
        # Format to 2 decimal places and remove trailing zeros
        formatted = f"{num:.2f}".rstrip('0').rstrip('.')
        return formatted
    
    def get_coefficients(self):
        """Get coefficients as Python list"""
        if self.polynomial_coefficients:
            try:
                return json.loads(self.polynomial_coefficients)
            except:
                return []
        return []
    
    def get_evaluation_data(self):
        """Get evaluation data as Python lists"""
        try:
            points = json.loads(self.evaluation_points) if self.evaluation_points else []
            results = json.loads(self.evaluation_results) if self.evaluation_results else []
            return points, results
        except:
            return [], []
