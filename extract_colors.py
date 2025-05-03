from PIL import Image
import json

def get_colors(image_path, num_colors=5):
    """Extracts dominant colors from an image."""
    try:
        img = Image.open(image_path)
        img = img.convert("RGB")
        # Reduce image size for faster processing
        img.thumbnail((100, 100))
        
        # Get colors using Pillow's built-in method
        result = img.getcolors(img.size[0] * img.size[1])
        if not result:
            print("Could not get colors from image.")
            return None
            
        # Sort by count (most frequent first)
        sorted_colors = sorted(result, key=lambda x: x[0], reverse=True)
        
        # Extract the RGB values
        dominant_colors_rgb = [color[1] for color in sorted_colors[:num_colors]]
        
        # Convert RGB to HEX
        dominant_colors_hex = [f"#{r:02x}{g:02x}{b:02x}" for r, g, b in dominant_colors_rgb]
        
        print(f"Extracted dominant colors (HEX): {dominant_colors_hex}")
        return dominant_colors_hex
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

def find_gold_grey(colors):
    """Identifies likely gold/beige and grey colors from a list of hex codes."""
    if not colors:
        return None, None
        
    gold = None
    grey = None
    
    # Simple heuristics to find gold/beige and grey
    # Gold/Beige: Often has R > G > B, with R and G relatively close
    # Grey: R, G, B values are close to each other
    
    for hex_color in colors:
        if hex_color == "#ffffff" or hex_color == "#000000": # Skip pure white/black
             continue
             
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        
        # Check for grey (values close)
        if abs(r - g) < 20 and abs(g - b) < 20 and abs(r - b) < 20 and not grey:
            # Avoid white/very light grey if possible, prefer darker grey
            if r > 100 and r < 220: # Check if it's not too light or dark
                 grey = hex_color
                 print(f"Identified Grey: {grey}")
                 continue # Found grey, move to next color
                 
        # Check for gold/beige (R > G > B-ish, not grey)
        if r > g and g > b and r > 150 and g > 100 and b < 150 and not gold:
             # Check if it's not too close to grey
             if not (abs(r - g) < 20 and abs(g - b) < 20):
                 gold = hex_color
                 print(f"Identified Gold/Beige: {gold}")
                 continue # Found gold, move to next color
                 
    # Fallback if specific heuristics fail
    if not grey and len(colors) > 1:
        # Assume the second most dominant non-white color might be grey
        for c in colors:
             if c != "#ffffff":
                 r = int(c[1:3], 16)
                 g = int(c[3:5], 16)
                 b = int(c[5:7], 16)
                 if abs(r - g) < 30 and abs(g - b) < 30: # Looser grey check
                     grey = c
                     print(f"Fallback Grey: {grey}")
                     break
                     
    if not gold and len(colors) > 0:
         # Assume the most dominant non-white/non-grey color might be gold/beige
         for c in colors:
             if c != "#ffffff" and c != grey:
                 gold = c
                 print(f"Fallback Gold/Beige: {gold}")
                 break
                 
    return gold, grey

if __name__ == "__main__":
    image_file = "/home/ubuntu/upload/BE Capital logo.jpg"
    output_file = "/home/ubuntu/color_palette.json"
    
    extracted_colors = get_colors(image_file, num_colors=10) # Get more colors initially
    
    gold_color, grey_color = find_gold_grey(extracted_colors)
    
    palette = {
        "gold": gold_color if gold_color else "#bfa78a", # Default fallback gold
        "grey": grey_color if grey_color else "#a0a0a0"  # Default fallback grey
    }
    
    with open(output_file, 'w') as f:
        json.dump(palette, f, indent=4)
        
    print(f"\nFinal Palette: Gold - {palette['gold']}, Grey - {palette['grey']}")
    print(f"Palette saved to {output_file}")

