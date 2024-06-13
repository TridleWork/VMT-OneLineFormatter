import os
import re

patterns = [
    re.compile(r'VertexLitGeneric', re.IGNORECASE),
    re.compile(r'LightmappedGeneric', re.IGNORECASE),
    re.compile(r'#')
]


def scan_vmt_files(location):
    vmt_files = []
    for root, dirs, files in os.walk(location):
        for file in files:
            if file.endswith(".vmt"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as vmt_file:
                    lines = vmt_file.readlines()
                    if lines:
                        vmt_files.append((file_path, lines))
    return vmt_files


def format_vmt_file(file_path, lines):
    formatted_lines = []
    in_block = False
    header_found = False

    for line in lines:
        stripped_line = line.strip()

        if (not header_found and any(pattern.search(stripped_line) for pattern in patterns)):
            header_found = True
            formatted_lines.append(stripped_line)
            in_block = True
        elif stripped_line.startswith("{"):
            in_block = False
            formatted_lines.append("{")
            in_block = True
        elif stripped_line == "}":
            formatted_lines.append("}")
            in_block = False
        elif in_block and stripped_line:
            formatted_lines.append("\t" + stripped_line)
        elif stripped_line:
            formatted_lines.append(stripped_line)

    if not header_found:
        formatted_lines.insert(0, '"VertexLitGeneric"')
        if len(formatted_lines) == 1:
            formatted_lines.append("{")
        if formatted_lines[-1] != "}":
            formatted_lines.append("}")

    final_lines = []
    in_block = False
    for line in formatted_lines:
        if line.strip() == "{":
            in_block = True
            final_lines.append(line)
        elif line.strip() == "}":
            in_block = False
            final_lines.append(line)
        elif in_block:
            final_lines.append("\t" + line.strip())
        else:
            final_lines.append(line.strip())

    with open(file_path, "w") as vmt_file:
        vmt_file.write("\n".join(final_lines) + "\n")


if __name__ == "__main__":
    location = input("Enter the location to scan: ")
    vmt_files = scan_vmt_files(location)

    if vmt_files:
        for file_path, _ in vmt_files:
            print(f"File: {file_path}")

        format_files = input("Do you want to format all files? (y/n) ").lower() == "y"
        if format_files:
            for file_path, lines in vmt_files:
                format_vmt_file(file_path, lines)
    else:
        print("No .vmt files found in the specified location.")
