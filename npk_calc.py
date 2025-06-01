import numpy as np



class PlantRequirements:
    def __init__(self, name, n, p, k, target_EC):
        self.name, self.n, self.p, self.k, self.target_EC = name, n, p, k, target_EC

    @property
    def ratio(self):                                    # Normalisierte N-P-K-Anteile
        vec = np.array([self.n, self.p, self.k], float)
        return vec / vec.sum()


class Fertilizer:
    def __init__(self, name, n, p, k, ml_per_L_per_mS, density_g_per_ml=1.0):
        self.name = name
        self.n = n
        self.p = p
        self.k = k
        self.ml_per_L_per_mS = ml_per_L_per_mS          # “EC-Leitfähigkeit” der Flasche
        self.density_g_per_ml = density_g_per_ml        # Dichte der Flasche (g/ml)

    @property
    def npk_vec(self):
        return np.array([self.n, self.p, self.k], float)

def mix_volumes(target: PlantRequirements, bottles: list[Fertilizer]):
    A = np.vstack([f.npk_vec for f in bottles]).T  # 3 × n Matrix
    t = target.ratio                               # 3-Vektor

    # solve A * v = t  
    v_rel, *_ = np.linalg.lstsq(A, t, rcond=None)
    v_rel = np.maximum(v_rel, 0)                   #  –0 → 0
    v_rel /= v_rel.sum()                           # norm


    ec_per_ml = np.array([1/f.ml_per_L_per_mS for f in bottles])
    ec_mix = (v_rel * ec_per_ml).sum()
    scale = target.target_EC / ec_mix
    v_ml = v_rel * scale                           # ml pro L

    return {bottles[i].name: v for i, v in enumerate(v_ml)}

#def mix_volumes(target: PlantRequirements, bottles):
#    A = np.column_stack([b.npk_vec for b in bottles])  # 3×n
#    t = target.ratio
#
#    v_rel, *_ = np.linalg.lstsq(A, t, rcond=None)      # kein .T !
#    v_rel = np.clip(v_rel, 0, None)
#    v_rel /= v_rel.sum()                               # relatives Verhältnis (∑=1)
#
#    ec_per_ml = 1 / np.array([b.ml_per_L_per_mS for b in bottles])
#    scale     = target.target_EC / (v_rel @ ec_per_ml) # auf Soll-EC skalieren
#    return v_rel * scale    

#
# calibration log; 350ml of water.
#
# 2ml of Micro increased EC by 1.145 mS/cm  -> 2ml per 0.35l per 1.145mS/cm = 4.99 ml/L/mS/cm
# 2ml of Grow increased EC by 0.940 mS/cm   -> 2ml per 0.35l per 0.940mS/cm = 6.08 ml/L/mS/cm
# 2ml of Bloom increased EC by 0.750 mS/cm  -> 2ml per 0.35l per 0.750mS/cm = 7.62 ml/L/mS/cm
#
#

micro  = Fertilizer("Micro", 2, 0, 0, 4.99, density_g_per_ml=1.1)   
grow   = Fertilizer("Grow" , 1, 0, 4, 6.08)   
bloom  = Fertilizer("Bloom", 1, 3, 4, 7.62, density_g_per_ml=1.1)   

AN_bottles = [micro, grow, bloom]

z_micro  = Fertilizer("Zeus Micro", 6.5, 0, 1.,  100.)   #measure exact values for ml/mS/cm
z_grow   = Fertilizer("Zeus Grow" , 5.5, 5, 10., 100.)   #measure exact values for ml/mS/cm
z_bloom  = Fertilizer("Zeus Bloom", 1.2, 5.4, 6, 100.)   #measure exact values for ml/mS/cm
k_stock  = Fertilizer("K Stock"  , 0, 0, 35.1,   100.)   # K₂SO₄ from Raiffeisen etc.

Zeus_bottles = [z_micro, z_grow, k_stock]#z_bloom]


# ---------- Zierpflanzen ----------
buntnessel = PlantRequirements("Buntnessel", 2, 1, 3, 1.0)

# ---------- Blattgemüse ----------
lettuce   = PlantRequirements("Lettuce"  , 2, 1, 3, 1.2)
basil     = PlantRequirements("Basil"    , 2, 1, 3, 1.2)
coriander = PlantRequirements("Coriander", 2, 1, 3, 1.2)
rucola    = PlantRequirements("Rucola"   , 2, 1, 3, 1.2)


# ---------- Fruchtgemüse ----------
# Tomate: vegetatives Stadium (bis Blütenansatz)
tomatoes_grow  = PlantRequirements("Tomatoes Grow" , 2, 1, 2, 1.8)

# Tomate: Frucht-/Ertragsphase
tomatoes_fruit = PlantRequirements("Tomatoes Fruit", 1.5, 0.7, 2.5, 2.0)

# Gurke (gesamtes Kulturfenster – braucht viel K, moderaten N, wenig P)
cucumbers      = PlantRequirements("Cucumbers"     , 2, 0.7, 3, 1.8)

tom_cuc_grow = PlantRequirements("Tom Cuc Grow" , 2, 1, 3, 1.8)
tom_cuc_fruit = PlantRequirements("Tom Cuc Fruit", 1.7, 0.7, 4, 2.0)

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate fertilizer volumes for a target plant.")
    parser.add_argument("target", type=str, 
                        help="Target plant name (e.g., lettuce, basil, coriander, rucola, tomatoes_grow, tomatoes_fruit, cucumbers)")
    parser.add_argument("liters", type=float, 
                        help="Volume in liters to calculate the fertilizer volumes for.")
    # switch to zeus + K_stock bottles
    parser.add_argument("-z", "--zeus", action="store_true", 
                        help="Use Zeus bottles instead of AN bottles.")
    args = parser.parse_args()

    # Map names to target objects
    targets = {
        "lettuce": lettuce,
        "basil": basil,
        "coriander": coriander,
        "rucola": rucola,
        "tomatoes_grow": tomatoes_grow,
        "tomatoes_fruit": tomatoes_fruit,
        "cucumbers": cucumbers,
        "buntnessel": buntnessel,
        "tom_cuc_grow": tom_cuc_grow,
        "tom_cuc_fruit": tom_cuc_fruit,
    }

    if args.target not in targets:
        print("Error: unknown target plant name.")
        print("Available targets:", ", ".join(targets.keys()))
        exit(1)

    target = targets[args.target]


bottles =  AN_bottles # Zeus_bottles
if args.zeus:
    bottles = Zeus_bottles

volumes = mix_volumes(target, bottles)

sanity_check = np.zeros(3, float)
for b, ml in volumes.items():
    bottle = None
    for f in bottles:
        if f.name == b:
            bottle = f
            break
    print(f"{b:5}: {ml:.2f} ml  / L, so {ml*args.liters:.2f} ml or {bottle.density_g_per_ml * ml *args.liters:.2f} g")
    #find bottle by name in bottles
    
    sanity_check += np.array([bottle.n, bottle.p, bottle.k], float)*ml
#normalise so last entry is the same as the target
sanity_check *= target.k / sanity_check[2]
print(f"\nSanity check:")
print(f"Sum: {sanity_check}")
print(f"Target: {[target.n, target.p, target.k]}, EC : {target.target_EC}")

#normalise the bottles so that the smallest is 1
min_ml = min([ml for b, ml in volumes.items()])
bottle_fractions = []
bottle_names = []
for b, ml in volumes.items():
    bottle_names.append(b)
    bottle_fractions.append(ml / min_ml)

print(f"\nNormalized ratios:")
for b, ml in zip(bottle_names, bottle_fractions):
    print(f"{b:5}: {ml:.2f}")

