import sys
import secrets
import string
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from math import log2

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
        'Basic Usage: -l (Length), -p (Passphrase), -c (Count), -f (File), --only/--force (Character Control)'
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
                
                # Handle EFF format (number + tab/spaces + word) or plain wordlist, written in because the EFF wordlist was a pain.
                parts = line.split()
                if len(parts) >= 2 and parts[0].isdigit():
                    words.append(parts[1])  # EFF format
                else:
                    words.append(parts[0])  # Plain wordlist (one word per line)
        
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


def calculate_entropy(length, charset_size): # '-v', '-vv', '--verbose' Calculate password entropy in bits
    return length * log2(charset_size) if charset_size > 0 else 0


def get_strength_rating(entropy): # '-v', '-vv', '--verbose' Determine password strength based on entropy
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


def generate_password(length, charset, args): # Generate Password
    max_attempts = 10000
    
    for _ in range(max_attempts):
        password = ''.join(secrets.choice(charset) for _ in range(length))
        if meets_requirements(password, args):
            return password
    
    print("Error: Could not generate password meeting minimum requirements.")
    print("Try reducing minimum requirements or increasing password length.")
    sys.exit(1)


def generate_passphrase(words, separator): # Generate memorable passphrase
    wordlist = [
        'correct', 'horse', 'battery', 'staple', 'python', 'secure', 'random',
        'crypto', 'cipher', 'encode', 'decode', 'algorithm', 'network', 'system',
        'digital', 'binary', 'quantum', 'neural', 'vector', 'matrix', 'token',
        'prime', 'hash', 'block', 'chain', 'vault', 'shield', 'guardian', 'keeper',
        'fortress', 'castle', 'dragon', 'phoenix', 'thunder', 'lightning', 'storm',
        'ocean', 'mountain', 'forest', 'river', 'cosmic', 'stellar', 'solar',
        'lunar', 'galaxy', 'nebula', 'comet', 'meteor', 'planet', 'orbit',
        'gravity', 'energy', 'power', 'force', 'velocity', 'momentum', 'spectrum',
        'wavelength', 'frequency', 'amplitude', 'resonance', 'harmony', 'melody',
        'rhythm', 'tempo', 'pulse', 'signal', 'data', 'stream', 'flow', 'current'
    ]
    
    selected_words = [secrets.choice(wordlist) for _ in range(words)]
    return separator.join(selected_words)


def read_stdin_params(): # stdin parameters
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
    charset = None
    
    if args.passphrase: # '-p', '--passphrase', Generate passphrase
        for _ in range(args.count):
            passphrase = generate_passphrase(args.words, args.separator)
            passwords.append(passphrase)
        charset = string.ascii_lowercase
    
    else: # Generate standard password
        charset = get_character_set(args)
        
        total_min = args.min_upper + args.min_lower + args.min_digits + args.min_symbols
        if total_min > args.length:
            print(f"Error: Minimum requirements ({total_min}) exceed password length ({args.length})")
            sys.exit(1)
        
        for _ in range(args.count):
            password = generate_password(args.length, charset, args)
            passwords.append(password)
    
    if args.quiet: # '-q', '--quiet', Outputs passwords quietly
        for pwd in passwords:
            print(pwd)
    
    else: # Default and verbose output
        if args.count == 1:
            print(f"Password: {passwords[0]}")
        else:
            print(f"Passwords: {', '.join(passwords)}")
        
        if args.verbose >= 1: # '-v', Verbosity Lvl 1
            avg_length = sum(len(p) for p in passwords) / len(passwords)
            charset_size = len(set(charset))
            entropy = calculate_entropy(int(avg_length), charset_size)
            
            print(f"\nGenerated: {args.count} password{'s' if args.count > 1 else ''}")
            print(f"Average length: {avg_length:.1f} characters")
            print(f"Entropy: {entropy:.2f} bits")
            print(f"Strength: {get_strength_rating(entropy)}")
        
        if args.verbose >= 2: # '-vv', Verbosity Lvl 2
            print("-" * 50)
            print(f"Character set size: {len(set(charset))}")
            print("Entropy is estimated; passphrase strength depends on wordlist size")
            
            if not args.passphrase:
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