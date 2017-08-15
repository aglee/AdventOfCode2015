import java.io.*;
import java.util.*;
import java.security.*;

// 2017-08-15-Tue: Was going over this stuff and discovered my Swift code wasn't working -- it got in an infinite loop somewhere.  Rewrote the solution in Java; this works.

class Input {
	static List<String> readLinesFromPath(String inputFilePath) throws IOException {
		BufferedReader reader = new BufferedReader(new FileReader(inputFilePath));
		String line = null;
		List<String> allLines = new ArrayList<String>();
		try {
			while((line = reader.readLine()) != null) {
				allLines.add(line);
			}
		} finally {
			reader.close();
		}
		return allLines;
	}

	static List<String> readLinesFromFile(String inputFileName) throws IOException {
		File inputFile = new File(System.getProperty("user.dir"), inputFileName);
		return readLinesFromPath(inputFile.toString());
	}
}

abstract class Source {
	Integer signal = null;

	abstract Integer calculateSignal();

	abstract boolean allInputsHaveSignal();

	final void updateSignal() {
		if (signal == null && allInputsHaveSignal()) {
			signal = calculateSignal();
		}
	}
}

class Constant extends Source {
	boolean allInputsHaveSignal() { return true; }
	Integer calculateSignal() { return signal; }
	
	Constant(int value) { this.signal = value; }
}

abstract class Gate extends Source {
	Source input1;
	Source input2;
	boolean allInputsHaveSignal() { return input1.signal != null && input2.signal != null; }
}

class AndGate extends Gate {
	Integer calculateSignal() { return input1.signal & input2.signal; }
}

class OrGate extends Gate {
	Integer calculateSignal() { return input1.signal | input2.signal; }
}

class LShiftGate extends Gate {
	Integer calculateSignal() { return input1.signal << input2.signal; }
}

class RShiftGate extends Gate {
	Integer calculateSignal() { return input1.signal >> input2.signal; }
}

class NotGate extends Gate {
	boolean allInputsHaveSignal() { return input1.signal != null; }
	Integer calculateSignal() { return input1.signal ^ 0xFFFF; }
}

class Wire extends Source {
	String name;
	Source input;
	boolean allInputsHaveSignal() { return input.signal != null; }
	Integer calculateSignal() { return input.signal; }
}

class Machine {
	private Map<String, Wire> wires = new HashMap<String, Wire>();
	private List<Gate> allGates = new ArrayList<Gate>();
	
	Machine(String inputFileName) throws IOException {
		List<String> lines = Input.readLinesFromFile(inputFileName);
		for (String line : lines) {
			parseInputLine(line);
		}
	}
	
	void propagateSignals() {
		while (true) {
			int wiresRemaining = propagateWireSignals();
			int gatesRemaining = propagateGateSignals();
			if (wiresRemaining == 0 && gatesRemaining == 0) {
				break;
			}
		}
	}
	
	private int propagateWireSignals() {
		int numberUnset = 0;
		for (String wireName : wires.keySet()) {
			wires.get(wireName).updateSignal();
			if (wires.get(wireName).signal == null) {
				numberUnset++;
			}
		}
		return numberUnset;
	}
	
	private int propagateGateSignals() {
		int numberUnset = 0;
		for (Gate gate : allGates) {
			gate.updateSignal();
			if (gate.signal == null) {
				numberUnset++;
			}
		}
		return numberUnset;
	}
	
	private void parseInputLine(String line) {
		String sides[] = line.split(" -> ");
		String leftParts[] = sides[0].split(" ");
		Source leftSource = null;
		Wire w = wireWithName(sides[1]);
		
		if (leftParts.length == 1) {
			leftSource = sourceFromString(leftParts[0]);
		} else if (leftParts.length == 2) {
			Gate gate = new NotGate();
			gate.input1 = sourceFromString(leftParts[1]);
			leftSource = gate;
		} else if (leftParts.length == 3) {
			String op = leftParts[1];
			Gate gate = null;
			if (op.equals("AND")) { gate = new AndGate(); }
			else if (op.equals("OR")) { gate = new OrGate(); }
			else if (op.equals("LSHIFT")) { gate = new LShiftGate(); }
			else if (op.equals("RSHIFT")) { gate = new RShiftGate(); }
			
			gate.input1 = sourceFromString(leftParts[0]);
			gate.input2 = sourceFromString(leftParts[2]);
			leftSource = gate;
		}
		
		if (leftSource == null) {
			throw new InvalidParameterException();
		}
		
		w.input = leftSource;
		
		if (leftSource instanceof Gate) {
			allGates.add((Gate)leftSource);
		}
	}
	
	// We expect s to contain either an integer or a wire name.
	private Source sourceFromString(String s) {
		Integer n;
		try {
			n = new Integer(s);
			return new Constant(n);
		} catch (NumberFormatException ex) {
			return wireWithName(s);
		}
	}
	
	Wire wireWithName(String name) {
		Wire w = wires.get(name);
		if (w == null) {
			w = new Wire();
			w.name = name;
			wires.put(name, w);
		}
		return w;
	}
	
	void dumpWires() {
		List<String> sortedWireNames = new ArrayList<String>(wires.keySet());
		Collections.sort(sortedWireNames);
		for (String name : sortedWireNames) {
			System.out.format("%s: %d\n", name, wires.get(name).signal);
		}
	}
}

class Day07 {
	public static void main(String[] args) throws IOException {
		doExample();
		Integer answer1 = doPartOne();
		doPartTwo(answer1);
	}
	
	private static void doExample() throws IOException {
		System.out.println("-- using example input --");
		Machine machine = new Machine("test-input.txt");
		machine.propagateSignals();
		machine.dumpWires();
	}
	
	private static Integer doPartOne() throws IOException {
		System.out.println("-- Part 1 --");
		Machine machine1 = new Machine("Day07-input.txt");
		machine1.propagateSignals();
		Integer answer1 = machine1.wireWithName("a").signal;
		System.out.println(answer1);
		return answer1;
	}
	
	private static void doPartTwo(Integer bSignal) throws IOException {
		System.out.println("-- Part 2 --");
		Machine machine2 = new Machine("Day07-input.txt");
		machine2.wireWithName("b").signal = bSignal;
		machine2.propagateSignals();
		Integer answer2 = machine2.wireWithName("a").signal;
		System.out.println(answer2);
	}
}