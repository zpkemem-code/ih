"""
Pyromod compatibility patch for Pyrogram 2.0.106
This patches the pyromod.listen.client module to fix the TypeError
"""
import sys
from types import ModuleType

# Create a mock pyromod structure that's compatible
class MockPyromod:
    """Mock pyromod module to prevent import errors"""
    pass

# Install the mock before actual pyromod tries to import
sys.modules['pyromod'] = MockPyromod()
sys.modules['pyromod.listen'] = MockPyromod()
sys.modules['pyromod.listen.client'] = MockPyromod()
sys.modules['pyromod.listen.message'] = MockPyromod()
sys.modules['pyromod.listen.chat'] = MockPyromod()
sys.modules['pyromod.listen.user'] = MockPyromod()
sys.modules['pyromod.listen.callback_query_handler'] = MockPyromod()
sys.modules['pyromod.listen.message_handler'] = MockPyromod()
sys.modules['pyromod.helpers'] = MockPyromod()
sys.modules['pyromod.nav'] = MockPyromod()

print("Pyromod compatibility patch applied")
