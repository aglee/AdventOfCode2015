import Foundation

// Figured out the pattern by eyeballing.
// Note this is a 1-based ordinal number.
func ordinalNumberOfGridEntry(_ row: Int, _ col: Int) -> Int {
	let firstInRow = 1 + (row * (row - 1))/2
	return firstInRow + (col - 1)*row + (col - 1)*col/2
}

// Reproducing the visual aid from the problem statement, as a
// sanity check that the ordinalNumberOfGridEntry function works.
print("This is order in which the grid is filled:")
for row in 1...6 {
	var rowString = ""
	for col in 1...6 {
		rowString += String(format: "%4d", ordinalNumberOfGridEntry(row, col))
	}
	print(rowString)
}

// To continue, please consult the code grid in the manual.  Enter the code at row 2978, column 3083.

let row = 2978
let col = 3083
let n = ordinalNumberOfGridEntry(row, col)
var code = 20151125
for _ in 0..<n-1 {
	code = (code * 252533) % 33554393
}
print("code is \(code)")


