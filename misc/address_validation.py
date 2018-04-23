"""
This file compiles the "validation code" used in `conftest.py`
for validating signatures.

Note: requirements.txt does not currently specify for serpent
to be installed. You can install it with:

$ pip install git+https://github.com/ethereum/serpent.git
"""
import serpent
from ethereum import utils


"""
Build a pure version of the validation code.
"""
def compile_pure(address):
    validation_code = '''
~calldatacopy(0, 0, 128)
~call(3000, 1, 0, 0, 128, 0, 32)
return(~mload(0) == {})
    '''.format(utils.checksum_encode(address))
    return serpent.compile(validation_code)


"""
Build an impure version of the validation code, which uses sstore.
This is useful for testing that impure validation
contracts will be rejected.
"""
def compile_impure_sstore(address):
    validation_code = '''
~calldatacopy(0, 0, 128)
~call(3000, 1, 0, 0, 128, 0, 32)
~sstore(1, 1)
return(~mload(0) == {})
    '''.format(utils.checksum_encode(address))
    return serpent.compile(validation_code)


"""
Build an impure version of the validation code, which uses sload.
This is useful for testing that impure validation
contracts will be rejected.
"""
def compile_impure_sload(address):
    validation_code = '''
~sload(0)
~calldatacopy(0, 0, 128)
~call(3000, 1, 0, 0, 128, 0, 32)
return(~mload(0) == {})
    '''.format(utils.checksum_encode(address))
    return serpent.compile(validation_code)


addr = utils.privtoaddr(1337)
pure = compile_pure(addr).replace(addr, b'<<ADDRESS>>')
impure_sstore = compile_impure_sstore(addr).replace(addr, b'<<ADDRESS>>')
impure_sload = compile_impure_sload(addr).replace(addr, b'<<ADDRESS>>')

print("-" * 10)
print("Pure:")
print("-" * 10)
print(pure)
print("-" * 10)
print("Impure (sstore):")
print("-" * 10)
print(impure_sstore)
print("-" * 10)
print("Impure (sload):")
print("-" * 10)
print(impure_sload)
print("-" * 10)
