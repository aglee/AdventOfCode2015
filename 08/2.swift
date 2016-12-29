import Foundation

let dirURL = URL(fileURLWithPath: CommandLine.arguments[0]).deletingLastPathComponent()
let fileURL = dirURL.appendingPathComponent("input.txt")  // "input.txt" or "test.txt"
let fileContents = try! String(contentsOf: fileURL)
let lines = fileContents.components(separatedBy: "\n")

func quotingDiff(_ s: String) -> (orig: Int, added: Int) {
	let chars = Array(s.characters)
	var added = 2  // Pre-count the surrounding quotes that would be added.
	for ch in Array(s.characters) {
		if ch == "\\" || ch == "\"" {
			added += 1
		}
	}
	return (chars.count, added)
}

var totalAdded = 0
for line in lines {
	let (orig, added) = quotingDiff(line)
	print((orig, added, orig + added))
	totalAdded += added
}
print(totalAdded)

