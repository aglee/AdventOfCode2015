import Foundation

let dirURL = URL(fileURLWithPath: CommandLine.arguments[0]).deletingLastPathComponent()
let fileURL = dirURL.appendingPathComponent("input.txt")  // "input.txt" or "test.txt"
let fileContents = try! String(contentsOf: fileURL)
let lines = fileContents.components(separatedBy: "\n")

func lengthDiff(_ s: String) -> (originalLength: Int, skipped: Int) {
	let chars = Array(s.characters)
	var skipped = 2  // Pre-count the leading and trailing quotes.
	var i = 1  // Skip the leading quote.
	while i < chars.count - 1 {  // The -1 is to skip the trailing quote.
		let ch = chars[i]; i += 1
		if ch == "\\" {
			let ch2 = chars[i]; i += 1
			switch ch2 {
				case "\\", "\"": skipped += 1
				case "x": skipped += 3; i += 2
				default: fatalError("Unexpected character '\(ch2)' after backslash in '\(s)")
			}
		}
	}
	return (chars.count, skipped)
}


var totalSkipped = 0
for line in lines {
	let (orig, skipped) = lengthDiff(line)
	//print((orig, skipped, orig - skipped))
	totalSkipped += skipped
}
print(totalSkipped)

