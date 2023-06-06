#!/usr/bin/python3

# imports
import argparse
import os
import sys
import pyfiglet
import subprocess
import time

try:
    start_time = time.time()  # gets system time, used for calculating total runtime.
    banner = pyfiglet.figlet_format("GrayBox PCHistory Crusher")
    print(banner)  # prints banner using pyfiglet

    cwd = os.getcwd()  # establishes the current working directory of the script

    # Check if VirtualTerminalLevel registry value is set to 1 so color is allowed in powershell
    command = 'powershell -Command "(Get-ItemProperty -Path HKCU:\Console).VirtualTerminalLevel"'
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    current_value = result.stdout.strip()

    # If VirtualTerminalLevel registry entry is not set to 1, this sets it, otherwise this is skipped
    if current_value != "1":
        command = 'powershell -Command "Set-ItemProperty -Path HKCU:\Console -Name VirtualTerminalLevel -Value 1"'
        subprocess.run(command, shell=True)

    # instantiate parser to take user arguments
    parser = argparse.ArgumentParser("gbpc.py")

    # create arguments
    parser.add_argument(  # pcHistory location argument
        "-p",
        "--pcHistory",
        default=False,
        required=False,
        type=argparse.FileType("r"),
        help="Location of 'pchistory.txt' file. Default: file is in the same directory as gpc.py",
    )
    parser.add_argument(  # architecture for Hashcat argument
        "-arch",
        "--archType",
        default="all",
        required=False,
        type=str,
        help='Options are "CPU", "GPU", "FPGA" or "all" (default), for device doing the workload.',
    )
    parser.add_argument(  # hashcat aggressiveness argument
        "-agro",
        "--agroLvl",
        default=3,
        required=False,
        type=int,
        help="How hard do you want to work your computer (CPU/GPU) while brute forcing (1-4) Default: 3 \n Note: 1 has "
             "little impact, where 4 will make your computer unusable beyond this task.",
    )
    parser.add_argument(  # output to file argument
        "-o",
        "--out",
        default=False,
        required=False,
        dest="outFile",
        type=str,
        help="output file location and/or name ",
    )

    args = parser.parse_args()  # starts the parser


    def arch_check():  # checks user input to establish what architecture is to be used in hashcat
        arch_in = args.archType
        arch_valid = ["cpu", "gpu", "all"]
        if arch_in in arch_valid:
            if arch_in.lower() == "cpu":
                arch_in = "1"
                return arch_in
            elif arch_in.lower() == "gpu":
                arch_in = "2"
                return arch_in
            else:
                arch_in = "1,2,3"
                return arch_in
        else:
            print("Invalid architecture, select CPU, GPU, or ALL(default)")
            exit()


    arch_check()  # checks archetecture input provided by user


    def file_check():  # checs if file exists in the current directory, or wherever the user pointed to.
        pc_history = args.pcHistory
        if pc_history:
            return pc_history.name
        fccwd = os.getcwd()
        files = os.listdir(fccwd)
        for file in files:
            if file.endswith("pchistory.txt"):
                return file
        print('No pchistory.txt file was found in the current directory. Please specify the file via --pc_history')
        sys.exit()


    def proc_hashes(hash_in):  # strips pchistory.txt, ignoring any lines that start with #, and building an array
        lines = []
        with open(hash_in, "r") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    lines.append(line)
        return lines


    def read_proc_output(process):  # reads output from hashcat, only returns the hash and PC turning it green
        results = []
        while True:
            output = process.stdout.readline()
            if output == "" and process.poll() is not None:
                break
            if (
                    output.count(":") == 4
                    and "sha256" in output
                    and "Hash.Target" not in output
            ):
                results.append(output.strip())
        return results


    def cracker():  # hashcat logic, uses arguments provided by user to fill in list []
        for line in hash_array:
            hash_comm = [
                "hashcat",
                "-a",
                "3",
                "-m",
                "10900",
                "--potfile-disable",
                "-D",  # arch argument
                str(arch_check()),  # arch value
                "-w",  # agro argument
                str(args.agroLvl),  # agro level value
                line,  # single hash value
                "?d?d?d?d?d?d",
                "--increment",
                "--increment-min",
                "4",
            ]
            process = subprocess.Popen(
                hash_comm, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
            cracked_pins = read_proc_output(process)
            process.wait()
            for pin in cracked_pins:
                colon_count = pin.count(":")
                if colon_count >= 4:
                    pin_parts = pin.split(":", 4)
                    rest_of_pin = ":".join(pin_parts[4:])
                    pin_out_term = (
                            pin_parts[0]
                            + ":"
                            + pin_parts[1]
                            + ":"
                            + pin_parts[2]
                            + ":"
                            + pin_parts[3]
                            + ":"
                            + "\033[5;32m"
                            + rest_of_pin
                            + "\033[0m"
                    )
                    print(pin_out_term)
                    if args.outFile:
                        output_dir = os.path.dirname(args.outFile)
                        if os.path.isdir(output_dir):
                            with open(args.outFile, 'a') as f:
                                f.write(str(pin) + "\n")
                    else:
                        break


    # loading all necessary values.
    print("\u2714", end=" ")
    print("Checking Hash File!")
    hashIn = str(file_check())
    print("\u2714", end=" ")
    print("Loading Hashes!")
    hash_array = proc_hashes(file_check())
    print("\u2714", end=" ")
    print("Starting Hashcat For Your " + str(len(hash_array)) + " hashes!\n")
    print("\npasscode(s) will be displayed in green below\n")
    cracker()
    end_time = time.time()
    elapsed_time = end_time - start_time  # Calculate elapsed time of whole process

    # if the process runs for less than 30 seconds something is probably wrong. This could be implemented better in
    # future versions.
    if elapsed_time < 30:
        print("hashcat didn't like our input. Usually this happens if you select the wrong architecture, "
              "try a different option or dont provide an argument at all and try again.")

except KeyboardInterrupt:  # If the user killed the process with ctrl+c, this will be printed
    print("Look what you did, you killed it!")
    exit()
except Exception as e:  # This catches all other exceptions and prints the message below along with the error
    print("An unhandled exception has occurred. submit this error on Github")
    print(e)
