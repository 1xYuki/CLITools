import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from hashlib import blake2b, blake2s, sha256
from pathlib import Path

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
        'Basic Usage: [INPUT] -l (Length), -a (Algorithm), -f (File), -s (Save), -v & -vv (Verbosity)'
    )
    parser.add_argument(
        'input', type=str, nargs='?', help='Input to be hashed (Omit to read from stdin)'
        )
    parser.add_argument(
        '-a', '--algorithm', type=str, default='blake2b', 
        choices=['blake2b', 'blake2s', 'sha256'],
        help='Hash algorithm to use: blake2b [Default], blake2s, or sha256'
        )
    parser.add_argument(
        '-l', '--length', type=int, default=None, 
        help='Maximum hash length in bytes: blake2b (1-64), blake2s (1-32), sha256 (fixed at 32)'
        )
    parser.add_argument(
        '-f', '--file', type=str, metavar='FILE',
        help='Hash contents of specified file'
        )
    parser.add_argument(
        '-s', '--save', type=str, metavar='FILE',
        help='Save hash output to specified file'
        )
    group.add_argument(
        '-q', '--quiet', action='store_true',
        help='Quiet mode, only output the hash'
        )
    group.add_argument(
        '-v', '--verbose', action='count', default=0,
        help='Add Verbosity (-v for verbose, -vv for full verbose)'
        )
    return parser.parse_args()


def get_hash_function(algorithm, length=None): # '-a', '--algorithm', Returns the appropriate hash function with specified digest length if applicable.
    if algorithm == 'blake2b':
        digest_size = length if length else 64
        if digest_size < 1 or digest_size > 64:
            print("Error: blake2b hash length must be between 1 and 64 bytes")
            sys.exit(1)
        return lambda data: blake2b(data, digest_size=digest_size).hexdigest()
    
    elif algorithm == 'blake2s':
        digest_size = length if length else 32
        if digest_size < 1 or digest_size > 32:
            print("Error: blake2s hash length must be between 1 and 32 bytes")
            sys.exit(1)
        return lambda data: blake2s(data, digest_size=digest_size).hexdigest()
    
    elif algorithm == 'sha256':
        if length and length != 32:
            print("Warning: sha256 has fixed length of 32 bytes, ignoring -l argument")
        return lambda data: sha256(data).hexdigest()
    
    else:
        print(f"Error: Unknown algorithm '{algorithm}'")
        sys.exit(1)


def get_input_data(args): # 'input', Retrieves input data from file, stdin, or command line argument
    if args.file: # '-f', '--file', File input
        try:
            with open(args.file, 'rb') as f:
                return f.read(), f'file: {args.file}'
        except IOError as e:
            print(f"Error reading file: {e}")
            sys.exit(1)
    
    elif args.input is None: # stdin input
        if sys.stdin.isatty():
            print("Error: No input provided. Use [INPUT], -f FILE, or pipe data via stdin")
            sys.exit(1)
        return sys.stdin.read().encode(), 'stdin'
    
    else: # CLI Argument
        return args.input.encode(), f"string: '{args.input}'"


def get_output_filename(args): # File output logic, if not specified '+_hash'
    if args.save:
        return args.save
    elif args.file:
        file_path = Path(args.file)
        return f"{file_path.stem}_hashed{file_path.suffix}"
    return None


def main():
    args = get_args()
    
    hash_func =(
        get_hash_function(args.algorithm, args.length)
        )
    
    input_data, input_source =(
        get_input_data(args)
    )
    
    output_file =(
        get_output_filename(args)
    )

    hashed_input =(
        hash_func(input_data)
    )

    if args.quiet: # '-q', '--quiet', Outputs Hash Quietly
        print(hashed_input)
        
        if output_file:
            try:
                with open(output_file, 'w') as f:
                    f.write(hashed_input + '\n')
            except IOError as e:
                print(f"\nError saving to file: {e}")
        return
    
    if args.verbose >= 1: # '-v', Verbosity Lvl 1
        print(f"Input source: {input_source}")
        print(f"Input length: {len(input_data)} bytes")
        print(f"Algorithm: {args.algorithm.upper()}")
        if args.length:
            print(f"Hash length: {args.length} bytes")
        print("-" * 50)
    
    if args.verbose >= 2: # '-vv', Verbosity Lvl 2
        print(f"Input as bytes: {input_data[:100]}{'...' if len(input_data) > 100 else ''}")
        print(f"Input hex: {input_data[:50].hex()}{'...' if len(input_data) > 50 else ''}")
        print(f"Processing with {args.algorithm.upper()} algorithm...")
        print("-" * 50)
    
    print(f"Hash: {hashed_input}")
    
    if args.verbose >= 1: # '-v' + '-vv', Verbose output statement
        actual_length = len(hashed_input) // 2
        print(f"Hash length: {len(hashed_input)} hex characters ({actual_length} bytes)")
    
    if output_file: # Save to file
        try:
            with open(output_file, 'w') as f:
                f.write(hashed_input + '\n')
            print(f"\nHash saved to: {output_file}")
        except IOError as e:
            print(f"\nError saving to file: {e}")

if __name__ == '__main__':
    main()