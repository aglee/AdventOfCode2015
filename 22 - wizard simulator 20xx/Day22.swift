/*
Magic Missile costs 53 mana. It instantly does 4 damage.
Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit points.
Shield costs 113 mana. It starts an effect that lasts for 6 turns. While it is active, your armor is increased by 7.
Poison costs 173 mana. It starts an effect that lasts for 6 turns. At the start of each turn while it is active, it deals the boss 3 damage.
Recharge costs 229 mana. It starts an effect that lasts for 5 turns. At the start of each turn while it is active, it gives you 101 new mana.
*/
enum Spell {
	case missile, drain, shield, poison, recharge
	
	var cost: Int {
		switch self {
		case .missile: return 53
		case .drain: return 73
		case .shield: return 113
		case .poison: return 173
		case .recharge: return 229
		}
	}
	
	var effectDuration: Int {
		switch self {
		case .missile: return 0
		case .drain: return 0
		case .shield: return 6
		case .poison: return 6
		case .recharge: return 5
		}
	}
}

struct Player {
	var hit: Int
	var armor: Int = 0
	var mana: Int
	var effectTimers: [Spell: Int] = [:]
	
	init(hit: Int, mana: Int) {
		self.hit = hit
		self.mana = mana
	}
}

struct Boss {
	var hit: Int
	var damage: Int
	
	init(hit: Int, damage: Int) {
		self.hit = hit
		self.damage = damage
	}
}

enum Outcome { case playerWins, bossWins, nobodyWins }

enum Difficulty { case normal, hard }

struct Game {
	var player = Player(hit: 50, mana: 500)
	var boss = Boss(hit: 58, damage: 9)
	var totalSpent = 0
	let difficulty: Difficulty
	
	init(difficulty: Difficulty = .normal) {
		self.difficulty = difficulty
	}
	
	mutating func castSpell(_ spell: Spell) {
		switch spell {
		case .missile: boss.hit -= 4
		case .drain: boss.hit -= 2; player.hit += 2
		case .shield: player.armor += 7
		case .poison: ()
		case .recharge: ()
		}
		player.mana -= spell.cost
		totalSpent += spell.cost
		if spell.effectDuration > 0 {
			player.effectTimers[spell] = spell.effectDuration
		}
	}
	
	mutating func applyActiveEffects() {
		for (spell, timer) in player.effectTimers {
			switch spell {
			case .missile: ()
			case .drain: ()
			case .shield: if timer == 1 { player.armor -= 7 }
			case .poison: boss.hit -= 3
			case .recharge: player.mana += 101
			}
			player.effectTimers[spell] = (timer == 1 ? nil : timer - 1)
		}
	}
	
	func possibleSpells() -> [Spell] {
		var spells: [Spell] = []
		
		for s: Spell in [.missile, .drain, .shield, .poison, .recharge] {
			// Spells the player cannot afford are not allowed.
			if s.cost > player.mana {
				continue
			}

			// Spells that either don't have an active "effect" or whose
			// effect is about to expire are allowed.
			if player.effectTimers[s] == nil || player.effectTimers[s] == 1 {
				spells.append(s)
			}
		}
		
		return spells
	}
	
	mutating func playOneCycle(spell: Spell) -> Outcome {
		// Take player's turn.
		if self.difficulty == .hard {
			player.hit -= 1
			if player.hit <= 0 {
				return .bossWins
			}
		}
		applyActiveEffects()
		if boss.hit <= 0 {
			return .playerWins
		}
		castSpell(spell)
		if boss.hit <= 0 {
			return .playerWins
		}
		
		// Take boss's turn.
		applyActiveEffects()
		if boss.hit <= 0 {
			return .playerWins
		}
		let damage = max(boss.damage - player.armor, 1)
		player.hit -= damage
		if player.hit <= 0 {
			return .bossWins
		}

		// If we got this far, nobody has won the game yet.
		return .nobodyWins
	}
}

// Assumes game is not already in a state where one side has already won.
// lowestSoFar = -1 means we have no candidate answers yet.
func lowestTotalSpent(startingWith game: Game, lowestWinningTotalSoFar: Int) -> Int {
	var lowestSoFar = lowestWinningTotalSoFar
	let spells = game.possibleSpells()
	for s in spells {
		var g = game
		switch g.playOneCycle(spell: s) {
		case .playerWins:
			if (g.totalSpent < lowestSoFar) || (lowestSoFar == -1) {
				lowestSoFar = g.totalSpent
				//print("win: \(lowestSoFar)")
			}
		case .bossWins: ()
		case .nobodyWins:
			if (g.totalSpent < lowestSoFar) || (lowestSoFar == -1) {
				let b = lowestTotalSpent(startingWith: g, lowestWinningTotalSoFar: lowestSoFar)
				if (b < lowestSoFar) || (lowestSoFar == -1) {
					lowestSoFar = b
				}
			}
		}
	}
	return lowestSoFar
}

print("-- Part 1 --")
let answer1 = lowestTotalSpent(startingWith: Game(), lowestWinningTotalSoFar: -1)
print("Lowest mana spent is \(answer1).")

print("-- Part 2 --")
let answer2 = lowestTotalSpent(startingWith: Game(difficulty: .hard), lowestWinningTotalSoFar: -1)
print("Lowest mana spent is \(answer2).")


