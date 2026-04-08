
---

### 2. `nexah/urf_axial_space/__init__.py`

```python
"""
URF Axial Space – Public API

Provides 3D coordinate mapping for Matroschka structures,
Spiral Coupling and Switch Layer dynamics.
"""

from .urf_axial_space_kernel import URFAxialSpaceKernel

__all__ = ["URFAxialSpaceKernel"]

# Simple high-level access
__version__ = "0.1"
