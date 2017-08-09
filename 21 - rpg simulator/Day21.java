import java.util.*;

class Player {
	String name;
	int hitPoints;
	int damagePoints;
	int armorPoints;
	private GoodieBag goodieBag;
	
	Player(String name, int hits, int damage, int armor) {
		this.name = name;
		this.hitPoints = hits;
		this.damagePoints = damage;
		this.armorPoints = armor;
		this.goodieBag = null;
	}
	
	int getGoldSpent() {
		return (goodieBag == null) ? 0 : goodieBag.getTotalCost();
	}
	
	void setGoodieBag(GoodieBag goodieBag) {
		if (this.goodieBag != null) {
			throw new IllegalArgumentException("Can't set a player's goodieBag twice.");
		}
		this.goodieBag = goodieBag;
		this.damagePoints += goodieBag.getTotalDamage();
		this.armorPoints += goodieBag.getTotalArmor();
	}
	
	public String toString() {
		return String.format("Player '%s': hits=%d, damage=%d, armor=%d", name, hitPoints, damagePoints, armorPoints);
	}
}

class Goodie {
	String name;
	int cost;
	int damage;
	int armor;
	
	Goodie(String name, int cost, int damage, int armor) {
		this.name = name;
		this.cost = cost;
		this.damage = damage;
		this.armor = armor;
	}

	public String toString() {
		return String.format("%s '%s': hits=%d, damage=%d, armor=%d", getClass().getSimpleName(), name, cost, damage, armor);
	}
}

class Weapon extends Goodie {
	static Weapon[] allWeapons = {
		new Weapon("Dagger", 8, 4, 0),
		new Weapon("Shortsword", 10, 5, 0),
		new Weapon("Warhammer", 25, 6, 0),
		new Weapon("Longsword", 40, 7, 0),
		new Weapon("Greataxe", 74, 8, 0),
	};

	Weapon(String name, int cost, int damage, int armor) {
		super(name, cost, damage, armor);
	}
}

class Armor extends Goodie {
	static Armor[] allArmors = {
		new Armor("<<NOT AN ARMOR>>", 0, 0, 0),  // A placeholder to have the same effect as "no armor".
		new Armor("Leather", 13, 0, 1),
		new Armor("Chainmail", 31, 0, 2),
		new Armor("Splintmail", 53, 0, 3),
		new Armor("Bandedmail", 75, 0, 4),
		new Armor("Platemail", 102, 0, 5),
	};

	Armor(String name, int cost, int damage, int armor) {
		super(name, cost, damage, armor);
	}
}

class Ring extends Goodie {
	static Ring[] allRings = {
		new Ring("<<NOT A RING>>", 0, 0, 0),  // A placeholder to have the same effect as "no ring".
		new Ring("Damage +1", 25, 1, 0),
		new Ring("Damage +2", 50, 2, 0),
		new Ring("Damage +3", 100, 3, 0),
		new Ring("Defense +1", 20, 0, 1),
		new Ring("Defense +2", 40, 0, 2),
		new Ring("Defense +3", 80, 0, 3),
	};

	Ring(String name, int cost, int damage, int armor) {
		super(name, cost, damage, armor);
	}
}

class GoodieBag {
	public static List<GoodieBag> getAllPossibleGoodieBags() {
		List<GoodieBag> list = new ArrayList<GoodieBag>();
		for (Weapon weapon : Weapon.allWeapons) {
			for (Armor armor : Armor.allArmors) {
				for (int r1 = 0; r1 < Ring.allRings.length - 1; r1++) {
					for (int r2 = r1 + 1; r2 < Ring.allRings.length; r2++) {
						Ring ring1 = Ring.allRings[r1];
						Ring ring2 = Ring.allRings[r2];
						list.add(new GoodieBag(weapon, armor, new Ring[]{ring1, ring2}));
					}
				}
			}
		}
		return list;
	}

	Weapon weapon;  // Exactly one.
	Armor armor;  // At most one.
	Ring[] rings;  // At most two.
	
	private GoodieBag(Weapon weapon, Armor armor, Ring[] rings) {
		this.weapon = weapon;
		this.armor = armor;
		this.rings = rings;
	}
	
	int getTotalCost() {
		int total = 0;
		total += weapon.cost;
		total += ((armor == null) ? 0 : armor.cost);
		for (Ring r : rings) {
			total += r.cost;
		}
		return total;
	}
	
	int getTotalDamage() {
		int total = 0;
		total += weapon.damage;
		total += ((armor == null) ? 0 : armor.damage);
		for (Ring r : rings) {
			total += r.damage;
		}
		return total;
	}
	
	int getTotalArmor() {
		int total = 0;
		total += weapon.armor;
		total += ((armor == null) ? 0 : armor.armor);
		for (Ring r : rings) {
			total += r.armor;
		}
		return total;
	}
	
	public String toString() {
		String[] ringNames = new String[rings.length];
		for (int i = 0; i < rings.length; i++) { ringNames[i] = rings[i].name; }
		return String.format("GoodieBag: weapon=%s, armor=%s, rings=%s", weapon.name, armor.name, String.join(", ", ringNames));
	}
}

class Game {
	boolean shouldLogMoves = false;
	
	Player attacker;
	Player defender;
	
	Game(Player p1, Player p2) {
		attacker = p1;
		defender = p2;
	}
	
	void playToEnd() {
		while (attacker.hitPoints > 0) {
			// The defender loses some number of hit points.
			int attackAmount = attacker.damagePoints - defender.armorPoints;
			if (attackAmount <= 0) { attackAmount = 1; }
			defender.hitPoints -= attackAmount;
			
			if (shouldLogMoves) {
				System.out.println(String.format("The %s deals %d-%d = %d damage; the %s goes down to %d hit points.", attacker.name, attacker.damagePoints, defender.armorPoints, attacker.damagePoints - defender.armorPoints, defender.name, defender.hitPoints));
			}
			
			// The attacker and defender switch places.
			Player temp = attacker;
			attacker = defender;
			defender = temp;
		}
		//System.out.println(String.format("GAME OVER -- winner is %s, gold spent = %d", defender.name, defender.getGoldSpent()));
	}
}

class Challenge {
	public static void main(String[] args) {
//		doExampleTest();
//		doPartOne();
		doPartTwo();
	}
	
	private static void doExampleTest() {
		Player player = new Player("player", 8, 5, 5);
		Player boss = new Player("boss", 12, 7, 2);
		Game game = new Game(player, boss);
		game.shouldLogMoves = true;
		game.playToEnd();
	}
	
	private static void doPartOne() {
		GoodieBag bestSoFar = null;
		for (GoodieBag goodieBag : GoodieBag.getAllPossibleGoodieBags()) {
			if (playerWinsWithGoodieBag(goodieBag)) {
				if ((bestSoFar == null) || (goodieBag.getTotalCost() < bestSoFar.getTotalCost())) {
					bestSoFar = goodieBag;
				}
			}
		}
		String bestName = ((bestSoFar == null) ? "<none>" : bestSoFar.toString());
		int bestBargain = ((bestSoFar == null) ? -1 : bestSoFar.getTotalCost());
		System.out.println(String.format("BEST BARGAIN IS %s, COST=%d", bestName, bestBargain));
	}
	
	private static void doPartTwo() {
		GoodieBag bestSoFar = null;
		for (GoodieBag goodieBag : GoodieBag.getAllPossibleGoodieBags()) {
			if (!playerWinsWithGoodieBag(goodieBag)) {
				if ((bestSoFar == null) || (goodieBag.getTotalCost() > bestSoFar.getTotalCost())) {
					bestSoFar = goodieBag;
				}
			}
		}
		String bestName = ((bestSoFar == null) ? "<none>" : bestSoFar.toString());
		int bestBargain = ((bestSoFar == null) ? -1 : bestSoFar.getTotalCost());
		System.out.println(String.format("BEST BARGAIN IS %s, COST=%d", bestName, bestBargain));
	}
	
	private static boolean playerWinsWithGoodieBag(GoodieBag goodieBag) {
		Player player = new Player("player", 100, 0, 0);
		player.setGoodieBag(goodieBag);
		Player boss = new Player("boss", 104, 8, 1);
		Game game = new Game(player, boss);
		game.playToEnd();
		return (game.defender == player);  // When the game ends, the winner is the defender.
	}
}

