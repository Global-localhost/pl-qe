import pennylane as qml

from zquantum.core.interfaces.backend import QuantumSimulator
from zquantum.core.measurement import load_wavefunction, ExpectationValues, sample_from_wavefunction
from .utils import save_symbolic_operator
from openfermion.ops import SymbolicOperator



class PennyLaneDevice(QuantumSimulator):
    def __init__(self, n_samples=None, device="default.qubit"):
        self.n_samples = n_samples
        self.device = device

    def run_circuit_and_measure(self, circuit, **kwargs):
        """
        Method for executing the circuit and measuring the outcome.
        Args:
            circuit (core.circuit.Circuit): quantum circuit to be executed.
        """
        wavefunction = self.get_wavefunction(circuit)
        return sample_from_wavefunction(wavefunction, self.n_samples)

    def get_expectation_values(self, circuit, qubit_operator, **kwargs):
        """
        Executes the circuit and calculates the expectation values for given operator.

        Args:
            circuit (core.circuit.Circuit): quantum circuit to be executed.
            qubit_operator(openfermion): Operator for which we calculate the expectation value.

        Returns:
            ExpectationValues: object representing expectation values for given operator.
        """
        return self.get_exact_expectation_values(circuit, qubit_operator, **kwargs)

    def get_exact_expectation_values(self, circuit, qubit_operator, **kwargs):
        """
        Calculates the expectation values for given operator, based on the exact quantum state produced by circuit.

        Args:
            circuit (core.circuit.Circuit): quantum circuit to be executed.
            qubit_operator (openfermion): Operator for which we calculate the expectation value.

        Returns:
            ExpectationValues: object representing expectation values for given operator.
        """
        # convert the OpenFermion operator to PennyLane observables
        coeffs, obs = qml.qchem.convert_hamiltonian(qubit_operator).terms
        num_qubits = len(circuit.get_qubits())
        dev = qml.device(self.device, wires=num_qubits)

        ansatz = qml.from_qiskit(circuit.to_qiskit())
        qnodes = qml.map(obs, ansatz, dev, measure="expval")
        exp_val = qml.dot(qnodes, coeffs)
        return ExpectationValues(values=exp_val)

    def get_wavefunction(self, circuit):
        """
        Returns a wavefunction representing quantum state produced by a circuit

        Args:
            circuit (core.circuit.Circuit): quantum circuit to be executed.

        Returns:
            pyquil.Wafefunction: wavefunction object.

        """
        # First, save the circuit object to file in JSON format
        save_circuit(circuit, './temp_qhipster_circuit.json')


        # Parse JSON files for qhipster usage
        subprocess.call(['/app/json_parser/json_to_qasm.o', './temp_qhipster_circuit.json'])
        # Run simulation
        subprocess.call(['/app/zapata/zapata_interpreter_no_mpi_get_wf.out',
                         './temp_qhipster_circuit.txt', str(self.nthreads), './temp_qhipster_wavefunction.json'])

        wavefunction = load_wavefunction('./temp_qhipster_wavefunction.json')
        os.remove('./temp_qhipster_circuit.json')
        os.remove('./temp_qhipster_wavefunction.json')
        return wavefunction
