import sys
import secrets
import string
from argparse import ArgumentParser, RawDescriptionHelpFormatter

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
        'Basic Usage: -l (Length), -p (Passphrase), -c (Count), --only/--force (Character Control)'
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
        '-f', '--force', type=str,
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
        '-v', '--verbose', action='store_true',
        help='Show entropy and character set information'
        )
    parser.add_argument(
        '--save', type=str, metavar='FILE',
        help='Save generated passwords to file'
        )
    return parser.parse_args()


def get_character_set(args): # Build character set based on arguments
    if args.force: # '-f', '--force', Use only specified characters
        return args.force
    
    if args.only: # '-o', '--only', Use specific character type
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


def calculate_entropy(length, charset_size): # Calculate password entropy in bits
    import math
    if charset_size == 0:
        return 0
    return length * math.log2(charset_size)


def meets_requirements(password, args, charset): # Check if password meets minimum requirements
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
        if meets_requirements(password, args, charset):
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


def display_info(password, args, charset): # '-v', '--verbose', Display password information
    print(f"\nPassword: {password}")
    print("-" * 50)
    print(f"Length: {len(password)} characters")
    print(f"Character set size: {len(set(charset))}")
    
    entropy = calculate_entropy(len(password), len(set(charset)))
    print(f"Entropy: {entropy:.2f} bits")
    
    if entropy < 28:
        strength = "Very Weak"
    elif entropy < 36:
        strength = "Weak"
    elif entropy < 60:
        strength = "Reasonable"
    elif entropy < 128:
        strength = "Strong"
    else:
        strength = "Very Strong"
    
    print(f"Strength: {strength}")
    
    print(f"\nCharacter composition:")
    print(f"  Uppercase: {sum(1 for c in password if c in string.ascii_uppercase)}")
    print(f"  Lowercase: {sum(1 for c in password if c in string.ascii_lowercase)}")
    print(f"  Digits: {sum(1 for c in password if c in string.digits)}")
    print(f"  Symbols: {sum(1 for c in password if c in string.punctuation)}")


def main():
    args = get_args()
    
    passwords = []
    
    if args.passphrase: # '-p', '--passphrase', Generate passphrase
        for _ in range(args.count):
            passphrase = generate_passphrase(args.words, args.separator)
            passwords.append(passphrase)
            
            if args.verbose:
                display_info(passphrase, args, string.ascii_lowercase)
            else:
                print(passphrase)
    
    else: # Generate standard password
        charset = get_character_set(args)
        
        total_min = args.min_upper + args.min_lower + args.min_digits + args.min_symbols
        if total_min > args.length:
            print(f"Error: Minimum requirements ({total_min}) exceed password length ({args.length})")
            sys.exit(1)
        
        for _ in range(args.count):
            password = generate_password(args.length, charset, args)
            passwords.append(password)
            
            if args.verbose:
                display_info(password, args, charset)
            else:
                print(password)
    
    if args.save: # '--save', Save passwords to file
        try:
            with open(args.save, 'w') as f:
                for pwd in passwords:
                    f.write(pwd + '\n')
            print(f"\nPasswords saved to: {args.save}")
        except IOError as e:
            print(f"\nError saving to file: {e}")
            sys.exit(1)


if __name__ == '__main__':
    main()