"""
Ingredient Suggestion Service
Provides autocomplete suggestions for common cooking ingredients
"""

from typing import List, Dict, Any, Optional
from app.database import get_db_connection, get_db_cursor

# Comprehensive list of 500+ common ingredients
COMMON_INGREDIENTS = [
    # Proteins - Poultry
    "Egg", "Egg White", "Egg Yolk", "Chicken", "Chicken Breast", "Chicken Thigh",
    "Chicken Wing", "Chicken Drumstick", "Ground Chicken", "Turkey", "Turkey Breast",
    "Duck", "Duck Breast", "Quail", "Goose",
    
    # Proteins - Meat
    "Beef", "Ground Beef", "Beef Steak", "Beef Brisket", "Beef Ribs", "Beef Tenderloin",
    "Pork", "Pork Chop", "Pork Belly", "Ground Pork", "Pork Tenderloin", "Pork Ribs",
    "Bacon", "Ham", "Sausage", "Chorizo", "Salami", "Prosciutto", "Pancetta",
    "Lamb", "Lamb Chop", "Ground Lamb", "Lamb Shank", "Veal", "Venison",
    
    # Proteins - Seafood
    "Fish", "Salmon", "Tuna", "Cod", "Halibut", "Tilapia", "Sea Bass", "Mackerel",
    "Trout", "Snapper", "Mahi Mahi", "Catfish", "Anchovy", "Sardine",
    "Shrimp", "Prawn", "Crab", "Crab Meat", "Lobster", "Crawfish",
    "Squid", "Calamari", "Octopus", "Clam", "Mussel", "Oyster", "Scallop",
    
    # Proteins - Plant-Based
    "Tofu", "Firm Tofu", "Silken Tofu", "Tempeh", "Seitan", "Edamame",
    
    # Vegetables - Leafy Greens
    "Spinach", "Kale", "Lettuce", "Romaine Lettuce", "Arugula", "Cabbage",
    "Napa Cabbage", "Red Cabbage", "Bok Choy", "Chinese Cabbage", "Collard Greens",
    "Swiss Chard", "Watercress", "Endive", "Radicchio", "Mustard Greens",
    
    # Vegetables - Cruciferous
    "Broccoli", "Cauliflower", "Brussels Sprouts", "Kohlrabi",
    
    # Vegetables - Root Vegetables
    "Potato", "Sweet Potato", "Yam", "Carrot", "Beet", "Turnip", "Parsnip",
    "Radish", "Daikon", "Rutabaga", "Jicama", "Cassava", "Taro",
    
    # Vegetables - Alliums
    "Onion", "Red Onion", "White Onion", "Yellow Onion", "Green Onion", "Scallion",
    "Spring Onion", "Shallot", "Garlic", "Leek", "Chives",
    
    # Vegetables - Nightshades
    "Tomato", "Cherry Tomato", "Grape Tomato", "Roma Tomato", "Plum Tomato",
    "Bell Pepper", "Red Bell Pepper", "Green Bell Pepper", "Yellow Bell Pepper",
    "Chili Pepper", "Jalapeño", "Serrano Pepper", "Habanero", "Poblano",
    "Cayenne Pepper", "Thai Chili", "Bird's Eye Chili", "Eggplant", "Japanese Eggplant",
    
    # Vegetables - Squash & Gourds
    "Zucchini", "Yellow Squash", "Butternut Squash", "Acorn Squash", "Spaghetti Squash",
    "Pumpkin", "Cucumber", "Bitter Melon", "Winter Melon",
    
    # Vegetables - Other
    "Mushroom", "Shiitake Mushroom", "Portobello Mushroom", "Button Mushroom",
    "Oyster Mushroom", "Enoki Mushroom", "Porcini Mushroom",
    "Asparagus", "Celery", "Corn", "Baby Corn", "Green Bean", "String Bean",
    "Snap Pea", "Snow Pea", "Bean Sprout", "Bamboo Shoot", "Water Chestnut",
    "Artichoke", "Fennel", "Okra", "Rhubarb",
    
    # Fruits - Citrus
    "Lemon", "Lime", "Orange", "Blood Orange", "Tangerine", "Clementine",
    "Grapefruit", "Pomelo", "Yuzu", "Calamansi",
    
    # Fruits - Berries
    "Strawberry", "Blueberry", "Raspberry", "Blackberry", "Cranberry",
    "Gooseberry", "Elderberry", "Goji Berry",
    
    # Fruits - Tropical
    "Mango", "Pineapple", "Papaya", "Passion Fruit", "Dragon Fruit", "Guava",
    "Lychee", "Longan", "Rambutan", "Star Fruit", "Jackfruit", "Durian",
    
    # Fruits - Stone Fruits
    "Peach", "Nectarine", "Plum", "Apricot", "Cherry", "Date",
    
    # Fruits - Other
    "Apple", "Pear", "Banana", "Plantain", "Grape", "Watermelon", "Cantaloupe",
    "Honeydew", "Kiwi", "Pomegranate", "Fig", "Persimmon", "Avocado", "Coconut",
    
    # Grains & Cereals
    "Rice", "White Rice", "Brown Rice", "Jasmine Rice", "Basmati Rice", "Wild Rice",
    "Sticky Rice", "Arborio Rice", "Sushi Rice",
    "Wheat", "Wheat Flour", "All-Purpose Flour", "Bread Flour", "Cake Flour",
    "Whole Wheat Flour", "Self-Rising Flour", "Pastry Flour",
    "Quinoa", "Oats", "Rolled Oats", "Steel Cut Oats", "Barley", "Bulgur",
    "Couscous", "Farro", "Millet", "Buckwheat", "Cornmeal", "Polenta", "Grits",
    
    # Pasta & Noodles
    "Pasta", "Spaghetti", "Linguine", "Fettuccine", "Penne", "Rigatoni",
    "Macaroni", "Fusilli", "Farfalle", "Lasagna", "Ravioli", "Tortellini",
    "Orzo", "Angel Hair", "Vermicelli",
    "Noodle", "Rice Noodle", "Egg Noodle", "Ramen Noodle", "Udon Noodle",
    "Soba Noodle", "Glass Noodle", "Rice Vermicelli", "Pad Thai Noodle",
    
    # Bread & Baked Goods
    "Bread", "White Bread", "Whole Wheat Bread", "Sourdough", "Baguette",
    "Ciabatta", "Focaccia", "Pita", "Naan", "Tortilla", "Wrap",
    
    # Legumes & Beans
    "Bean", "Black Bean", "Kidney Bean", "Pinto Bean", "Navy Bean",
    "Lima Bean", "Cannellini Bean", "Great Northern Bean",
    "Chickpea", "Garbanzo Bean", "Lentil", "Red Lentil", "Green Lentil",
    "Split Pea", "Black-Eyed Pea",
    
    # Nuts & Seeds
    "Peanut", "Peanut Butter", "Almond", "Almond Butter", "Cashew",
    "Walnut", "Pecan", "Pistachio", "Hazelnut", "Macadamia Nut",
    "Pine Nut", "Brazil Nut", "Chestnut",
    "Sesame Seed", "Sunflower Seed", "Pumpkin Seed", "Chia Seed",
    "Flax Seed", "Poppy Seed", "Hemp Seed",
    
    # Dairy
    "Milk", "Whole Milk", "Skim Milk", "2% Milk", "Buttermilk", "Evaporated Milk",
    "Condensed Milk", "Heavy Cream", "Whipping Cream", "Half and Half",
    "Sour Cream", "Crème Fraîche",
    "Butter", "Unsalted Butter", "Salted Butter", "Clarified Butter", "Ghee",
    "Cheese", "Cheddar", "Mozzarella", "Parmesan", "Pecorino Romano",
    "Swiss Cheese", "Gruyere", "Brie", "Camembert", "Blue Cheese", "Gorgonzola",
    "Feta", "Goat Cheese", "Ricotta", "Mascarpone", "Cream Cheese",
    "Cottage Cheese", "Provolone", "Monterey Jack", "Pepper Jack",
    "Yogurt", "Greek Yogurt", "Plain Yogurt",
    
    # Dairy Alternatives
    "Almond Milk", "Soy Milk", "Coconut Milk", "Oat Milk", "Rice Milk",
    "Cashew Milk", "Vegan Butter", "Vegan Cheese",
    
    # Herbs - Fresh
    "Basil", "Thai Basil", "Holy Basil", "Cilantro", "Coriander Leaf",
    "Parsley", "Flat-Leaf Parsley", "Mint", "Spearmint", "Peppermint",
    "Dill", "Oregano", "Thyme", "Rosemary", "Sage", "Tarragon",
    "Chives", "Lemongrass", "Bay Leaf", "Curry Leaf", "Kaffir Lime Leaf",
    
    # Spices - Ground
    "Salt", "Sea Salt", "Kosher Salt", "Black Pepper", "White Pepper",
    "Cayenne Pepper", "Red Pepper Flakes", "Paprika", "Smoked Paprika",
    "Cumin", "Coriander", "Turmeric", "Ginger Powder", "Garlic Powder",
    "Onion Powder", "Cinnamon", "Nutmeg", "Clove", "Cardamom",
    "Allspice", "Star Anise", "Fennel Seed", "Caraway Seed",
    "Mustard Seed", "Celery Seed", "Fenugreek", "Sumac", "Za'atar",
    
    # Spice Blends
    "Curry Powder", "Garam Masala", "Chinese Five Spice", "Italian Seasoning",
    "Herbes de Provence", "Cajun Seasoning", "Taco Seasoning", "Chili Powder",
    "Everything Bagel Seasoning", "Old Bay Seasoning",
    
    # Oils & Fats
    "Olive Oil", "Extra Virgin Olive Oil", "Vegetable Oil", "Canola Oil",
    "Sunflower Oil", "Safflower Oil", "Peanut Oil", "Avocado Oil",
    "Coconut Oil", "Sesame Oil", "Toasted Sesame Oil", "Grapeseed Oil",
    "Corn Oil", "Palm Oil", "Lard", "Shortening", "Cooking Spray",
    
    # Vinegars
    "Vinegar", "White Vinegar", "Apple Cider Vinegar", "Balsamic Vinegar",
    "Red Wine Vinegar", "White Wine Vinegar", "Rice Vinegar", "Rice Wine Vinegar",
    "Sherry Vinegar", "Champagne Vinegar", "Malt Vinegar",
    
    # Sauces - Asian
    "Soy Sauce", "Dark Soy Sauce", "Light Soy Sauce", "Tamari",
    "Fish Sauce", "Oyster Sauce", "Hoisin Sauce", "Plum Sauce",
    "Sweet Chili Sauce", "Sriracha", "Sambal Oelek", "Gochujang",
    "Teriyaki Sauce", "Ponzu", "Mirin", "Sake", "Shaoxing Wine",
    
    # Sauces - Western
    "Tomato Sauce", "Marinara Sauce", "Tomato Paste", "Tomato Puree",
    "Ketchup", "Mustard", "Dijon Mustard", "Whole Grain Mustard",
    "Mayonnaise", "Aioli", "BBQ Sauce", "Hot Sauce", "Tabasco",
    "Worcestershire Sauce", "A1 Sauce", "Ranch Dressing",
    "Caesar Dressing", "Salsa", "Pico de Gallo", "Guacamole",
    
    # Curry Pastes & Asian Condiments
    "Red Curry Paste", "Green Curry Paste", "Yellow Curry Paste",
    "Massaman Curry Paste", "Panang Curry Paste",
    "Miso Paste", "White Miso", "Red Miso", "Tahini", "Harissa",
    
    # Sweeteners
    "Sugar", "White Sugar", "Granulated Sugar", "Brown Sugar",
    "Light Brown Sugar", "Dark Brown Sugar", "Powdered Sugar",
    "Confectioners Sugar", "Honey", "Maple Syrup", "Agave Nectar",
    "Corn Syrup", "Molasses", "Stevia", "Monk Fruit", "Palm Sugar",
    "Coconut Sugar", "Jaggery",
    
    # Baking Ingredients
    "Baking Powder", "Baking Soda", "Yeast", "Active Dry Yeast",
    "Instant Yeast", "Vanilla Extract", "Almond Extract",
    "Cocoa Powder", "Chocolate Chips", "Dark Chocolate", "Milk Chocolate",
    "White Chocolate", "Gelatin", "Cornstarch", "Tapioca Starch",
    "Potato Starch", "Arrowroot", "Cream of Tartar",
    
    # Canned & Preserved
    "Canned Tomato", "Diced Tomato", "Crushed Tomato", "Tomato Sauce",
    "Coconut Cream", "Canned Coconut Milk", "Coconut Water",
    "Chicken Broth", "Beef Broth", "Vegetable Broth", "Stock",
    "Pickle", "Pickled Cucumber", "Kimchi", "Sauerkraut", "Capers",
    "Olives", "Green Olive", "Black Olive", "Kalamata Olive",
    "Sun-Dried Tomato", "Roasted Red Pepper",
    
    # Thai Specific
    "Galangal", "Kaffir Lime", "Bird's Eye Chili", "Shrimp Paste",
    "Tamarind", "Tamarind Paste", "Pandan Leaf",
    
    # Japanese Specific
    "Miso", "Wasabi", "Nori", "Seaweed", "Wakame", "Kombu",
    "Bonito Flakes", "Dashi", "Panko", "Matcha",
    
    # Indian Specific
    "Ghee", "Paneer", "Garam Masala", "Tandoori Masala", "Chaat Masala",
    "Asafoetida", "Curry Leaf", "Fenugreek Leaf",
    
    # Other International
    "Kimchi", "Gochugaru", "Perilla Leaf", "Harissa", "Preserved Lemon",
    "Ras el Hanout", "Shawarma Spice",
]

class IngredientSuggestionService:
    """Service for ingredient autocomplete suggestions"""
    
    def __init__(self):
        # Create lowercase mapping for case-insensitive search
        self.ingredients_lower = {ing.lower(): ing for ing in COMMON_INGREDIENTS}
        self.ingredients_sorted = sorted(COMMON_INGREDIENTS, key=str.lower)
    
    def get_suggestions(
        self,
        query: str,
        limit: int = 10,
        include_db_ingredients: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Get ingredient suggestions based on query
        
        Matching strategy:
        1. Search in predefined COMMON_INGREDIENTS list (500+ items)
        2. If include_db_ingredients=True, also search in recipe database
        3. Merge and deduplicate results
        
        Priority scoring:
        - Exact match: 1000 points
        - Prefix match: 900 points
        - Word boundary: 850 points
        - Substring match: 800 points
        
        Args:
            query: Partial ingredient name (e.g., "eg", "chic", "tom")
            limit: Maximum number of suggestions
            include_db_ingredients: Whether to include ingredients from database
        
        Returns:
            List of ingredient suggestions with match info
        """
        if not query or len(query.strip()) < 1:
            return []
        
        query_lower = query.strip().lower()
        matches = []
        seen_ingredients = set()
        
        # 1. Search in predefined common ingredients list (fast, in-memory)
        for ingredient_lower, ingredient_original in self.ingredients_lower.items():
            score = self._calculate_match_score(ingredient_lower, query_lower)
            
            if score > 0:
                matches.append({
                    "name": ingredient_original,
                    "name_lower": ingredient_lower,
                    "match_type": self._get_match_type(ingredient_lower, query_lower),
                    "score": score,
                    "length": len(ingredient_original),
                    "source": "common"
                })
                seen_ingredients.add(ingredient_lower)
        
        # 2. Search in database for additional ingredients from actual recipes
        if include_db_ingredients:
            try:
                db_ingredients = self._search_db_ingredients(query_lower, limit * 2)
                
                for ing in db_ingredients:
                    ing_lower = ing["name"].lower()
                    
                    # Skip if already found in common ingredients
                    if ing_lower in seen_ingredients:
                        continue
                    
                    score = self._calculate_match_score(ing_lower, query_lower)
                    
                    if score > 0:
                        matches.append({
                            "name": ing["name"],
                            "name_lower": ing_lower,
                            "match_type": self._get_match_type(ing_lower, query_lower),
                            "score": score - 50,  # Slightly lower priority than common ingredients
                            "length": len(ing["name"]),
                            "source": "database",
                            "usage_count": ing.get("usage_count", 0)
                        })
                        seen_ingredients.add(ing_lower)
            except Exception as e:
                # Silently fail if database is unavailable
                print(f"Database ingredient search failed: {e}")
        
        # Sort by score (desc), then by length (asc) for shorter names first
        matches.sort(key=lambda x: (-x["score"], x["length"]))
        
        # Format results
        suggestions = []
        for match in matches[:limit]:
            result = {
                "name": match["name"],
                "match_type": match["match_type"],
                "category": self._get_category(match["name"])
            }
            
            # Include usage count if from database
            if match.get("source") == "database" and match.get("usage_count"):
                result["usage_count"] = match["usage_count"]
            
            suggestions.append(result)
        
        return suggestions
    
    def _calculate_match_score(self, ingredient_lower: str, query_lower: str) -> int:
        """Calculate match score for ingredient"""
        # Exact match
        if ingredient_lower == query_lower:
            return 1000
        # Starts with query (prefix)
        elif ingredient_lower.startswith(query_lower):
            return 900
        # Word boundary match (for multi-word ingredients)
        elif any(word.startswith(query_lower) for word in ingredient_lower.split()):
            return 850
        # Contains query (substring)
        elif query_lower in ingredient_lower:
            return 800
        else:
            return 0
    
    def _get_match_type(self, ingredient_lower: str, query_lower: str) -> str:
        """Get match type description"""
        if ingredient_lower == query_lower:
            return "exact"
        elif ingredient_lower.startswith(query_lower):
            return "prefix"
        elif any(word.startswith(query_lower) for word in ingredient_lower.split()):
            return "word"
        else:
            return "substring"
    
    def _search_db_ingredients(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """
        Search ingredients from recipes database
        Extracts unique ingredients from mainIngredient and ingredients JSON
        """
        search_pattern = f"%{query}%"
        
        sql = """
            WITH ingredient_list AS (
                -- Get mainIngredient
                SELECT 
                    r."mainIngredient" as name,
                    COUNT(*) as usage_count
                FROM recipes r
                WHERE 
                    r.status = 'APPROVED'
                    AND LOWER(r."mainIngredient") LIKE LOWER(%s)
                    AND r."mainIngredient" IS NOT NULL
                GROUP BY r."mainIngredient"
                
                UNION
                
                -- Get ingredients from JSON array
                SELECT 
                    ingredient->>'name' as name,
                    COUNT(*) as usage_count
                FROM recipes r,
                     jsonb_array_elements(r.ingredients) AS ingredient
                WHERE 
                    r.status = 'APPROVED'
                    AND LOWER(ingredient->>'name') LIKE LOWER(%s)
                    AND ingredient->>'name' IS NOT NULL
                GROUP BY ingredient->>'name'
            )
            SELECT 
                name,
                SUM(usage_count) as usage_count
            FROM ingredient_list
            GROUP BY name
            ORDER BY usage_count DESC, name ASC
            LIMIT %s
        """
        
        try:
            with get_db_connection() as conn:
                with get_db_cursor(conn) as cur:
                    cur.execute(sql, [search_pattern, search_pattern, limit])
                    results = cur.fetchall()
                    return [dict(row) for row in results]
        except Exception as e:
            print(f"Database query failed: {e}")
            return []
    
    def _get_category(self, ingredient: str) -> str:
        """Categorize ingredient (simple heuristic)"""
        ingredient_lower = ingredient.lower()
        
        # Proteins
        if any(word in ingredient_lower for word in ["chicken", "beef", "pork", "fish", "shrimp", 
                                                       "salmon", "tuna", "egg", "turkey", "duck", 
                                                       "lamb", "bacon", "sausage", "tofu", "tempeh",
                                                       "crab", "lobster", "squid", "octopus"]):
            return "protein"
        
        # Vegetables
        if any(word in ingredient_lower for word in ["tomato", "onion", "garlic", "carrot", "potato",
                                                       "broccoli", "spinach", "lettuce", "cabbage",
                                                       "cucumber", "pepper", "mushroom", "zucchini",
                                                       "eggplant", "celery", "cauliflower", "kale",
                                                       "bean", "corn", "pumpkin", "radish", "ginger"]):
            return "vegetable"
        
        # Fruits
        if any(word in ingredient_lower for word in ["apple", "banana", "orange", "lemon", "lime",
                                                       "mango", "pineapple", "strawberry", "blueberry",
                                                       "avocado", "coconut", "grape", "watermelon"]):
            return "fruit"
        
        # Dairy
        if any(word in ingredient_lower for word in ["milk", "cheese", "butter", "cream", "yogurt"]):
            return "dairy"
        
        # Grains
        if any(word in ingredient_lower for word in ["rice", "pasta", "noodle", "bread", "flour",
                                                       "quinoa", "oats", "spaghetti", "macaroni"]):
            return "grain"
        
        # Herbs & Spices
        if any(word in ingredient_lower for word in ["basil", "oregano", "thyme", "rosemary", "parsley",
                                                       "cilantro", "mint", "cumin", "paprika", "turmeric",
                                                       "cinnamon", "pepper", "salt", "curry", "chili powder"]):
            return "herb_spice"
        
        # Condiments
        if any(word in ingredient_lower for word in ["sauce", "oil", "vinegar", "honey", "sugar",
                                                       "mayonnaise", "ketchup", "mustard"]):
            return "condiment"
        
        return "other"

# Global instance
ingredient_service = IngredientSuggestionService()
