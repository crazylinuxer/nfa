from runner import Runner, red, green

if __name__ == "__main__":
    print("Building state map... ", end='', flush=True)
    try:
        runner = Runner()
    except Exception as exc:
        print(red("Error!"))
        print(exc.args[0])
        exit()
    print(green("Done"))

    print("Build the DFA for this NFA? [y/N]")
    try:
        response = input()
        if response in ['y', 'Y', 'д', 'Д']:
            runner.map.write_dfa_to_file("./dfa_input.txt")
    except (EOFError, KeyboardInterrupt):
        print()
        exit()
    except Exception as exc:
        print(red(exc.args[0]))
        exit()

    print("Would you like to see explanation of each automaton step? [Y/n]")
    try:
        response = input()
        if response in ['', 'y', 'Y', 'д', 'Д']:
            exp = True
        else:
            exp = False
        while True:
            value = input("Enter the string to check: ")
            if runner(value, exp):
                print("    Accept " + green("✔ ️") + '\n')
            else:
                print("    Reject " + red("❌") + '\n')
    except (EOFError, KeyboardInterrupt):
        print()
        exit()
    except Exception as exc:
        print(red(exc.args[0]))
        exit()
