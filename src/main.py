import sys
from crawler import crawl
from indexer import Indexer
from search import SearchEngine

def main():
    indexer = Indexer()
    search = SearchEngine(indexer)

    print("=========================================")
    print("      Quotes Web Search Tool CLI         ")
    print("=========================================")
    print("Commands: build, load, print <word>, find <phrase>, exit")

    while True:
        try:
            # Get user input and split into command and arguments
            user_input = input("\n> ").strip().split(maxsplit=1)
            
            if not user_input:
                continue

            command = user_input[0].lower()
            args = user_input[1] if len(user_input) > 1 else ""

            if command == "build":
                print("\n[1/3] Starting crawler...")
                pages_data = crawl()
                print("\n[2/3] Building inverted index...")
                indexer.build_index(pages_data)
                print("[3/3] Saving index to disk...")
                indexer.save()
                print("Build complete!")

            elif command == "load":
                indexer.load()

            elif command == "print":
                if not args:
                    print("Usage error: Please provide a word (e.g., 'print nonsense').")
                else:
                    search.print_word(args)

            elif command == "find":
                if not args:
                    print("Usage error: Please provide a phrase (e.g., 'find good friends').")
                else:
                    search.find_phrase(args)

            elif command in ["exit", "quit"]:
                print("Exiting search tool...")
                break
                
            else:
                print("Unknown command. Available: build, load, print, find, exit")

        except KeyboardInterrupt:
            print("\nExiting search tool...")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()