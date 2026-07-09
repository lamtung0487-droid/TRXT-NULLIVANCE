"""
L2.5b Topological Vortex Detector
=================================
Detects vortices using winding number calculation on 2x2 plaquettes.
Robust against amplitude fluctuations.
"""

import numpy as np

def wrap_phase(delta):
    """Wrap phase difference to (-pi, pi]."""
    return (delta + np.pi) % (2 * np.pi) - np.pi

def detect_vortices(theta):
    """
    Detect vortices in a 2D phase field using winding number.
    
    Args:
        theta (np.ndarray): 2D array of phase values (radians).
        
    Returns:
        dict: {
            'coords_plus': list of (x, y) tuples for +1 vortices,
            'coords_minus': list of (x, y) tuples for -1 vortices,
            'charge_map': 2D array with +1, -1, 0 at vortex locations
        }
    """
    ny, nx = theta.shape
    charge_map = np.zeros((ny, nx), dtype=int)
    coords_plus = []
    coords_minus = []
    
    # Vectorized calculation on plaquettes
    # Points: 0=(i,j), 1=(i+1,j), 2=(i+1,j+1), 3=(i,j+1)
    # Loop direction: 0->1->2->3->0 (CCW)
    
    # We can use roll to get neighbors efficiently
    t00 = theta
    t10 = np.roll(theta, -1, axis=1) # (i+1, j)
    t11 = np.roll(np.roll(theta, -1, axis=1), -1, axis=0) # (i+1, j+1)
    t01 = np.roll(theta, -1, axis=0) # (i, j+1) # Wait, roll axis 0 is y? usually y is axis 0.
    
    # Let's verify indexing: theta[y, x]
    # roll(-1, axis=1) shifts left, so element at [y, x] becomes [y, x+1] value. Correct.
    # roll(-1, axis=0) shifts up, so element at [y, x] becomes [y+1, x] value. Correct.
    
    # Edges:
    # 1: (x,y) -> (x+1,y)  : t10 - t00
    # 2: (x+1,y) -> (x+1,y+1) : t11 - t10
    # 3: (x+1,y+1) -> (x,y+1) : t01 - t11
    # 4: (x,y+1) -> (x,y) : t00 - t01
    
    d1 = wrap_phase(t10 - t00)
    d2 = wrap_phase(t11 - t10)
    d3 = wrap_phase(t01 - t11)
    d4 = wrap_phase(t00 - t01)
    
    winding_sum = d1 + d2 + d3 + d4
    winding_number = winding_sum / (2 * np.pi)
    
    # Classification
    # Vortex (+1): winding ~ +1
    # Anti-vortex (-1): winding ~ -1
    
    # We assign the charge to the top-left corner (pixel i,j) of the plaquette
    # Or center? Let's stick to pixel coordinates for simplicity.
    # Note: periodic boundary conditions are handled by np.roll wrapping,
    # but the physical edge winding might be weird at the boundary if phase jumps.
    # However, for a torus topology, this is correct.
    
    # Thresholds
    is_plus = (winding_number > 0.5) & (winding_number < 1.5)
    is_minus = (winding_number > -1.5) & (winding_number < -0.5)
    
    # Extract coordinates
    y_plus, x_plus = np.where(is_plus)
    y_minus, x_minus = np.where(is_minus)
    
    for y, x in zip(y_plus, x_plus):
        # Filter boundary effects if mostly interested in bulk?
        # On torus, valid everywhere.
        charge_map[y, x] = 1
        coords_plus.append((x, y)) # Return (x, y) tuple
        
    for y, x in zip(y_minus, x_minus):
        charge_map[y, x] = -1
        coords_minus.append((x, y))
        
    return {
        'coords_plus': coords_plus,
        'coords_minus': coords_minus,
        'charge_map': charge_map
    }
