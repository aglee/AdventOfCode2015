import Foundation

class Source: CustomStringConvertible {
	var signal: UInt16? { fatalError("can't get signal from abstract base class") }
	var abbrev: String { fatalError("can't get abbrev from abstract base class") }

	// MARK: - CustomStringConvertible methods
	
	var description: String { fatalError("can't get description from abstract base class") }
}

class Constant: Source {
	let value: UInt16
	
	init(value: UInt16) {
		self.value = value
	}

	// MARK: - Source overrides
	
	override var signal: UInt16? {
		print("signal: constant #\(value)")
		return value
	}
	
	override var abbrev: String {
		return description
	}
	
	// MARK: - CustomStringConvertible methods
	
	override var description: String {
		return "#\(value)"
	}
}

class Wire: Source {
	var name: String
	var line: String?
	var source: Source?
	
	init(name: String) {
		self.name = name
	}

	// MARK: - Source overrides
	
	override var signal: UInt16? {
		print("signal: wire #\(name), source \(source == nil ? "nil" : source!.abbrev)")
		return source?.signal
	}
	
	override var abbrev: String {
		return "#\(name)"
	}
	
	// MARK: - CustomStringConvertible methods
	
	override var description: String {
		if let source = self.source {
			return "#\(name)-\(source)"
		} else {
			return "#\(name)-NO_SOURCE"
		}
	}
}

class Gate: Source {
	var type: String
	var inputs: [Source]

	init(type: String, inputs: [Source]) {
		self.type = type
		self.inputs = inputs
	}
	
	// MARK: - Source overrides
	
	var marked = false
	override var signal: UInt16? {
		if marked {
			print("aha")
		}
		marked = true
	
	
		print("signal: \(description)")
		switch type {
			case "NOT": return applyOperator({ ~$0[0] })
			case "AND": return applyOperator({ $0[0] & $0[1] })
			case "OR": return applyOperator({ $0[0] | $0[1] })
			case "LSHIFT": return applyOperator({ $0[0] << $0[1] })
			case "RSHIFT": return applyOperator({ $0[0] >> $0[1] })
			default: fatalError("Unexpected gate type '\(type)'")
		}
	}
	
	override var abbrev: String {
		return type
	}
	
	// MARK: - CustomStringConvertible methods
	
	override var description: String {
		return "(\(type) \(inputs.map({ $0.abbrev }).joined(separator: " ")))"
//		return "(\(type) - \(inputs.count) inputs)"
	}
	
	// MARK: - Private methods
	
	private func applyOperator(_ op: ([UInt16]) -> UInt16) -> UInt16? {
		var signals: [UInt16] = []
		for source in inputs {
			guard let sig = source.signal else {
				return nil
			}
			signals.append(sig)
		}
		return op(signals)
	}
}

struct Machine {
	var wires: [String: Wire] = [:]
	
	func wire(named name: String) -> Wire? {
		return wires[name]
	}
	
	mutating func addConnections(_ desc: String) {
		var parts = desc.components(separatedBy: " ").filter({ !$0.isEmpty })
		
		let wire = wireAddedIfNeeded(name: parts.removeLast())
		wire.line = desc
		
		parts.removeLast()  // Remove the "->".
		
		let source: Source
		switch parts.count {
//			case 1: source = Constant(value: UInt16(parts[0])!)
			case 1: source = wireOrConstant(parts[0])
			case 2: source = Gate(type: parts[0], inputs: [wireOrConstant(parts[1])])
			case 3: source = Gate(type: parts[1], inputs: [wireOrConstant(parts[0]),
															wireOrConstant(parts[2])])
			default: fatalError("Unexpected lhs in description '\(desc)'")
		}
		
		wire.source = source
	}
	
	func dump() {
		for wireName in wires.keys.sorted() {
			print("\(wires[wireName]!)")
		}
	}
	
	// MARK: - Private methods
	
	private mutating func wireAddedIfNeeded(name: String) -> Wire {
		if let wire = wire(named: name) {
			return wire
		} else {
			let wire = Wire(name: name)
			wires[name] = wire
			return wire
		}
	}
	
	private mutating func wireOrConstant(_ nameOrValue: String) -> Source {
		if let value = UInt16(nameOrValue) {
			return Constant(value: value)
		} else {
			return wireAddedIfNeeded(name: nameOrValue)
		}
	}
}

let urlOfThisScript = URL(fileURLWithPath: CommandLine.arguments[0])
let dayName = urlOfThisScript.lastPathComponent.components(separatedBy: "-").first!
let pathToInputFile = urlOfThisScript.deletingLastPathComponent().appendingPathComponent(dayName).path + "-input.txt"
let inputString = try! String(contentsOfFile: pathToInputFile)
let inputLines = inputString.components(separatedBy: "\n").filter({ !$0.isEmpty })

var m = Machine()
for line in inputLines {
	m.addConnections(line)
}
m.dump()
print(m.wire(named: "a")?.signal as Any)



/*

test input:

123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i

output:

d: 72
e: 507
f: 492
g: 114
h: 65412
i: 65079
x: 123
y: 456

*/