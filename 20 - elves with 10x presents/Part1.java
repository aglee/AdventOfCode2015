import java.util.*;

class Part1 {
	public static void main(String[] args) {
		int targetNumber = 29_000_000;
		int numHouses = targetNumber;
		int numElves = numHouses;
		int[] giftCounts = new int[numHouses];
		for (int elf = 1; elf < numElves; elf++) {
			for (int house = elf; house < numHouses; house += elf) {
				giftCounts[house] += 10 * elf;
			}
		}
		for (int house = 0; house < giftCounts.length; house++) {
			if (giftCounts[house] >= targetNumber) {
				System.out.println("house index is " + house + ", gifts = " + giftCounts[house]);
				System.exit(0);
			}
		}
	}
}

