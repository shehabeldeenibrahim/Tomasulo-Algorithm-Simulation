# Tomasulo-Algorithm-Simulation
Architectural simulator capable of assessing the performance of a simplified superscalar out-of-order 16-bit RISC processor that uses Tomasulo’s algorithm with speculation with web-base support (Python-Flask).

Instruction set architecture (ISA): The simulator assumes a simplified RISC ISA inspired by the ISA of the
Ridiculously Simple Computer (RiSC-16) proposed by Bruce Jacob. As implied by its name, the word size of this
computer is 16-bit. The processor has 8 general-purpose registers R0 to R7 (16-bit each). The register R0 always
contains the value 0 and cannot be changed. Memory is word addressable and uses a 16-bit address (as such the
memory capacity is 128 KB). The instruction format itself is not very important to the simulation and therefore is
not described here. However, the simulator should support the following set of instructions (16-bit each):


1. Load/store
o Load word: Loads value from memory into regA. Memory address is formed by adding imm
with contents of regB, where imm is a 7-bit signed immediate value (ranging from -64 to 63).
§ LW regA, regB, imm
o Store word: Stores value from regA into memory. Memory address is computed as in the case
of the load word instruction
§ SW regA, regB, imm
2. Unconditional branch
o Jump: branches to the address PC+1+imm
§ JMP imm
3. Conditional branch
o Branch if equal: branches to the address PC+1+imm if regA=regB
§ BEQ regA, regB, imm
4. Call/Return
o Jump and link register: Stores the value of PC+1 in regA and branches (unconditionally) to the
address in regB.
§ JALR regA, regB
o Return: branches (unconditionally) to the address stored in regA
§ RET regA
5. Arithmetic
o Add: Adds the value of regB and regC storing the result in regA
§ ADD regA, regB, regC
o Subtract: Subtracts the value of regC from regB storing the result in regA
§ SUB regA, regB, regC
o Add immediate: Adds the value of regB to imm storing the result in regA
§ ADDI regA, regB, imm
o Nand: Performans a bitwise NAND operation between the values of regB and regC storing the
result in regA
§ NAND regA, regB, regC
o Multiply: Multiplies the value of regB and regC storing the result in regA
§ MUL regA, regB, regC
