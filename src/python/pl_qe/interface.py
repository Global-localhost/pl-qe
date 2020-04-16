from zquantum.core.interfaces.backend import QuantumSimulator


class PennyLaneDefaultQubit(QuantumSimulator):
    def __init__(self, n_samples=None, nthreads=1):
        self.nthreads = nthreads
        self.n_samples = n_samples

    def run_circuit_and_measure(self, circuit, **kwargs):
        wavefunction = self.get_wavefunction(circuit)
        return sample_from_wavefunction(wavefunction, self.n_samples)

    def get_expectation_values(self, circuit, qubit_operator, **kwargs):
        return self.get_exact_expectation_values(circuit, qubit_operator, **kwargs)

    def get_exact_expectation_values(self, circuit, qubit_operator, **kwargs):
        save_circuit(circuit, './temp_qhipster_circuit.json')
        if(isinstance(qubit_operator, SymbolicOperator)):
            save_symbolic_operator(qubit_operator, './temp_qhipster_operator.json')
        else:
            raise Exception("Unsupported type: "+type(qubit_operator) + "QHipster works only with openfermion.SymbolicOperator")


        # Parse JSON files for qhipster usage
        subprocess.call(['/app/json_parser/json_to_qasm.o', './temp_qhipster_circuit.json'])
        subprocess.call(['/app/json_parser/qubitop_to_paulistrings.o',
                         './temp_qhipster_operator.json'])
        # Run simulation
        subprocess.call(['/app/zapata/zapata_interpreter_no_mpi_get_exp_vals.out',
                         './temp_qhipster_circuit.txt', str(self.nthreads), './temp_qhipster_operator.txt',
                         './expectation_values.json'])
        return load_expectation_values('./expectation_values.json')

    def get_wavefunction(self, circuit):
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
