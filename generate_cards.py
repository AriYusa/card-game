#!/usr/bin/env python3
"""
Card Game Generator
Generates all card types following game description constraints.
"""

import json
import random
from typing import Dict, List, Any


# Define perks
PERKS = ["Combat", "Diplomacy", "Science", "Engineering", "Medicine"]


def is_balanced_distribution(totals: Dict[str, int], target_per_perk: int, tolerance: float = 0.15) -> bool:
    """Check if distribution is balanced within tolerance."""
    min_allowed = target_per_perk * (1 - tolerance)
    max_allowed = target_per_perk * (1 + tolerance)
    
    for perk, total in totals.items():
        if total < min_allowed or total > max_allowed:
            return False
    return True


def generate_characters() -> List[Dict[str, Any]]:
    """
    Generate 30 characters.
    - Each has exactly 5 base points
    - Points are randomly distributed across perks
    - Ensures balanced distribution across all perks (within 25% of average)
    """
    max_attempts = 1000
    target_per_perk = 30  # 150 total points / 5 perks
    
    for attempt in range(max_attempts):
        characters = []
        perk_totals = {perk: 0 for perk in PERKS}
        
        for i in range(30):
            perks = {perk: 0 for perk in PERKS}
            
            # Distribute exactly 5 points randomly
            for _ in range(5):
                perk = random.choice(PERKS)
                perks[perk] += 1
            
            # Track totals
            for perk, value in perks.items():
                perk_totals[perk] += value
            
            characters.append({
                "id": f"char_{i+1:02d}",
                "perks": perks,
                "name": f"Character {i+1}"
            })
        
        # Check if distribution is balanced
        if is_balanced_distribution(perk_totals, target_per_perk):
            return characters
    
    # Fallback: return last attempt if max attempts reached
    print(f"Warning: Could not achieve balanced character distribution after {max_attempts} attempts")
    return characters


def generate_single_perk_developments() -> List[Dict[str, Any]]:
    """
    Generate 50 Single-Perk Development cards (+2).
    - 10 for each of the 5 perks
    """
    cards = []
    card_id = 1
    
    for perk in PERKS:
        for i in range(10):
            cards.append({
                "id": f"dev_single_{card_id:02d}",
                "name": f"{perk} Boost {i+1}",
                "type": "Permanent Perk Boost",
                "boost": {perk: 2},
                "description": f"Add +2 to {perk}"
            })
            card_id += 1
    
    return cards


def generate_dual_perk_developments() -> List[Dict[str, Any]]:
    """
    Generate 30 Dual-Perk Development cards (+1/+1).
    - Evenly distributed across all perk combinations
    - 10 possible combinations (5 choose 2) = 3 cards per combination
    """
    cards = []
    card_id = 1
    
    # Generate all perk pairs
    perk_pairs = []
    for i in range(len(PERKS)):
        for j in range(i+1, len(PERKS)):
            perk_pairs.append((PERKS[i], PERKS[j]))
    
    # Generate 3 cards per pair (3 * 10 = 30)
    for perk1, perk2 in perk_pairs:
        for i in range(3):
            cards.append({
                "id": f"dev_dual_{card_id:02d}",
                "name": f"{perk1}/{perk2} Boost {i+1}",
                "type": "Permanent Perk Boost",
                "boost": {perk1: 1, perk2: 1},
                "description": f"Add +1 to {perk1} and +1 to {perk2}"
            })
            card_id += 1
    
    return cards


def generate_special_developments() -> List[Dict[str, Any]]:
    """
    Generate 10 One-time Special Ability cards.
    - Randomly selected from template pool
    """
    special_templates = [
        {
            "name": "Double Duty",
            "description": "This character counts for 2 challenges per round",
            "effect": "character_double_assignment"
        },
        {
            "name": "Sabotage",
            "description": "Reduce another player's character perk by 2",
            "effect": "reduce_perk_2"
        },
        {
            "name": "Minor Sabotage",
            "description": "Reduce another player's character perk by 1",
            "effect": "reduce_perk_1"
        },
        {
            "name": "Prophecy",
            "description": "Can foresee the final challenge",
            "effect": "reveal_final_crisis"
        },
        {
            "name": "Second Chance",
            "description": "Reroll one failed challenge attempt",
            "effect": "reroll_challenge"
        },
        {
            "name": "Theft",
            "description": "Steal one development card from another player",
            "effect": "steal_dev_card"
        },
        {
            "name": "Inspiration",
            "description": "All your characters get +1 to all perks this round",
            "effect": "boost_all_perks_1"
        },
        {
            "name": "Emergency Training",
            "description": "Add +3 to any one perk for one challenge",
            "effect": "temp_boost_3"
        },
        {
            "name": "Resilience",
            "description": "Character cannot be exhausted this round",
            "effect": "prevent_exhaustion"
        },
        {
            "name": "Alliance",
            "description": "Draw 2 additional development cards",
            "effect": "draw_2_cards"
        },
        {
            "name": "Negotiator",
            "description": "You may trade Victory Points at 2:1 ratio this round",
            "effect": "favorable_vp_trade"
        },
        {
            "name": "Quick Recovery",
            "description": "Refresh one exhausted character immediately",
            "effect": "refresh_exhausted"
        },
        {
            "name": "Strategic Planning",
            "description": "Look at top 3 challenge cards and choose one",
            "effect": "choose_challenge"
        },
        {
            "name": "Resource Sharing",
            "description": "Helpers don't suffer debuff if challenge succeeds",
            "effect": "no_helper_debuff"
        },
        {
            "name": "Lucky Break",
            "description": "Automatically succeed on one challenge with gap of -1 or -2",
            "effect": "auto_success_small_gap"
        }
    ]
    
    # Randomly select 10 unique special abilities
    selected = random.sample(special_templates, 10)
    
    cards = []
    for i, template in enumerate(selected, 1):
        cards.append({
            "id": f"dev_special_{i:02d}",
            "name": template["name"],
            "type": "One-time Special Ability",
            "boost": {},
            "description": template["description"],
            "effect": template["effect"]
        })
    
    return cards


def generate_challenges() -> List[Dict[str, Any]]:
    """
    Generate 60 Challenge cards.
    - 20 Common (5-7 points, 1 VP)
    - 20 Elite (9-11 points, 2 VP)
    - 20 Heroic (13-15 points, 3 VP)
    - Ensures balanced perk distribution within each tier
    """
    max_attempts = 1000
    
    for attempt in range(max_attempts):
        challenges = []
        
        # Track requirements per tier
        tier_requirements = {
            "Common": {perk: 0 for perk in PERKS},
            "Elite": {perk: 0 for perk in PERKS},
            "Heroic": {perk: 0 for perk in PERKS}
        }
        
        # Common challenges (5-7 points, 1 VP)
        card_id = 1
        for i in range(20):
            num_perks = random.choice([1, 2])
            selected_perks = random.sample(PERKS, num_perks)
            
            total_points = random.randint(5, 7)
            requirements = {}
            
            if num_perks == 1:
                requirements[selected_perks[0]] = total_points
            else:
                first = random.randint(2, total_points - 2)
                second = total_points - first
                requirements[selected_perks[0]] = first
                requirements[selected_perks[1]] = second
            
            # Track totals
            for perk, value in requirements.items():
                tier_requirements["Common"][perk] += value
            
            req_str = " + ".join([f"{v} {k}" for k, v in requirements.items()])
            challenges.append({
                "id": f"challenge_common_{card_id:02d}",
                "name": f"Common Challenge {card_id}",
                "tier": "Common",
                "requirements": requirements,
                "total_points": total_points,
                "victory_points": 1,
                "description": f"Requires {req_str}"
            })
            card_id += 1
        
        # Elite challenges (9-11 points, 2 VP)
        card_id = 1
        for i in range(20):
            num_perks = random.choice([1, 2, 3])
            selected_perks = random.sample(PERKS, num_perks)
            
            total_points = random.randint(9, 11)
            requirements = {}
            
            if num_perks == 1:
                requirements[selected_perks[0]] = total_points
            elif num_perks == 2:
                first = random.randint(3, total_points - 3)
                second = total_points - first
                requirements[selected_perks[0]] = first
                requirements[selected_perks[1]] = second
            else:
                remaining = total_points
                for j, perk in enumerate(selected_perks):
                    if j == len(selected_perks) - 1:
                        requirements[perk] = remaining
                    else:
                        val = random.randint(2, remaining - 2 * (len(selected_perks) - j - 1))
                        requirements[perk] = val
                        remaining -= val
            
            # Track totals
            for perk, value in requirements.items():
                tier_requirements["Elite"][perk] += value
            
            req_str = " + ".join([f"{v} {k}" for k, v in requirements.items()])
            challenges.append({
                "id": f"challenge_elite_{card_id:02d}",
                "name": f"Elite Challenge {card_id}",
                "tier": "Elite",
                "requirements": requirements,
                "total_points": total_points,
                "victory_points": 2,
                "description": f"Requires {req_str}"
            })
            card_id += 1
        
        # Heroic challenges (13-15 points, 3 VP)
        card_id = 1
        for i in range(20):
            num_perks = random.choice([2, 3])
            selected_perks = random.sample(PERKS, num_perks)
            
            total_points = random.randint(13, 15)
            requirements = {}
            
            if num_perks == 2:
                first = random.randint(5, total_points - 5)
                second = total_points - first
                requirements[selected_perks[0]] = first
                requirements[selected_perks[1]] = second
            else:
                remaining = total_points
                for j, perk in enumerate(selected_perks):
                    if j == len(selected_perks) - 1:
                        requirements[perk] = remaining
                    else:
                        val = random.randint(3, remaining - 3 * (len(selected_perks) - j - 1))
                        requirements[perk] = val
                        remaining -= val
            
            # Track totals
            for perk, value in requirements.items():
                tier_requirements["Heroic"][perk] += value
            
            req_str = " + ".join([f"{v} {k}" for k, v in requirements.items()])
            challenges.append({
                "id": f"challenge_heroic_{card_id:02d}",
                "name": f"Heroic Challenge {card_id}",
                "tier": "Heroic",
                "requirements": requirements,
                "total_points": total_points,
                "victory_points": 3,
                "description": f"Requires {req_str}"
            })
            card_id += 1
        
        # Check if all tiers are balanced
        common_total = sum(tier_requirements["Common"].values())
        elite_total = sum(tier_requirements["Elite"].values())
        heroic_total = sum(tier_requirements["Heroic"].values())
        
        common_balanced = is_balanced_distribution(tier_requirements["Common"], common_total / 5, tolerance=0.35)
        elite_balanced = is_balanced_distribution(tier_requirements["Elite"], elite_total / 5, tolerance=0.35)
        heroic_balanced = is_balanced_distribution(tier_requirements["Heroic"], heroic_total / 5, tolerance=0.35)
        
        if common_balanced and elite_balanced and heroic_balanced:
            return challenges
    
    # Fallback: return last attempt if max attempts reached
    print(f"Warning: Could not achieve balanced challenge distribution after {max_attempts} attempts")
    return challenges


def generate_final_crisis() -> List[Dict[str, Any]]:
    """
    Generate 10 Final Crisis cards.
    - Each requires 130 total points
    - Varied requirement profiles (different perk distributions)
    """
    crises = []
    
    # Define different distribution strategies
    strategies = [
        # Combat-heavy
        {"Combat": 40, "Diplomacy": 20, "Science": 25, "Engineering": 25, "Medicine": 20},
        # Science-heavy
        {"Combat": 20, "Diplomacy": 20, "Science": 40, "Engineering": 30, "Medicine": 20},
        # Engineering-heavy
        {"Combat": 25, "Diplomacy": 20, "Science": 25, "Engineering": 40, "Medicine": 20},
        # Medicine-heavy
        {"Combat": 20, "Diplomacy": 25, "Science": 20, "Engineering": 25, "Medicine": 40},
        # Diplomacy-heavy
        {"Combat": 25, "Diplomacy": 40, "Science": 20, "Engineering": 20, "Medicine": 25},
        # Balanced
        {"Combat": 26, "Diplomacy": 26, "Science": 26, "Engineering": 26, "Medicine": 26},
        # Two-perk focus (Combat + Science)
        {"Combat": 35, "Diplomacy": 20, "Science": 35, "Engineering": 20, "Medicine": 20},
        # Two-perk focus (Engineering + Medicine)
        {"Combat": 20, "Diplomacy": 20, "Science": 20, "Engineering": 35, "Medicine": 35},
        # Three-perk focus
        {"Combat": 30, "Diplomacy": 30, "Science": 30, "Engineering": 20, "Medicine": 20},
        # Extreme specialization
        {"Combat": 50, "Diplomacy": 20, "Science": 20, "Engineering": 20, "Medicine": 20}
    ]
    
    for i, requirements in enumerate(strategies, 1):
        # Verify total is 130
        total = sum(requirements.values())
        
        primary_focus = max(requirements.items(), key=lambda x: x[1])[0]
        req_str = ", ".join([f"{v} {k}" for k, v in sorted(requirements.items(), key=lambda x: -x[1])])
        
        crises.append({
            "id": f"crisis_{i:02d}",
            "name": f"Final Crisis {i}: {primary_focus} Focused",
            "requirements": requirements,
            "total_points": total,
            "description": f"Requires {req_str} (Total: {total} points)"
        })
    
    return crises


def calculate_perk_distribution(characters: List[Dict]) -> Dict:
    """Calculate distribution of perk values across all characters."""
    distribution = {perk: {i: 0 for i in range(6)} for perk in PERKS}
    totals = {perk: 0 for perk in PERKS}
    
    for character in characters:
        for perk, value in character["perks"].items():
            distribution[perk][value] += 1
            totals[perk] += value
    
    return distribution, totals


def calculate_challenge_requirements(challenges: List[Dict], crises: List[Dict]) -> Dict:
    """Calculate total perk requirements for each challenge tier."""
    requirements_by_tier = {
        "Common": {perk: 0 for perk in PERKS},
        "Elite": {perk: 0 for perk in PERKS},
        "Heroic": {perk: 0 for perk in PERKS},
        "Final Crisis": {perk: 0 for perk in PERKS}
    }
    
    for challenge in challenges:
        tier = challenge["tier"]
        for perk, value in challenge["requirements"].items():
            requirements_by_tier[tier][perk] += value
    
    for crisis in crises:
        for perk, value in crisis["requirements"].items():
            requirements_by_tier["Final Crisis"][perk] += value
    
    return requirements_by_tier


def calculate_stats(characters: List[Dict], developments: List[Dict], 
                    challenges: List[Dict], crises: List[Dict]) -> Dict:
    """Calculate and return statistics about generated cards."""
    
    # Character stats
    char_totals = [sum(c["perks"].values()) for c in characters]
    avg_char_points = sum(char_totals) / len(char_totals)
    
    # Perk distribution
    perk_distribution, perk_totals = calculate_perk_distribution(characters)
    
    # Development stats
    single_perk = [d for d in developments if d["type"] == "Permanent Perk Boost" and len(d["boost"]) == 1]
    dual_perk = [d for d in developments if d["type"] == "Permanent Perk Boost" and len(d["boost"]) == 2]
    special = [d for d in developments if d["type"] == "One-time Special Ability"]
    
    # Average boost value
    total_boost = 0
    for d in developments:
        total_boost += sum(d["boost"].values())
    avg_boost = total_boost / len(developments) if developments else 0
    
    # Challenge stats
    common = [c for c in challenges if c["tier"] == "Common"]
    elite = [c for c in challenges if c["tier"] == "Elite"]
    heroic = [c for c in challenges if c["tier"] == "Heroic"]
    
    # Challenge requirements by tier
    challenge_requirements = calculate_challenge_requirements(challenges, crises)
    
    return {
        "characters": {
            "total": len(characters),
            "avg_points": round(avg_char_points, 2),
            "min_points": min(char_totals),
            "max_points": max(char_totals),
            "perk_distribution": perk_distribution,
            "perk_totals": perk_totals
        },
        "developments": {
            "total": len(developments),
            "single_perk": len(single_perk),
            "dual_perk": len(dual_perk),
            "special": len(special),
            "avg_boost": round(avg_boost, 2)
        },
        "challenges": {
            "total": len(challenges),
            "common": len(common),
            "elite": len(elite),
            "heroic": len(heroic),
            "requirements_by_tier": challenge_requirements
        },
        "final_crisis": {
            "total": len(crises)
        }
    }


def main():
    """Generate all cards and save to cards.json"""
    
    print("Generating card game data...")
    print("-" * 50)
    
    # Generate all card types
    print("Generating characters...")
    characters = generate_characters()
    
    print("Generating development cards...")
    single_devs = generate_single_perk_developments()
    dual_devs = generate_dual_perk_developments()
    special_devs = generate_special_developments()
    developments = single_devs + dual_devs + special_devs
    
    print("Generating challenge cards...")
    challenges = generate_challenges()
    
    print("Generating final crisis cards...")
    crises = generate_final_crisis()
    
    # Calculate statistics BEFORE saving
    print("\n" + "=" * 50)
    print("STATISTICS")
    print("=" * 50)
    
    stats = calculate_stats(characters, developments, challenges, crises)
    
    print(f"\nCharacters: {stats['characters']['total']}")
    print(f"  - Average points: {stats['characters']['avg_points']} (target: 5.0)")
    print(f"  - Range: {stats['characters']['min_points']}-{stats['characters']['max_points']}")
    
    print(f"\nPerk Totals (sum across all characters):")
    total_all_perks = sum(stats['characters']['perk_totals'].values())
    for perk in PERKS:
        total = stats['characters']['perk_totals'][perk]
        print(f"  {perk:12s}: {total} points")
    print(f"  {'Total':12s}: {total_all_perks} points")
    
    print(f"\nDevelopments: {stats['developments']['total']}")
    print(f"  - Single-Perk (+2): {stats['developments']['single_perk']}")
    print(f"  - Dual-Perk (+1/+1): {stats['developments']['dual_perk']}")
    print(f"  - Special Abilities: {stats['developments']['special']}")
    print(f"  - Average boost: {stats['developments']['avg_boost']} (target: 2.0)")
    
    print(f"\nChallenges: {stats['challenges']['total']}")
    print(f"  - Common (1 VP): {stats['challenges']['common']}")
    print(f"  - Elite (2 VP): {stats['challenges']['elite']}")
    print(f"  - Heroic (3 VP): {stats['challenges']['heroic']}")
    
    print(f"\nPerk Requirements by Challenge Tier:")
    for tier in ["Common", "Elite", "Heroic", "Final Crisis"]:
        reqs = stats['challenges']['requirements_by_tier'][tier]
        total_req = sum(reqs.values())
        print(f"  {tier}:")
        for perk in PERKS:
            print(f"    {perk:12s}: {reqs[perk]:3d} points")
        print(f"    {'Total':12s}: {total_req:3d} points")
    
    print(f"\nFinal Crisis: {stats['final_crisis']['total']}")
    
    # Save to separate JSON files
    print("\n" + "=" * 50)
    print("Saving cards to separate files...")
    
    with open("characters.json", "w") as f:
        json.dump(characters, f, indent=2)
    print("✓ Characters saved to characters.json")
    
    with open("developments.json", "w") as f:
        json.dump(developments, f, indent=2)
    print("✓ Developments saved to developments.json")
    
    with open("challenges.json", "w") as f:
        json.dump(challenges, f, indent=2)
    print("✓ Challenges saved to challenges.json")
    
    with open("final_crisis.json", "w") as f:
        json.dump(crises, f, indent=2)
    print("✓ Final Crisis saved to final_crisis.json")
    
    # Save statistics separately
    with open("statistics.json", "w") as f:
        json.dump(stats, f, indent=2)
    print("✓ Statistics saved to statistics.json")
    
    print("=" * 50)


if __name__ == "__main__":
    main()
