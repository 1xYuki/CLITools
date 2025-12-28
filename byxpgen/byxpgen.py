import sys
import secrets
import string
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from math import log2

DEFAULT_WORDLIST = [
    'acid', 'acorn', 'acre', 'acts', 'afar', 'affix', 'aged', 'agent', 'agile', 'aging',
    'agony', 'ahead', 'aide', 'aids', 'aim', 'ajar', 'alarm', 'alias', 'alibi', 'alien',
    'alike', 'alive', 'aloe', 'aloft', 'aloha', 'alone', 'amend', 'amino', 'ample', 'amuse',
    'angel', 'anger', 'angle', 'ankle', 'apple', 'april', 'apron', 'aqua', 'area', 'arena',
    'argue', 'arise', 'armed', 'armor', 'army', 'aroma', 'array', 'arson', 'art', 'ashen',
    'ashes', 'atlas', 'atom', 'attic', 'audio', 'avert', 'avoid', 'awake', 'award', 'awoke',
    'axis', 'bacon', 'badge', 'bagel', 'baggy', 'baked', 'baker', 'balmy', 'banjo', 'barge',
    'barn', 'bash', 'basil', 'bask', 'batch', 'bath', 'baton', 'bats', 'blade', 'blank',
    'blast', 'blaze', 'bleak', 'blend', 'bless', 'blimp', 'blink', 'bloat', 'blob', 'blog',
    'blot', 'blunt', 'blurt', 'blush', 'boast', 'boat', 'body', 'boil', 'bok', 'bolt',
    'boned', 'boney', 'bonus', 'bony', 'book', 'booth', 'boots', 'boss', 'botch', 'both',
    'boxer', 'breed', 'bribe', 'brick', 'bride', 'brim', 'bring', 'brink', 'brisk', 'broad',
    'broil', 'broke', 'brook', 'broom', 'brush', 'buck', 'bud', 'buggy', 'bulge', 'bulk',
    'bully', 'bunch', 'bunny', 'bunt', 'bush', 'bust', 'busy', 'buzz', 'cable', 'cache',
    'cadet', 'cage', 'cake', 'calm', 'cameo', 'canal', 'candy', 'cane', 'canon', 'cape',
    'card', 'cargo', 'carol', 'carry', 'carve', 'case', 'cash', 'cause', 'cedar', 'chain',
    'chair', 'chant', 'chaos', 'charm', 'chase', 'cheek', 'cheer', 'chef', 'chess', 'chest',
    'chew', 'chief', 'chili', 'chill', 'chip', 'chomp', 'chop', 'chow', 'chuck', 'chump',
    'chunk', 'churn', 'chute', 'cider', 'cinch', 'city', 'civic', 'civil', 'clad', 'claim',
    'clamp', 'clap', 'clash', 'clasp', 'class', 'claw', 'clay', 'clean', 'clear', 'cleat',
    'cleft', 'clerk', 'click', 'cling', 'clink', 'clip', 'cloak', 'clock', 'clone', 'cloth',
    'cloud', 'clump', 'coach', 'coast', 'coat', 'cod', 'coil', 'coke', 'cola', 'cold',
    'colt', 'coma', 'come', 'comic', 'comma', 'cone', 'cope', 'copy', 'coral', 'cork',
    'cost', 'cot', 'couch', 'cough', 'cover', 'cozy', 'craft', 'cramp', 'crane', 'crank',
    'crate', 'crave', 'crawl', 'crazy', 'creme', 'crepe', 'crept', 'crib', 'cried', 'crisp',
    'crook', 'crop', 'cross', 'crowd', 'crown', 'crumb', 'crush', 'crust', 'cub', 'cult',
    'cupid', 'cure', 'curl', 'curry', 'curse', 'curve', 'curvy', 'cushy', 'cut', 'cycle',
    'dab', 'dad', 'daily', 'dairy', 'daisy', 'dance', 'dandy', 'darn', 'dart', 'dash',
    'data', 'date', 'dawn', 'deaf', 'deal', 'dean', 'debit', 'debt', 'debug', 'decaf',
    'decal', 'decay', 'deck', 'decor', 'decoy', 'deed', 'delay', 'denim', 'dense', 'dent',
    'depth', 'derby', 'desk', 'dial', 'diary', 'dice', 'dig', 'dill', 'dime', 'dimly',
    'diner', 'dingy', 'disco', 'dish', 'disk', 'ditch', 'ditzy', 'dizzy', 'dock', 'dodge',
    'doing', 'doll', 'dome', 'donor', 'donut', 'dose', 'dot', 'dove', 'down', 'dowry',
    'doze', 'drab', 'drama', 'drank', 'draw', 'dress', 'dried', 'drift', 'drill', 'drive',
    'drone', 'droop', 'drove', 'drown', 'drum', 'dry', 'duck', 'duct', 'dude', 'dug',
    'duke', 'duo', 'dusk', 'dust', 'duty', 'dwarf', 'dwell', 'eagle', 'early', 'earth',
    'easel', 'east', 'eaten', 'eats', 'ebay', 'ebony', 'ebook', 'echo', 'edge', 'eel',
    'eject', 'elbow', 'elder', 'elf', 'elk', 'elm', 'elope', 'elude', 'elves', 'email',
    'emit', 'empty', 'emu', 'enter', 'entry', 'envoy', 'equal', 'erase', 'error', 'erupt',
    'essay', 'etch', 'evade', 'even', 'evict', 'evil', 'evoke', 'exact', 'exit', 'fable',
    'faced', 'fact', 'fade', 'fall', 'false', 'fancy', 'fang', 'fax', 'feast', 'feed',
    'femur', 'fence', 'fend', 'ferry', 'fetal', 'fetch', 'fever', 'fiber', 'fifth', 'fifty',
    'film', 'filth', 'final', 'finch', 'fit', 'five', 'flag', 'flaky', 'flame', 'flap',
    'flask', 'fled', 'flick', 'fling', 'flint', 'flip', 'flirt', 'float', 'flock', 'flop',
    'floss', 'flyer', 'foam', 'foe', 'fog', 'foil', 'folic', 'folk', 'food', 'fool',
    'found', 'fox', 'foyer', 'frail', 'frame', 'fray', 'fresh', 'fried', 'frill', 'frisk',
    'from', 'front', 'frost', 'froth', 'frown', 'froze', 'fruit', 'gag', 'gains', 'gala',
    'game', 'gap', 'gas', 'gave', 'gear', 'gecko', 'geek', 'gem', 'genre', 'gift',
    'gig', 'gills', 'given', 'giver', 'glad', 'glass', 'glide', 'gloss', 'glove', 'glow',
    'glue', 'goal', 'going', 'golf', 'gong', 'good', 'gooey', 'goofy', 'gore', 'gown',
    'grab', 'grain', 'grant', 'grape', 'graph', 'grasp', 'grass', 'grave', 'gravy', 'gray',
    'green', 'greet', 'grew', 'grid', 'grief', 'grill', 'grip', 'grit', 'groom', 'grope',
    'growl', 'grub', 'grunt', 'guide', 'gulf', 'gulp', 'gummy', 'guru', 'gush', 'gut',
    'guy', 'habit', 'half', 'halo', 'halt', 'happy', 'harm', 'hash', 'hasty', 'hatch',
    'hate', 'haven', 'hazel', 'hazy', 'heap', 'heat', 'heave', 'hedge', 'hefty', 'help',
    'herbs', 'hers', 'hub', 'hug', 'hula', 'hull', 'human', 'humid', 'hump', 'hung',
    'hunk', 'hunt', 'hurry', 'hurt', 'hush', 'hut', 'ice', 'icing', 'icon', 'icy',
    'igloo', 'image', 'ion', 'iron', 'islam', 'issue', 'item', 'ivory', 'ivy', 'jab',
    'jam', 'jaws', 'jazz', 'jeep', 'jelly', 'jet', 'jiffy', 'job', 'jog', 'jolly',
    'jolt', 'jot', 'joy', 'judge', 'juice', 'juicy', 'july', 'jumbo', 'jump', 'junky',
    'juror', 'jury', 'keep', 'keg', 'kept', 'kick', 'kilt', 'king', 'kite', 'kitty',
    'kiwi', 'knee', 'knelt', 'koala', 'kung', 'ladle', 'lady', 'lair', 'lake', 'lance',
    'land', 'lapel', 'large', 'lash', 'lasso', 'last', 'latch', 'late', 'lazy', 'left',
    'legal', 'lemon', 'lend', 'lens', 'lent', 'level', 'lever', 'lid', 'life', 'lift',
    'lilac', 'lily', 'limb', 'limes', 'line', 'lint', 'lion', 'lip', 'list', 'lived',
    'liver', 'lunar', 'lunch', 'lung', 'lurch', 'lure', 'lurk', 'lying', 'lyric', 'mace',
    'maker', 'malt', 'mama', 'mango', 'manor', 'many', 'map', 'march', 'mardi', 'marry',
    'mash', 'match', 'mate', 'math', 'moan', 'mocha', 'moist', 'mold', 'mom', 'moody',
    'mop', 'morse', 'most', 'motor', 'motto', 'mount', 'mouse', 'mousy', 'mouth', 'move',
    'movie', 'mower', 'mud', 'mug', 'mulch', 'mule', 'mull', 'mumbo', 'mummy', 'mural',
    'muse', 'music', 'musky', 'mute', 'nacho', 'nag', 'nail', 'name', 'nanny', 'nap',
    'navy', 'near', 'neat', 'neon', 'nerd', 'nest', 'net', 'next', 'niece', 'ninth',
    'nutty', 'oak', 'oasis', 'oat', 'ocean', 'oil', 'old', 'olive', 'omen', 'onion',
    'only', 'ooze', 'opal', 'open', 'opera', 'opt', 'otter', 'ouch', 'ounce', 'outer',
    'oval', 'oven', 'owl', 'ozone', 'pace', 'pagan', 'pager', 'palm', 'panda', 'panic',
    'pants', 'panty', 'paper', 'park', 'party', 'pasta', 'patch', 'path', 'patio', 'payer',
    'pecan', 'penny', 'pep', 'perch', 'perky', 'perm', 'pest', 'petal', 'petri', 'petty',
    'photo', 'plank', 'plant', 'plaza', 'plead', 'plot', 'plow', 'pluck', 'plug', 'plus',
    'poach', 'pod', 'poem', 'poet', 'pogo', 'point', 'poise', 'poker', 'polar', 'polio',
    'polka', 'polo', 'pond', 'pony', 'poppy', 'pork', 'poser', 'pouch', 'pound', 'pout',
    'power', 'prank', 'press', 'print', 'prior', 'prism', 'prize', 'probe', 'prong', 'proof',
    'props', 'prude', 'prune', 'pry', 'pug', 'pull', 'pulp', 'pulse', 'puma', 'punch',
    'punk', 'pupil', 'puppy', 'purr', 'purse', 'push', 'putt', 'quack', 'quake', 'query',
    'quiet', 'quill', 'quilt', 'quit', 'quota', 'quote', 'rabid', 'race', 'rack', 'radar',
    'radio', 'raft', 'rage', 'raid', 'rail', 'rake', 'rally', 'ramp', 'ranch', 'range',
    'rank', 'rant', 'rash', 'raven', 'reach', 'react', 'ream', 'rebel', 'recap', 'relax',
    'relay', 'relic', 'remix', 'repay', 'repel', 'reply', 'rerun', 'reset', 'rhyme', 'rice',
    'rich', 'ride', 'rigid', 'rigor', 'rinse', 'riot', 'ripen', 'rise', 'risk', 'ritzy',
    'rival', 'river', 'roast', 'robe', 'robin', 'rock', 'rogue', 'roman', 'romp', 'rope',
    'rover', 'royal', 'ruby', 'rug', 'ruin', 'rule', 'runny', 'rush', 'rust', 'rut',
    'sadly', 'sage', 'said', 'saint', 'salad', 'salon', 'salsa', 'salt', 'same', 'sandy',
    'santa', 'satin', 'sauna', 'saved', 'savor', 'sax', 'say', 'scale', 'scam', 'scan',
    'scare', 'scarf', 'scary', 'scoff', 'scold', 'scoop', 'scoot', 'scope', 'score', 'scorn',
    'scout', 'scowl', 'scrap', 'scrub', 'scuba', 'scuff', 'sect', 'sedan', 'self', 'send',
    'sepia', 'serve', 'set', 'seven', 'shack', 'shade', 'shady', 'shaft', 'shaky', 'sham',
    'shape', 'share', 'sharp', 'shed', 'sheep', 'sheet', 'shelf', 'shell', 'shine', 'shiny',
    'ship', 'shirt', 'shock', 'shop', 'shore', 'shout', 'shove', 'shown', 'showy', 'shred',
    'shrug', 'shun', 'shush', 'shut', 'shy', 'sift', 'silk', 'silly', 'silo', 'sip',
    'siren', 'sixth', 'size', 'skate', 'skew', 'skid', 'skier', 'skies', 'skip', 'skirt',
    'skit', 'sky', 'slab', 'slack', 'slain', 'slam', 'slang', 'slash', 'slate', 'slaw',
    'sled', 'sleek', 'sleep', 'sleet', 'slept', 'slice', 'slick', 'slimy', 'sling', 'slip',
    'slit', 'slob', 'slot', 'slug', 'slum', 'slurp', 'slush', 'small', 'smash', 'smell',
    'smile', 'smirk', 'smog', 'snack', 'snap', 'snare', 'snarl', 'sneak', 'sneer', 'sniff',
    'snore', 'snort', 'snout', 'snowy', 'snub', 'snuff', 'speak', 'speed', 'spend', 'spent',
    'spew', 'spied', 'spill', 'spiny', 'spoil', 'spoke', 'spoof', 'spool', 'spoon', 'sport',
    'spot', 'spout', 'spray', 'spree', 'spur', 'squad', 'squat', 'squid', 'stack', 'staff',
    'stage', 'stain', 'stall', 'stamp', 'stand', 'stank', 'stark', 'start', 'stash', 'state',
    'stays', 'steam', 'steep', 'stem', 'step', 'stew', 'stick', 'sting', 'stir', 'stock',
    'stole', 'stomp', 'stony', 'stood', 'stool', 'stoop', 'stop', 'storm', 'stout', 'stove',
    'straw', 'stray', 'strut', 'stuck', 'stud', 'stuff', 'stump', 'stung', 'stunt', 'suds',
    'sugar', 'sulk', 'surf', 'sushi', 'swab', 'swan', 'swarm', 'sway', 'swear', 'sweat',
    'sweep', 'swell', 'swept', 'swim', 'swing', 'swipe', 'swirl', 'swoop', 'swore', 'syrup',
    'tacky', 'taco', 'tag', 'take', 'tall', 'talon', 'tamer', 'tank', 'taper', 'taps',
    'tarot', 'tart', 'task', 'taste', 'tasty', 'taunt', 'thank', 'thaw', 'theft', 'theme',
    'thigh', 'thing', 'think', 'thong', 'thorn', 'those', 'throb', 'thud', 'thumb', 'thump',
    'thus', 'tiara', 'tidal', 'tidy', 'tiger', 'tile', 'tilt', 'tint', 'tiny', 'trace',
    'track', 'trade', 'train', 'trait', 'trap', 'trash', 'tray', 'treat', 'tree', 'trek',
    'trend', 'trial', 'tribe', 'trick', 'trio', 'trout', 'truce', 'truck', 'trump', 'trunk',
    'try', 'tug', 'tulip', 'tummy', 'turf', 'tusk', 'tutor', 'tutu', 'tux', 'tweak',
    'tweet', 'twice', 'twine', 'twins', 'twirl', 'twist', 'uncle', 'uncut', 'undo', 'unify',
    'union', 'unit', 'untie', 'upon', 'upper', 'urban', 'used', 'user', 'usher', 'utter',
    'value', 'vapor', 'vegan', 'venue', 'verse', 'vest', 'veto', 'vice', 'video', 'view',
    'viral', 'virus', 'visa', 'visor', 'vixen', 'vocal', 'voice', 'void', 'volt', 'voter',
    'vowel', 'wad', 'wafer', 'wager', 'wages', 'wagon', 'wake', 'walk', 'wand', 'wasp',
    'watch', 'water', 'wavy', 'wheat', 'whiff', 'whole', 'whoop', 'wick', 'widen', 'widow',
    'width', 'wife', 'wifi', 'wilt', 'wimp', 'wind', 'wing', 'wink', 'wipe', 'wired',
    'wiry', 'wise', 'wish', 'wispy', 'wok', 'wolf', 'womb', 'wool', 'woozy', 'word',
    'work', 'worry', 'wound', 'woven', 'wrath', 'wreck', 'wrist', 'xerox', 'yahoo', 'yam',
    'yard', 'year', 'yeast', 'yelp', 'yield', 'yo-yo', 'yodel', 'yoga', 'yoyo', 'yummy',
    'zebra', 'zero', 'zesty', 'zippy', 'zone', 'zoom',
]

def get_args():
    parser = ArgumentParser(
        description='CLI Tool for generating secure passwords and passphrases',
        epilog='Developed for Yuki, by Yuki, Always and Forever',
        formatter_class=RawDescriptionHelpFormatter
    )
    group =(
        parser.add_mutually_exclusive_group()
    )
    parser.usage =(
        'Basic Usage: -l (Length), -p (Passphrase), -c (Count), -f (File), -W (Wordlist), --only/--force (Character Control)'
    )
    parser.add_argument(
        '-l', '--length', type=int, default=12,
        help='Password length (default: 12 characters)'
        )
    parser.add_argument(
        '-c', '--count', type=int, default=1,
        help='Number of passwords to generate (default: 1)'
        )
    parser.add_argument(
        '-p', '--passphrase', action='store_true',
        help='Generate passphrase instead of password'
        )
    parser.add_argument(
        '-w', '--words', type=int, default=4,
        help='Number of words in passphrase (default: 4)'
        )
    parser.add_argument(
        '-s', '--separator', type=str, default='-',
        help='Passphrase word separator (default: -)'
        )
    parser.add_argument(
        '-W', '--wordlist', type=str, metavar='FILE',
        help='Use custom wordlist file for passphrases (one word per line or EFF format)'
        )
    parser.add_argument(
        '--no-upper', action='store_true',
        help='Exclude uppercase letters'
        )
    parser.add_argument(
        '--no-lower', action='store_true',
        help='Exclude lowercase letters'
        )
    parser.add_argument(
        '--no-digits', action='store_true',
        help='Exclude digits'
        )
    parser.add_argument(
        '--no-symbols', action='store_true',
        help='Exclude symbols'
        )
    group.add_argument(
        '-o', '--only', type=str, 
        choices=['alpha', 'alphanumeric', 'numeric', 'symbols'],
        help='Use only specific character types'
        )
    group.add_argument(
        '-F', '--force-chars', type=str,
        help='Force use of specific characters (e.g., "abc123!@#")'
        )
    parser.add_argument(
        '--min-upper', type=int, default=0,
        help='Minimum number of uppercase letters'
        )
    parser.add_argument(
        '--min-lower', type=int, default=0,
        help='Minimum number of lowercase letters'
        )
    parser.add_argument(
        '--min-digits', type=int, default=0,
        help='Minimum number of digits'
        )
    parser.add_argument(
        '--min-symbols', type=int, default=0,
        help='Minimum number of symbols'
        )
    parser.add_argument(
        '-f', '--file', type=str, metavar='FILE',
        help='Save generated passwords to file'
        )
    group.add_argument(
        '-q', '--quiet', action='store_true',
        help='Quiet mode, only output passwords'
        )
    group.add_argument(
        '-v', '--verbose', action='count', default=0,
        help='Add Verbosity (-v for verbose, -vv for full verbose)'
        )
    return parser.parse_args()


def load_wordlist(filepath): # '-W', '--wordlist', Load custom wordlist from file
    try:
        words = []
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                parts = line.split()
                if len(parts) >= 2 and parts[0].isdigit():
                    words.append(parts[1])
                else:
                    words.append(parts[0])
        
        if not words:
            print(f"Error: No words found in wordlist file: {filepath}")
            sys.exit(1)
        
        return words
    
    except IOError as e:
        print(f"Error reading wordlist file: {e}")
        sys.exit(1)


def get_character_set(args): # Build character set based on arguments
    if args.force_chars:
        return args.force_chars
    
    if args.only:
        if args.only == 'alpha':
            return string.ascii_letters
        elif args.only == 'alphanumeric':
            return string.ascii_letters + string.digits
        elif args.only == 'numeric':
            return string.digits
        elif args.only == 'symbols':
            return string.punctuation
    
    charset = ''
    
    if not args.no_upper:
        charset += string.ascii_uppercase
    if not args.no_lower:
        charset += string.ascii_lowercase
    if not args.no_digits:
        charset += string.digits
    if not args.no_symbols:
        charset += string.punctuation
    
    if not charset:
        print("Error: No character types selected. At least one character type must be enabled.")
        sys.exit(1)
    
    return charset


def calculate_entropy(length, charset_size): # '-v', '-vv', Calculate password entropy in bits
    return length * log2(charset_size) if charset_size > 0 else 0


def get_strength_rating(entropy): # '-v', '-vv', Determine password strength based on entropy
    if entropy < 28:
        return "Very Weak"
    elif entropy < 36:
        return "Weak"
    elif entropy < 60:
        return "Reasonable"
    elif entropy < 128:
        return "Strong"
    else:
        return "Very Strong"


def meets_requirements(password, args): # Check if password meets minimum requirements
    if args.min_upper > 0:
        if sum(1 for c in password if c in string.ascii_uppercase) < args.min_upper:
            return False
    if args.min_lower > 0:
        if sum(1 for c in password if c in string.ascii_lowercase) < args.min_lower:
            return False
    if args.min_digits > 0:
        if sum(1 for c in password if c in string.digits) < args.min_digits:
            return False
    if args.min_symbols > 0:
        if sum(1 for c in password if c in string.punctuation) < args.min_symbols:
            return False
    return True


def generate_password(length, charset, args): # Generate cryptographically secure password
    max_attempts = 10000
    
    for _ in range(max_attempts):
        password = ''.join(secrets.choice(charset) for _ in range(length))
        if meets_requirements(password, args):
            return password
    
    print("Error: Could not generate password meeting minimum requirements.")
    print("Try reducing minimum requirements or increasing password length.")
    sys.exit(1)


def generate_passphrase(words, separator, wordlist): # '-p', '--passphrase', Generate memorable passphrase
    selected_words = [secrets.choice(wordlist) for _ in range(words)]
    return separator.join(selected_words)


def read_stdin_params(): # Read generation parameters from stdin
    if sys.stdin.isatty():
        return None
    
    stdin_data = sys.stdin.read().strip()
    if not stdin_data:
        return None
    
    params = {}
    for line in stdin_data.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            params[key.strip().lower()] = value.strip()
    
    return params


def main():
    args = get_args()
    
    stdin_params = read_stdin_params()
    if stdin_params:
        if 'length' in stdin_params:
            args.length = int(stdin_params['length'])
        if 'count' in stdin_params:
            args.count = int(stdin_params['count'])
    
    passwords = []
    
    if args.passphrase: # '-p', '--passphrase', Generate passphrase
        wordlist =(
            load_wordlist(args.wordlist) if args.wordlist else DEFAULT_WORDLIST # EFF Short Wordlist is the default.
        )
        
        if not wordlist:
            print("Error: No wordlist available. Please provide a wordlist with -W or add words to DEFAULT_WORDLIST.")
            sys.exit(1)
        
        for _ in range(args.count):
            passphrase = generate_passphrase(args.words, args.separator, wordlist)
            passwords.append(passphrase)
        
        charset_size = len(wordlist)
        avg_length = sum(len(p) for p in passwords) / len(passwords)
    
    else: # Generate standard password
        charset = get_character_set(args)
        
        total_min = args.min_upper + args.min_lower + args.min_digits + args.min_symbols
        if total_min > args.length:
            print(f"Error: Minimum requirements ({total_min}) exceed password length ({args.length})")
            sys.exit(1)
        
        for _ in range(args.count):
            password = generate_password(args.length, charset, args)
            passwords.append(password)
        
        charset_size = len(set(charset))
        avg_length = sum(len(p) for p in passwords) / len(passwords)
    
    if args.quiet: # '-q', '--quiet', Outputs passwords quietly
        for pwd in passwords:
            print(pwd)
    
    else: # Default and verbose output
        if args.count == 1:
            print(f"Password: {passwords[0]}")
        else:
            print(f"Passwords: {', '.join(passwords)}")
        
        if args.verbose >= 1: # '-v', Verbosity Lvl 1
            if args.passphrase:
                entropy = args.words * log2(charset_size)
            else:
                entropy = calculate_entropy(int(avg_length), charset_size)
            
            print(f"\nGenerated: {args.count} password{'s' if args.count > 1 else ''}")
            print(f"Average length: {avg_length:.1f} characters")
            print(f"Entropy: {entropy:.2f} bits")
            print(f"Strength: {get_strength_rating(entropy)}")
        
        if args.verbose >= 2: # '-vv', Verbosity Lvl 2
            print("-" * 50)
            
            if args.passphrase:
                print(f"Wordlist size: {charset_size} words")
                if args.wordlist:
                    print(f"Custom wordlist: {args.wordlist}")
                else:
                    print(f"Using default EFF wordlist")
                print(f"Words per passphrase: {args.words}")
                print(f"Separator: '{args.separator}'")
            else:
                print(f"Character set size: {charset_size}")
                sample_pwd = passwords[0]
                print(f"\nCharacter composition (sample):")
                print(f"  Uppercase: {sum(1 for c in sample_pwd if c in string.ascii_uppercase)}")
                print(f"  Lowercase: {sum(1 for c in sample_pwd if c in string.ascii_lowercase)}")
                print(f"  Digits: {sum(1 for c in sample_pwd if c in string.digits)}")
                print(f"  Symbols: {sum(1 for c in sample_pwd if c in string.punctuation)}")
                print(f"\nCharacter set preview: {charset[:50]}{'...' if len(charset) > 50 else ''}")
    
    if args.file: # '-f', '--file', Save passwords to file
        try:
            with open(args.file, 'w') as f:
                for pwd in passwords:
                    f.write(pwd + '\n')
            if not args.quiet:
                print(f"\nPasswords saved to: {args.file}")
        except IOError as e:
            print(f"\nError saving to file: {e}")
            sys.exit(1)


if __name__ == '__main__':
    main()