import itertools
import string
import sys
import time
import os
import readline

def path_completer(text, state):
    line = readline.get_line_buffer()
    if os.path.isdir(line):
        options = [f for f in os.listdir(line) if f.startswith(text)]
    else:
        dirname, _, partial = line.rpartition('/')
        dirname += '/'
        options = [f for f in os.listdir(dirname) if f.startswith(partial)]
    options.append(None)
    return options[state]

def generate_wordlist(min_length, max_length, charset, filepath, verbosity):
    # Calculate the total number of words
    total_words = sum(len(charset)**i for i in range(min_length, max_length + 1))

    # Estimate the file size (rough estimate assuming average word length)
    avg_word_length = (min_length + max_length) / 2
    estimated_file_size = total_words * avg_word_length / (1024 * 1024)  # in MB

    print(f"Estimated file size: {estimated_file_size:.2f} MB")

    # Ask for confirmation
    confirm = input(f"Do you want to generate a wordlist of {total_words} words? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Wordlist generation aborted.")
        return

    start_time = time.time()

    with open(filepath, 'w') as f:
        words_generated = 0
        for word_length in range(min_length, max_length + 1):
            for word in itertools.product(charset, repeat=word_length):
                f.write(''.join(word) + '\n')
                words_generated += 1

                if verbosity > 0:
                    elapsed_time = time.time() - start_time
                    eta_seconds = (total_words - words_generated) * (elapsed_time / words_generated) if words_generated else 0
                    eta_hours, rem = divmod(eta_seconds, 3600)
                    eta_minutes, eta_seconds = divmod(rem, 60)
                    if verbosity >= 1:
                        print(f"\rWords generated: {words_generated}/{total_words} | ETA: {int(eta_hours):02}:{int(eta_minutes):02}:{int(eta_seconds):02}", end='', flush=True)
                    if verbosity >= 3 and words_generated % 1000 == 0:
                        elapsed_hours, rem = divmod(elapsed_time, 3600)
                        elapsed_minutes, elapsed_seconds = divmod(rem, 60)
                        print(f"\n{words_generated} words generated. Elapsed time: {int(elapsed_hours):02}:{int(elapsed_minutes):02}:{int(elapsed_seconds):02}")

    print("\nWordlist generation complete.")

if __name__ == "__main__":
    try:
        min_length = int(input("Enter minimum length of words: ").strip())
        max_length = int(input("Enter maximum length of words: ").strip())

        # Setting up tab completion
        readline.set_completer(path_completer)
        readline.parse_and_bind("tab: complete")

        charset_option = int(input("Select character set option:\n1. Default (letters, digits, punctuation, space)\n2. Custom\nEnter your choice (1 or 2): ").strip())

        if charset_option == 1:
            charset = string.ascii_letters + string.digits + string.punctuation + ' '
        elif charset_option == 2:
            charset = input("Enter your custom set of characters: ").strip()
        else:
            print("Invalid option. Exiting.")
            sys.exit(1)

        filepath = input("Enter the path with the name of the .txt file (including .txt extension): ").strip()
        if not filepath.endswith('.txt'):
            print("Error: The file name must end with .txt")
        else:
            verbosity = int(input("Enter verbosity level (0 to 5): ").strip())
            generate_wordlist(min_length, max_length, charset, filepath, verbosity)
    except Exception as e:
        print(f"Error: {e}")
