import Foundation

protocol Source: CustomStringConvertible {
	var signal: UInt16? { get }
	var abbrev: String { get }
}

struct Constant: Source {
	let value: UInt16
	var signal: UInt16? {
		return value
	}
	
	var abbrev: String {
		return description
	}
	
	var description: String {
		return "#\(value)"
	}
}

class Wire: Source {
	var name: String
	var line: String?
	var source: Source?
	var signal: UInt16? {
		return source?.signal
	}
	
	init(name: String) {
		self.name = name
	}

	var abbrev: String {
		return "#\(name)"
	}
	
	var description: String {
		if let source = self.source {
			return "#\(name)-\(source)"
		} else {
			return "#\(name)-NO_SOURCE"
		}
	}
}

struct Gate: Source {
	var marked = false
	init(type: String, inputs: [Source]) {
		self.type = type
		self.inputs = inputs
	}
	
	var type: String
	var inputs: [Source]
	var signal: UInt16? {
		switch type {
			case "NOT": return applyOperator({ ~$0[0] })
			case "AND": return applyOperator({ $0[0] & $0[1] })
			case "OR": return applyOperator({ $0[0] | $0[1] })
			case "LSHIFT": return applyOperator({ $0[0] << $0[1] })
			case "RSHIFT": return applyOperator({ $0[0] >> $0[1] })
			default: fatalError("Unexpected gate type '\(type)'")
		}
	}
	
	var abbrev: String {
		return type
	}
	
	var description: String {
		return "(\(type) \(inputs.map({ $0.abbrev }).joined(separator: " ")))"
//		return "(\(type) - \(inputs.count) inputs)"
	}
	
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
//			if let signal = wires[wireName]!.signal {
//				print("\(wireName): \(signal)")
//			} else {
//				print("\(wireName): nil")
//			}
		}
	}
	
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
//print(m.wire(named: "a")?.signal)



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