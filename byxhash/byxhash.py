from argparse import ArgumentParser, RawDescriptionHelpFormatter
from hashlib import blake2b

def get_args():
    parser = ArgumentParser(
        description='CLI Tool for checking and manipulating inputs with blake2b',
        epilog='Developed for Yuki, by Yuki, Always and Forever',
        formatter_class=RawDescriptionHelpFormatter
    )
    group =(
        parser.add_mutually_exclusive_group()
    )
    parser.usage =(
        'Basic Usage: [INPUT] -l (Length, 1-64), -s (Save Hash to File), -v & -vv (Verbosity)'
    )
    parser.add_argument(
        'input', type=str, help='Input to be hashed'
        )
    parser.add_argument(
        '-l', '--length', type=int, default=64, help='Maximum hash length in bytes: 1-64'
        )
    parser.add_argument(
        '-s', '--save', type=str, metavar='FILE',help='Save hash output to specified file'
        )
    group.add_argument(
        '-q', '--quiet', action='store_true',help='Quiet mode, only output the hash'
        )
    group.add_argument(
        '-v', '--verbose', action='count', default=0,help='Add Verbosity (-v for verbose, -vv for full verbose)'
        )
    return parser.parse_args()


def main():
    args = get_args()
    
    if args.length < 1 or args.length > 64: # '-l', '--length', Length Check 1 -64 Bytes
        print("Error: Hash length must be between 1 and 64 bytes")
        return
    
    hashed_input =( 
        blake2b(args.input.encode(), digest_size=args.length).hexdigest()
    )
    
    if args.quiet: # '-q', '--quiet', Outputs Hash Quietly
        print(hashed_input)
        
        if args.save:
            try:
                with open(args.save, 'w') as f:
                    f.write(hashed_input + '\n')
            except IOError as e:
                    print(f"\nError saving to file: {e}")
            return
    
    if args.verbose >= 1: # '-v', Verbosity Lvl 1
        print(f"Input string: '{args.input}'")
        print(f"Input length: {len(args.input)} characters")
        print(f"Hash length: {args.length} bytes")
        print(f"Algorithm: BLAKE2b")
        print("-" * 50)
    
    if args.verbose >= 2: # '-vv', Verbosity Lvl 2
        input_bytes = args.input.encode()
        print(f"Input as bytes: {input_bytes}")
        print(f"Input hex: {input_bytes.hex()}")
        print(f"Processing with BLAKE2b algorithm...")
        print("-" * 50)
    
    print(f"Hash: {hashed_input}")
    
    if args.verbose >= 1: # '-v' + '-vv', Verbose output statement
        print(f"Hash length: {len(hashed_input)} hex characters ({args.length} bytes)")
    
    if args.save: # 's', '--save', Save Argument
        try:
            with open(args.save, 'w') as f:
                f.write(hashed_input + '\n')
            print(f"\nHash saved to: {args.save}")
        except IOError as e:
            print(f"\nError saving to file: {e}")

if __name__ == '__main__':
    main()