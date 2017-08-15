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

// Dynamic programming table for the subset sums problem.
struct DPTable {
	var weights: [Int]
	var targetSum: Int
	var matrix: [[Bool]]

	init(weights: [Int], targetSum: Int) {
		self.weights = weights.sorted()
		self.targetSum = targetSum

		assert(weights.count > 0)
		assert(weights[0] > 0)
		assert(targetSum > 0)

		let matrixRow = Array<Bool>(repeating: false, count: targetSum + 1)
		self.matrix = Array<[Bool]>(repeating: matrixRow, count: self.weights.count)

		self.populateFlags()
	}

	// The flag at (i, j) will indicate whether we can produce the sum j
	// using a subset of weights[0...i].
	private mutating func populateFlags() {
		// Column 0 is all true, because we can always make the sum 0 using the empty set.
		for i in 0..<matrix.count { self[i, 0] = true }

		// The rest of row 0 is false except for the column at index weights[0].
		// That is to say, given only the single weight weights[0], the only sums
		// we can make are 0 and that weight.
		if weights[0] <= targetSum { self[0, weights[0]] = true }

		// Populate each of the remaining rows using the values previously entered.
		for i in 1..<matrix.count {
			for j in 1...targetSum {
				if j < weights[i] {
					// For each sum less than weights[i], weights[i] can't contribute
					// to forming that sum, so the sum can be formed iff the sum can be
					// formed by the weights[0...i-1].
					self[i, j] = self[i - 1, j]
				} else {
					// There are two ways we could form a sum that is >= weights[i].
					// One is by excluding weights[i] and using weights[0...i-1].
					// The other is by including weights[i] and forming the rest, i.e.
					// j-weights[i], using the weights[0...i-1].
					self[i, j] = self[i - 1, j] || self[i - 1, j - weights[i]]
				}
			}
		}
	}

	func dumpFlags() {
		for i in 0..<matrix.count {
			var rowString = ""
			for j in 0...targetSum {
				rowString += self[i, j] ? "T " : "F "
			}
			print(rowString)
		}
	}

	func solutions() -> [[Int]] {
		return subsetsOfWeights(throughIndex: weights.count - 1, totalling: targetSum)
	}

	private func subsetsOfWeights(throughIndex i: Int, totalling j: Int) -> [[Int]] {
		if j == 0 {
			return [[]]
		}

		if i == 0 {
			if j == weights[0] {
				return [[weights[0]]]
			} else {
				return []
			}
		}

		if !self[i, j] {
			return []
		}

		var subsets: [[Int]] = []

		let ss = subsetsOfWeights(throughIndex: i - 1, totalling: j)
		subsets.append(contentsOf: ss)

		if j >= weights[i] {
			for ss in subsetsOfWeights(throughIndex: i - 1, totalling: j - weights[i]) {
				subsets.append([weights[i]] + ss)
			}
		}

		return subsets
	}

	subscript(_ i: Int, _ j: Int) -> Bool {
		get {
			return matrix[i][j]
		}
		set {
			matrix[i][j] = newValue
		}
	}
}

func solveSanta(weights: [Int], numGroups: Int) {
	// Construct the DP table.
	let totalWeight = weights.reduce(0, +)
	let targetSum = totalWeight / numGroups
	assert(totalWeight == numGroups * targetSum, "totalWeight is not a multiple of \(numGroups)")
	let table = DPTable(weights: weights, targetSum: targetSum)
	
	// Find all candidate groups of weights.
	NSLog("finding groups of weights that add up to \(targetSum)")
	let allGroups = table.solutions()
	NSLog("found \(allGroups.count) possible groups")
	
	// Find all groups that have the smallest group size.
	var smallestGroupSize = weights.count + 1
	for sol in allGroups {
		if sol.count < smallestGroupSize {
			smallestGroupSize = sol.count
		}
	}
	print("smallest group size is \(smallestGroupSize)")
	let smallestGroups = allGroups.filter({ return $0.count == smallestGroupSize })
	print("found \(smallestGroups.count) groups with size \(smallestGroupSize)")

	// Among those, find the smallest "quantum entanglement"
	// (product of the group's elements).
	var smallestQuant = -1
	for sol in smallestGroups {
		let q = sol.reduce(1, *)
		if q < smallestQuant || smallestQuant == -1 {
			smallestQuant = q
		}
	}
	print("smallest quant among shortest groups is \(smallestQuant)")
}

func doSanityCheck(targetSum: Int) {
	let weights = [2, 3, 7, 8, 10]
	print("weights: ", weights)
	print("targetSum:", targetSum)
	let table = DPTable(weights: weights, targetSum: targetSum)
	table.dumpFlags()
	print(table.solutions())
	print()
}

//doSanityCheck(targetSum: 10)
//doSanityCheck(targetSum: 11)

let weights = readInputLines().map({ return Int($0)! })
print("-- Part 1 --")
solveSanta(weights: weights, numGroups: 3)
print("-- Part 2 --")
solveSanta(weights: weights, numGroups: 4)

