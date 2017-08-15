import Foundation

func readInputLines() -> [String] {
	do {
		let currentDirectoryURL = URL(fileURLWithPath: FileManager.default.currentDirectoryPath)
		let url = currentDirectoryURL.appendingPathComponent("input.txt")
		let fileContents = try String(contentsOf: url)
		return fileContents.components(separatedBy: "\n")
	} catch {
		print("ERROR: Could not load input file.")
		return []
	}
}

let lines = readInputLines()

enum Instruction {
	case hlf(reg: String)
	case tpl(reg: String)
	case inc(reg: String)
	case jmp(off: Int)
	case jie(reg: String, off: Int)
	case jio(reg: String, off: Int)

	init?(_ s: String) {
		let parts = s.components(separatedBy: " ")
		let r = parts[1].substring(to: s.index(s.startIndex, offsetBy: 1))

		switch parts[0] {
		case "hlf": self = .hlf(reg: r)
		case "tpl": self = .tpl(reg: r)
		case "inc": self = .inc(reg: r)
		case "jmp": self = .jmp(off: Int(parts[1])!)
		case "jie": self = .jie(reg: r, off: Int(parts[2])!)
		case "jio": self = .jio(reg: r, off: Int(parts[2])!)
		default: return nil
		}
	}
}

class Machine {
	let program: [Instruction] = readInputLines().map({ Instruction($0)! })
	var pc = 0
	var registers = ["a": 0, "b": 0]

	func exec(a: Int, b: Int) {
		registers["a"] = a
		registers["b"] = b
		pc = 0
		while pc >= 0 && pc < program.count {
			execInstruction()
		}
		print("After running the program, we have register b = \(registers["b"]!).")
	}

	private func execInstruction() {
		var offset = 1
		switch program[pc] {
		case .hlf(let reg): registers[reg] = registers[reg]! / 2
		case .tpl(let reg): registers[reg] = registers[reg]! * 3
		case .inc(let reg): registers[reg] = registers[reg]! + 1
		case .jmp(let off): offset = off
		case .jie(let reg, let off): if registers[reg]! & 1 == 0 { offset = off }
		case .jio(let reg, let off): if registers[reg]! == 1 { offset = off }
		}
		pc += offset
	}
}

print("-- Part 1 --")
Machine().exec(a: 0, b: 0)

print("-- Part 2 --")
Machine().exec(a: 1, b: 0)

/*
hlf r sets register r to half its current value, then continues with the next instruction.
tpl r sets register r to triple its current value, then continues with the next instruction.
inc r increments register r, adding 1 to it, then continues with the next instruction.
jmp offset is a jump; it continues with the instruction offset away relative to itself.
jie r, offset is like jmp, but only jumps if register r is even ("jump if even").
jio r, offset is like jmp, but only jumps if register r is 1 ("jump if one", not odd).
*/

